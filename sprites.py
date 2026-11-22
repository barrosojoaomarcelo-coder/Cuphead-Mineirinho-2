"""Objetos do jogo com Sprite, image, rect e update. Responsável: Moisés.

Davi cuida das imagens e das escolhas de animação em assets.py.
"""
import math
import pygame
from config import (FLOOR, LIVES, BOSS_HP, PLAYER_SPEED, GRAVITY, JUMP_SPEED,
                    SHOT_SPEED, SHOT_INTERVAL, DASH_SPEED, DASH_TIME, DASH_COOLDOWN, clamp)
from assets import player_pose, fire_image, flame_image
from animation import animated_frame


def hitboxes_overlap(first, second):
    """Caixas menores que as imagens deixam a esquiva mais justa."""
    if hasattr(second, 'previous_center'):
        area = first.hitbox.inflate(second.hitbox.width, second.hitbox.height)
        return bool(area.clipline(second.previous_center, second.hitbox.center))
    return first.hitbox.colliderect(second.hitbox)


class Player(pygame.sprite.Sprite):
    """Personagem: a posição x/y representa o ponto dos pés."""

    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.x = 190
        self.y = FLOOR
        self.vx = 0
        self.vy = 0
        self.hp = LIVES
        self.facing = 1
        self.on_ground = True
        self.crouch = False
        self.dash = 0
        self.dash_direction = 1
        self.dash_cooldown = 0
        self.invulnerable = 0
        self.shot_cooldown = 0
        self.shot_speed = SHOT_SPEED
        self.shot_interval = SHOT_INTERVAL
        self.anim_time = 0
        self.jump_age = 0
        self.land_time = 0
        self.shooting = False
        self.aim_x = 1
        self.aim_y = 0
        self.jump_buffer = 0
        self.coyote = .12
        self.previous_input = {}
        self.dashed = False
        self.jumped = False
        self.landed = False
        self.refresh_image()

    def update(self, dt, controls, can_dash=True, limit=920, left_limit=53):
        """Lê controles, movimenta e sincroniza imagem/caixa de colisão."""
        was_shooting = self.shooting
        self.dashed = False
        self.jumped = False
        self.landed = False
        self.invulnerable = max(0, self.invulnerable - dt)
        self.dash_cooldown = max(0, self.dash_cooldown - dt)
        self.shot_cooldown = max(-dt, self.shot_cooldown - dt)
        self.land_time = max(0, self.land_time - dt)
        self.anim_time += dt
        self.handle_input(controls, can_dash)
        if self.shooting and not was_shooting:
            self.shot_cooldown = max(0, self.shot_cooldown)
        self.move(dt, limit, left_limit)
        self.previous_input = controls.copy()
        self.refresh_image()

    def handle_input(self, controls, can_dash):
        """Detecta o instante do pulo/dash e a direção do movimento e da mira."""
        if controls.get('jump') and not self.previous_input.get('jump'):
            self.jump_buffer = .12
        if not controls.get('jump') and self.previous_input.get('jump') and self.vy < -220:
            self.vy *= .52  # Soltar cedo produz um salto mais baixo.
        direction = 0
        if controls.get('right'):
            direction += 1
        if controls.get('left'):
            direction -= 1
        self.direction = direction
        self.crouch = bool(controls.get('down')) and self.on_ground and self.dash <= 0
        if direction != 0 and self.dash <= 0:
            self.facing = direction
        self.aim_x = self.facing
        self.aim_y = 0
        if controls.get('up') and not controls.get('down'):
            self.aim_x = direction
            self.aim_y = -1
        self.shooting = bool(controls.get('shoot'))
        pressed_dash = controls.get('dash') and not self.previous_input.get('dash')
        if pressed_dash and can_dash and self.dash_cooldown <= 0:
            self.dash = DASH_TIME
            self.dash_cooldown = DASH_COOLDOWN
            self.dash_direction = self.facing
            if direction != 0:
                self.dash_direction = direction
            self.vy = 0
            self.dashed = True

    def move(self, dt, limit, left_limit=53):
        """Aplica aceleração, gravidade, salto e limites da arena."""
        self.jump_buffer = max(0, self.jump_buffer - dt)
        # Pequenas tolerâncias tornam o pulo próximo ao chão mais confortável.
        if self.on_ground:
            self.coyote = .11
        else:
            self.coyote = max(0, self.coyote - dt)
        if self.jump_buffer > 0 and self.coyote > 0 and self.dash <= 0:
            self.vy = -JUMP_SPEED
            self.on_ground = False
            self.jump_age = 0
            self.coyote = 0
            self.jump_buffer = 0
            self.jumped = True
        if self.dash > 0:
            self.dash = max(0, self.dash - dt)
            self.vx = self.dash_direction * DASH_SPEED
        else:
            speed = PLAYER_SPEED
            if self.crouch:
                speed = 115
            acceleration = 2700
            if self.direction == 0:
                acceleration = 3300
            target = self.direction * speed
            self.vx += clamp(target - self.vx, -acceleration * dt, acceleration * dt)
            self.vy += GRAVITY * dt
        self.x = clamp(self.x + self.vx * dt, left_limit, limit)
        self.y += self.vy * dt
        if self.y >= FLOOR:
            if not self.on_ground and self.vy > 180:
                self.land_time = .16
                self.landed = True
            self.y = FLOOR
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False
            self.jump_age += dt

    def refresh_image(self):
        """Mantém image e rect prontos para Group.draw()."""
        self.action, self.frame = player_pose(self)
        frames = self.assets['frames']
        pivot_x = 120 * 174 / 256
        if self.facing < 0:
            frames = self.assets['flipped']
            pivot_x = 174 - pivot_x
        pose = 0
        if self.land_time > .05:
            pose = 1
        elif self.dash > 0:
            pose = 3
        elif not self.on_ground and self.vy < -200:
            pose = 2
        image = animated_frame(self.assets, self.action, self.frame, pose, self.facing < 0,
                               (round(pivot_x), round(240 * 174 / 256)))
        if self.invulnerable > 0 and int(self.anim_time * 16) % 2 == 0:
            image = image.copy()
            image.set_alpha(100)
        self.image = image
        self.rect = image.get_rect(topleft=(round(self.x - pivot_x), round(self.y - 240 * 174 / 256)))
        if self.crouch or (self.dash > 0 and self.on_ground):
            self.hitbox = pygame.Rect(round(self.x - 16), round(self.y - 53), 32, 47)
        else:
            self.hitbox = pygame.Rect(round(self.x - 16), round(self.y - 99), 32, 90)

    def shoot(self):
        """Cria um pão na posição do indicador registrada no manifesto."""
        frames = self.assets['manifest']['player']['actions'][self.action]
        muzzle = frames['muzzles'][self.frame]
        if muzzle is not None:
            x = self.x + (muzzle[0] - 120) * 174 / 256 * self.facing
            y = self.y + (muzzle[1] - 240) * 174 / 256
        else:
            x = self.x + 66 * self.facing
            y = self.y - 83
            if self.crouch:
                y = self.y - 54
        return Bread(self.assets, x, y, self.aim_x, self.aim_y, self.shot_speed)


