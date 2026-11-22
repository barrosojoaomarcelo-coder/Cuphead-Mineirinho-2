"""Sprites da terceira fase. Regras: Moisés; artes/animação: Davi."""
import math
import pygame
from config import FLOOR, clamp
from sprites import Boss
from animation import animated_frame


class Piramide(Boss):
    """Um chefe, duas formas e vida compartilhada pelos dois olhos finais."""

    def __init__(self, assets):
        self.eye_y = 350
        self.target_eye_y = 350
        Boss.__init__(self, assets)

    def eye(self, side='right', height=None):
        if self.phase < 3:
            return 1042, 350 + math.sin(getattr(self, 'elapsed', 0) * 2) * 8
        y = self.eye_y if height is None else height
        return (145 if side == 'left' else 1130), y

    def update(self, dt, elapsed, state):
        self.elapsed = elapsed
        self.eye_y += clamp(self.target_eye_y - self.eye_y, -1000 * dt, 1000 * dt)
        Boss.update(self, dt, elapsed, state)

    def corner_image(self, side, elapsed, state):
        name = 'piramide-olho-' + ('esquerdo' if side == 'left' else 'direito')
        index = 1 if int(elapsed * 8) % 20 == 16 else 0
        if self.warning is not None:
            index = 3
        elif self.pulse > 0:
            # A pose 3 tem o olho aberto sem um raio embutido na arte.
            index = 3
        elif self.cast > 0:
            index = 5
        image = animated_frame(self.assets, name, index, bright=self.flash > 0)
        if state == 'transform':
            image = image.copy()
            image.set_alpha(round(255 * clamp((self.transform - .42) / .4, 0, 1)))
        x = -30 if side == 'left' else 1010
        # O olho ocupa a mesma altura do ponto de emissão dos lasers.
        rect = image.get_rect(topleft=(x, round(self.eye_y - 211)))
        return image, rect

    def refresh_image(self, elapsed, state):
        if self.phase >= 3 and not (state == 'transform' and self.transform < .5):
            self.image, self.rect = self.corner_image('right', elapsed, state)
            self.hitbox = pygame.Rect(1110, max(210, round(self.eye_y - 100)), 150,
                                       max(90, FLOOR - max(210, round(self.eye_y - 100))))
            return
        idle = (0, 1, 2, 1, 0, 0, 0, 3, 0, 0, 0, 0)
        index = idle[int(elapsed * 8) % len(idle)]
        if self.warning is not None:
            progress = 1 - self.warning['remaining'] / self.warning['total']
            index = 4 + min(3, int(progress * 4))
        elif self.pulse > 0:
            index = 8 + int(elapsed * 12) % 2
        elif self.cast > 0:
            index = 10 if self.cast > .15 else 11
        self.image = animated_frame(self.assets, 'piramide-base', index, bright=self.flash > 0)
        if state == 'transform':
            self.image = self.image.copy()
            self.image.set_alpha(round(255 * (1 - clamp(self.transform / .55, 0, 1))))
        bob = math.sin(elapsed * 2) * 8
        self.rect = self.image.get_rect(topleft=(830, round(125 + bob)))
        self.hitbox = pygame.Rect(965, round(285 + bob), 245, 305)


class PyramidSide(pygame.sprite.Sprite):
    """Olho esquerdo: desenha e recebe tiros; o dano vai ao mesmo chefe."""

    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self)
        self.boss = boss
        self.update(0, 0, 'title')

    def update(self, dt, elapsed, state):
        boss = self.boss
        if boss.phase < 3 or (state == 'transform' and boss.transform < .5):
            self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
            self.rect = pygame.Rect(-20, -20, 1, 1)
            self.hitbox = pygame.Rect(-20, -20, 0, 0)
            return
        self.image, self.rect = boss.corner_image('left', elapsed, state)
        top = max(210, round(boss.eye_y - 100))
        self.hitbox = pygame.Rect(20, top, 155, max(90, FLOOR - top))


