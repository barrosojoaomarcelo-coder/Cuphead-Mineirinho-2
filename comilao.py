"""Fase 2: duas formas e ataques dos desenhos do grupo. Frente: Moisés.

Como na aula, objetos visíveis são Sprites com image, rect e update.
Davi pode trocar as folhas em assets sem mudar as regras abaixo.
"""
import math
import pygame
from config import FLOOR, clamp
from sprites import Boss
from audio import play_sound


class Comilao(Boss):
    """Reaproveita vida e transformação do chefe, com outra arte e posição."""

    def mouth(self, elapsed):
        if self.phase < 3:
            return 1020, 447
        return 960, 540

    def eye(self):
        if self.phase < 3:
            return 1045, 300
        return 1060, 303

    def refresh_image(self, elapsed, state):
        form = 'comilao-corpo'
        position = (870, 190)
        if self.phase >= 3:
            form = 'comilao-boca'
            position = (842, 207)
        if state == 'transform' and self.transform < .52:
            form = 'comilao-corpo'
            position = (870, 190)
        index = int(elapsed * 5) % 4
        if self.breathing:
            index = 6
        elif self.warning is not None:
            index = 4 if self.warning['remaining'] > .5 else 5
        elif self.cast > 0:
            index = 7
        image = self.assets['frames'][form][index]
        if state == 'transform':
            image = image.copy()
            alpha = 1 - clamp(self.transform / .55, 0, 1)
            if form == 'comilao-boca':
                alpha = clamp((self.transform - .48) / .3, 0, 1)
            image.set_alpha(round(255 * alpha))
        if self.flash > 0:
            image = image.copy()
            image.fill((55, 45, 20, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.image = image
        self.rect = image.get_rect(topleft=position)
        self.hitbox = pygame.Rect(1005, 375, 190, 245)
        if self.phase >= 3:
            self.hitbox = pygame.Rect(900, 408, 335, 210)


class EyeRay(pygame.sprite.Sprite):
    """Raio fixo na direção anunciada; atinge no máximo uma vez."""

    def __init__(self, start, end):
        pygame.sprite.Sprite.__init__(self)
        self.start, self.end = start, end
        self.age = 0
        self.duration = .32
        self.touched = False
        self.rect = pygame.Rect(min(start[0], end[0]) - 10, min(start[1], end[1]) - 10,
                                abs(end[0] - start[0]) + 20, abs(end[1] - start[1]) + 20)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        first = pygame.Vector2(start) - self.rect.topleft
        last = pygame.Vector2(end) - self.rect.topleft
        for color, width in (((49, 30, 28), 16), ((181, 222, 49), 11), ((255, 251, 182), 4)):
            pygame.draw.line(self.image, color, first, last, width)

    def update(self, dt):
        self.age += dt
        if self.age >= self.duration:
            self.kill()

    def touches(self, player):
        return not self.touched and bool(player.hitbox.inflate(8, 8).clipline(self.start, self.end))


class Tongue(pygame.sprite.Sprite):
    """A língua cresce, alcança a arena e recolhe; desenho e colisão usam os mesmos pontos."""

    def __init__(self, start, mode):
        pygame.sprite.Sprite.__init__(self)
        self.start = start
        self.mode = mode
        self.age = 0
        self.duration = .82 if mode in ('sweep', 'moving') else .68
        self.touched = False
        self.points = []
        self.refresh_image()

    def update(self, dt):
        self.age += dt
        if self.age >= self.duration:
            self.kill()
            return
        self.refresh_image()

    def refresh_image(self):
        # Um quarto para esticar, um pequeno intervalo ativo, depois recolher.
        extension = min(1, self.age / .24, (self.duration - self.age) / .22)
        extension = clamp(extension, 0, 1)
        height = FLOOR - 22
        if self.mode == 'high':
            height = FLOOR - 175
        elif self.mode == 'moving':
            height = FLOOR - 90 - math.sin(self.age / self.duration * math.pi) * 95
        end_x = self.start[0] + (45 - self.start[0]) * extension
        bend_x = max(end_x, self.start[0] - 130)
        self.points = [self.start, (bend_x, height), (end_x, height)]
        if self.mode == 'sweep':
            lift = max(0, (self.age - .27) / .35) * 105 * extension
            self.points[-1] = (end_x, height - lift)
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        self.rect = pygame.Rect(min(xs) - 14, min(ys) - 14, max(xs) - min(xs) + 28, max(ys) - min(ys) + 28)
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        local = [pygame.Vector2(p) - self.rect.topleft for p in self.points]
        for color, width in (((49, 30, 28), 24), ((190, 77, 94), 18), ((243, 144, 145), 7)):
            pygame.draw.lines(self.image, color, False, local, width)
        pygame.draw.circle(self.image, (49, 30, 28), local[-1], 12)
        pygame.draw.circle(self.image, (243, 144, 145), local[-1], 8)

    def touches(self, player):
        if self.touched:
            return False
        box = player.hitbox.inflate(14, 14)
        for index in range(len(self.points) - 1):
            if box.clipline(self.points[index], self.points[index + 1]):
                return True
        return False


class Spike(pygame.sprite.Sprite):
    """Espinho que cai na marca indicada no chão e sai da arena."""

    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = x, 68
        self.image = pygame.Surface((32, 72), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (49, 30, 28), [(0, 0), (31, 0), (16, 71)])
        pygame.draw.polygon(self.image, (151, 183, 47), [(5, 3), (26, 3), (16, 58)])
        pygame.draw.line(self.image, (224, 229, 132), (9, 6), (16, 45), 3)
        self.rect = self.image.get_rect(midtop=(x, round(self.y)))
        self.hitbox = self.rect.inflate(-14, -18)

    def update(self, dt):
        self.y += 320 * dt
        self.rect.midtop = self.x, round(self.y)
        self.hitbox.center = self.rect.center
        if self.rect.top > FLOOR:
            self.kill()


def prepare_comilao(game, kind=None):
    """Define o ataque e seus pontos antes do aviso, sem perseguir o jogador depois."""
    sequence = ['eye', 'low', 'high', 'sweep']
    if game.boss.phase >= 3:
        sequence = ['low', 'spikes', 'high', 'moving', 'eye', 'sweep']
    if kind is None:
        kind = sequence[game.pattern_index % len(sequence)]
        game.pattern_index += 1
    duration = 1.35
    warning = {'type': 'comilao', 'kind': kind, 'remaining': duration, 'total': duration,
               'fired': False, 'x': game.boss.mouth(0)[0], 'y': game.boss.mouth(0)[1]}
    guidance = {'eye': 'OLHO CARREGANDO: SAIA DAS LINHAS',
                'low': 'LÍNGUA BAIXA: PREPARE O PULO',
                'high': 'LÍNGUA ALTA: FIQUE NO CHÃO',
                'sweep': 'RASTEIRA: PULE A LÍNGUA',
                'moving': 'LÍNGUA SUBINDO: FIQUE NO CHÃO',
                'spikes': 'ESPINHOS: VÁ PARA A FAIXA VERDE'}
    warning['guidance'] = guidance[kind]
    if kind == 'eye':
        warning['origin'] = game.boss.eye()
        warning['ends'] = [(140, FLOOR), (450, FLOOR), (760, FLOOR)]
    if kind == 'spikes':
        warning['safe_x'] = clamp(game.player.x, 190, 710)
        warning['lanes'] = [x for x in range(80, 861, 130) if abs(x - warning['safe_x']) > 180]
    game.warnings.append(warning)
    game.attack_timer = 3.7 if kind == 'spikes' else 3.25
    game.boss.cast = duration + .9
    game.boss.attack_type = kind
    play_sound(game.assets, 'telegraph')


def release_comilao(game, warning):
    kind = warning['kind']
    if kind == 'eye':
        for end in warning['ends']:
            game.beams.add(EyeRay(warning['origin'], end))
    elif kind == 'spikes':
        for x in warning['lanes']:
            game.fire.add(Spike(x))
    else:
        game.beams.add(Tongue((warning['x'], warning['y']), kind))
    play_sound(game.assets, 'attack')


def update_comilao(game, dt):
    game.attack_timer -= dt
    for warning in list(game.warnings):
        warning['remaining'] -= dt
        if not warning['fired'] and warning['remaining'] <= 0:
            warning['fired'] = True
            release_comilao(game, warning)
        if warning['remaining'] < -.15:
            game.warnings.remove(warning)
    if game.attack_timer <= 0 and not game.warnings and not game.beams and not game.fire:
        prepare_comilao(game)


def draw_comilao_warning(renderer, target, warning, color):
    """Davi pode ajustar os avisos aqui; os pontos vêm do ataque anunciado."""
    kind = warning['kind']
    if kind == 'eye':
        for end in warning['ends']:
            pygame.draw.line(target, color, warning['origin'], end, 2)
            pygame.draw.ellipse(target, color, (end[0] - 24, FLOOR - 6, 48, 12), 2)
    elif kind == 'spikes':
        for x in warning['lanes']:
            pygame.draw.ellipse(target, (224, 90, 65), (x - 22, FLOOR - 6, 44, 12), 3)
            pygame.draw.line(target, color, (x, 80), (x, 115), 3)
        pygame.draw.line(target, (177, 222, 106), (warning['safe_x'] - 165, FLOOR),
                         (warning['safe_x'] + 165, FLOOR), 6)
    else:
        y = FLOOR - 175 if kind == 'high' else FLOOR - 22
        if kind == 'moving':
            y = FLOOR - 185
        for x in range(50, 920, 32):
            pygame.draw.line(target, color, (x, y), (x + 12, y), 2)
    message = warning['guidance']
    if kind in ('low', 'sweep') and warning['remaining'] < .18:
        message = 'PULE AGORA!'
    renderer.text(target, message, (640, 105), 25, color, True, outline=True)