class Boss(pygame.sprite.Sprite):
    """Dragão com duas formas visuais e quatro níveis de ataque."""

    def __init__(self, assets):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.hp = BOSS_HP
        self.max_hp = BOSS_HP
        self.phase = 1
        self.flash = 0
        self.cast = 0
        self.transform = 0
        self.attack_type = None
        self.attack_mode = None
        self.charge = 0
        self.mouth_lock = None
        self.warning = None
        self.breathing = False
        self.horizontal = None
        self.dip_active = False
        self.dip_y = 0
        self.dip_from = 0
        self.dip_target = 0
        self.dip_age = 0
        self.dip_duration = .3
        self.pulse = 0
        self.refresh_image(0, 'title')

    def mouth(self, elapsed):
        """Durante o aviso de um especial, a boca mantém a mesma posição."""
        if self.mouth_lock is not None:
            return self.mouth_lock
        bob = math.sin(elapsed * 1.7) * 12
        if self.dip_active:
            bob = self.dip_y
        if self.phase < 3:
            return 1059, 341 + bob
        return 1090, 439 + bob

    def update(self, dt, elapsed, state):
        self.flash = max(0, self.flash - dt)
        self.cast = max(0, self.cast - dt)
        self.pulse = max(0, self.pulse - dt)
        if self.dip_active:
            self.dip_age = min(self.dip_duration, self.dip_age + dt)
            t = self.dip_age / self.dip_duration
            self.dip_y = self.dip_from + (self.dip_target - self.dip_from) * t * t * (3 - 2 * t)
        self.refresh_image(elapsed, state)

    def move_mouth(self, mouth_y, elapsed, duration=.3):
        """Abaixa o dragão até a altura da próxima fileira, sem teletransporte."""
        self.dip_from = self.dip_y if self.dip_active else math.sin(elapsed * 1.7) * 12
        self.dip_target = mouth_y - (341 if self.phase < 3 else 439)
        self.dip_age, self.dip_duration = 0, duration
        self.dip_active = True
        self.mouth_lock = None

    def refresh_image(self, elapsed, state):
        form = 'base'
        x, y = 858, 181
        mouth_y = 341
        if self.phase >= 3:
            form = 'head'
            x, y = 902, 158
            mouth_y = 439
        if state == 'transform' and self.transform < .52:
            form = 'base'
            x, y = 858, 181
        bob = math.sin(elapsed * 1.7) * 12
        if self.dip_active:
            bob = self.dip_y
        if self.mouth_lock is not None:
            bob = self.mouth_lock[1] - mouth_y
        index = int(elapsed * 12) % 4
        pose = 1 if int(elapsed * 6) % 2 else 0
        if self.breathing:
            index = 6
            pose = 3
        elif self.warning is not None:
            pose = 2
            index = 5
            if self.warning['remaining'] / self.warning['total'] > .42:
                index = 4
        elif self.cast > 0:
            pose = 4
            index = 7
            if self.cast > .1:
                index = 6
        if self.pulse > 0:
            pose = 3
        image = animated_frame(self.assets, form, index, pose, bright=self.flash > 0)
        if state == 'transform':
            image = image.copy()
            if form == 'base':
                alpha = 1 - clamp(self.transform / .55, 0, 1)
            else:
                alpha = clamp((self.transform - .48) / .3, 0, 1)
            image.set_alpha(round(255 * alpha))
        self.image = image
        self.rect = image.get_rect(topleft=(x, round(y + bob)))
        if self.phase < 3:
            self.hitbox = pygame.Rect(1035, round(252 + bob), 175, 358)
        else:
            self.hitbox = pygame.Rect(991, round(203 + bob), 265, 405)