class Servant(pygame.sprite.Sprite):
    """Serpente rasteja; morcego cruza o ar com direção fixada ao nascer."""

    def __init__(self, assets, kind, x, y, speed, target_y=None):
        pygame.sprite.Sprite.__init__(self)
        self.assets, self.kind = assets, kind
        self.x, self.y, self.base_y = x, y, y
        self.vx = -speed
        self.vy = 0
        if kind == 'bat':
            self.vy = clamp((target_y - y) / max(.1, (x - 190) / speed), -80, 80)
        self.hp = 2 if kind == 'snake' else 1
        self.age = 0
        self.refresh_image()

    def update(self, dt):
        self.age += dt
        self.x += self.vx * dt
        self.base_y += self.vy * dt
        self.y = FLOOR if self.kind == 'snake' else self.base_y + math.sin(self.age * 6) * 16
        self.refresh_image()
        if self.x < -100 or self.y > 730 or self.y < 60 or self.age > 9:
            self.kill()

    def refresh_image(self):
        name = 'servo-serpente' if self.kind == 'snake' else 'servo-morcego'
        self.image = self.assets['frames'][name][int(self.age * 12) % 6]
        if self.kind == 'snake':
            self.rect = self.image.get_rect(midbottom=(round(self.x), FLOOR + 4))
            self.hitbox = pygame.Rect(round(self.x - 20), FLOOR - 78, 40, 72)
        else:
            self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
            self.hitbox = pygame.Rect(round(self.x - 22), round(self.y - 22), 44, 44)


class EnergyRing(pygame.sprite.Sprite):
    """Anel vazado que sai do olho e se estabiliza numa altura anunciada."""

    def __init__(self, origin, lane_y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.start_y = origin
        self.y = self.start_y
        self.lane_y, self.speed = lane_y, speed
        self.age, self.touched = 0, False
        self.rx, self.ry = 29, 49
        self.image = pygame.Surface((70, 112), pygame.SRCALPHA)
        for color, width, inset in (((40, 24, 44), 10, 4), ((159, 236, 80), 6, 4), ((244, 255, 181), 2, 4)):
            pygame.draw.ellipse(self.image, color, (inset, inset, 62, 104), width)
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))

    def update(self, dt):
        self.age += dt
        self.x -= self.speed * dt
        progress = clamp(self.age / .55, 0, 1)
        self.y = self.start_y + (self.lane_y - self.start_y) * progress
        self.rect.center = round(self.x), round(self.y)
        if self.x < -80 or self.age > 6:
            self.kill()

    def touches(self, player):
        if self.touched:
            return False
        # Testa a borda elíptica; o espaço vazio do anel não causa dano.
        box = player.hitbox
        near_x = clamp(self.x, box.left, box.right) - self.x
        near_y = clamp(self.y, box.top, box.bottom) - self.y
        nearest = (near_x / self.rx) ** 2 + (near_y / self.ry) ** 2
        farthest = max(((x - self.x) / self.rx) ** 2 + ((y - self.y) / self.ry) ** 2
                       for x, y in (box.topleft, box.topright, box.bottomleft, box.bottomright))
        return nearest <= 1.18 and farthest >= .70


class PyramidLaser(pygame.sprite.Sprite):
    """Trajeto fixo com reflexões: desenho e colisão usam os mesmos segmentos."""

    def __init__(self, points, color, duration=.46):
        pygame.sprite.Sprite.__init__(self)
        self.points = tuple(points)
        self.duration = duration
        self.age, self.touched = 0, False
        xs, ys = [p[0] for p in points], [p[1] for p in points]
        self.rect = pygame.Rect(min(xs) - 12, min(ys) - 12, max(xs) - min(xs) + 24, max(ys) - min(ys) + 24)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        local = [pygame.Vector2(p) - self.rect.topleft for p in points]
        for ink, width in (((40, 24, 44), 20), (color, 14), ((255, 247, 208), 5)):
            pygame.draw.lines(self.image, ink, False, local, width)
        for p in local[1:-1]:
            pygame.draw.circle(self.image, (255, 247, 208), p, 9, 2)

    def update(self, dt):
        self.age += dt
        if self.age >= self.duration:
            self.kill()

    def touches(self, player):
        if self.touched:
            return False
        box = player.hitbox.inflate(16, 16)
        return any(box.clipline(self.points[i], self.points[i + 1]) for i in range(len(self.points) - 1))