class Bread(pygame.sprite.Sprite):
    """Tiro do jogador; kill() o remove de todos os grupos."""

    def __init__(self, assets, x, y, aim_x, aim_y, speed=SHOT_SPEED):
        pygame.sprite.Sprite.__init__(self)
        self.base_image = assets['bread']
        self.x, self.y = x, y
        length = math.hypot(aim_x, aim_y)
        if length == 0:
            length = 1
        self.vx = aim_x / length * speed
        self.vy = aim_y / length * speed
        self.age = 0
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(round(x), round(y)))
        self.hitbox = pygame.Rect(0, 0, 18, 18)
        self.hitbox.center = self.rect.center

    def update(self, dt):
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.image = pygame.transform.rotate(self.base_image, -self.age * 800)
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
        self.hitbox.center = self.rect.center
        if self.age > 1.4 or self.x < -40 or self.x > 1320 or self.y < -50 or self.y > 760:
            self.kill()


class Fire(pygame.sprite.Sprite):
    """Bola comum, gigante, ondulada, de chuva ou com quique."""

    def __init__(self, assets, data, mouth):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.x = data.get('x', mouth[0])
        self.y = data.get('y', mouth[1])
        angle = data.get('angle', 0)
        speed = data.get('speed', 0)
        self.vx = data.get('vx', math.cos(angle) * speed)
        self.vy = data.get('vy', math.sin(angle) * speed)
        self.kind = data.get('kind', 'orb')
        self.r = data.get('r', 16)
        self.gravity = data.get('gravity', 0)
        self.bounces = data.get('bounces', 0)
        self.amplitude = data.get('amplitude', 0)
        self.frequency = data.get('frequency', 0)
        self.base_y = self.y
        self.age = 0
        self.refresh_image()
        self.previous_center = self.hitbox.center

    def update(self, dt):
        self.previous_center = self.hitbox.center
        self.age += dt
        self.x += self.vx * dt
        if self.kind == 'sine':
            self.base_y += self.vy * dt
            self.y = self.base_y + math.sin(self.age * self.frequency) * self.amplitude
        else:
            self.vy += self.gravity * dt
            self.y += self.vy * dt
        if self.kind == 'bounce' and self.y + self.r >= FLOOR:
            if self.bounces > 0:
                self.y = FLOOR - self.r - 1
                self.vy = -abs(self.vy) * .78
                self.bounces -= 1
            else:
                self.kill()
        if self.age > 9 or self.x < -70 or self.x > 1400 or self.y < -140 or self.y > 790:
            self.kill()
        self.refresh_image()

    def refresh_image(self):
        self.image = fire_image(self.assets, self.r, math.atan2(self.vy, self.vx))
        self.rect = self.image.get_rect(center=(round(self.x), round(self.y)))
        radius = self.r * .76
        if self.kind == 'giant':
            radius = self.r * .5
        self.hitbox = pygame.Rect(0, 0, round(radius * 2), round(radius * 2))
        self.hitbox.center = self.rect.center


class Flame(pygame.sprite.Sprite):
    """Sopro anunciado: vive meio segundo e registra um único contato."""

    def __init__(self, warning):
        pygame.sprite.Sprite.__init__(self)
        self.x = warning['x']
        self.y = warning['y']
        self.end_x = warning['end_x']
        self.end_y = warning['end_y']
        self.half_width = warning.get('half_width', 22)
        self.age = 0
        self.duration = warning.get('duration', .5)
        self.touched = False
        self.image, self.rect = flame_image(self)

    def update(self, dt):
        self.age += dt
        if self.age >= self.duration:
            self.kill()
        self.image, self.rect = flame_image(self)

    def touches(self, player):
        """Rect.clipline faz o teste do sopro sem um algoritmo geométrico próprio."""
        if self.age < .08 or self.touched:
            return False
        area = player.hitbox.inflate(round(self.half_width * 1.44), round(self.half_width * 1.44))
        return bool(area.clipline((self.x, self.y), (self.end_x, self.end_y)))
