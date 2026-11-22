"""Fase 2: duas formas e ataques dos desenhos do grupo. Frente: Moisés.

Como na aula, objetos visíveis são Sprites com image, rect e update.
Davi pode trocar as folhas em assets sem mudar as regras abaixo.
"""
import math
import pygame
from config import FLOOR, clamp
from sprites import Boss
from audio import play_sound
from animation import animated_frame
from boss_attacks import COMILAO_WARNINGS, COMILAO_INTERVALS, COMILAO_SPIKE_SPEED


class Comilao(Boss):
    """Reaproveita vida e transformação do chefe, com outra arte e posição."""

    def mouth(self, elapsed):
        if self.phase < 3:
            return 1020, 447
        return 960, 520

    def eye(self):
        if self.phase < 3:
            return 1025, 300
        return 1005, 280

    def refresh_image(self, elapsed, state):
        form = 'comilao-corpo'
        position = (870, 190)
        if self.phase >= 3:
            form = 'comilao-boca'
            position = (842, 188)
        if state == 'transform' and self.transform < .52:
            form = 'comilao-corpo'
            position = (870, 190)
        # Animação em poses: respira, pisca, prepara, dispara e recupera.
        idle = (0, 1, 2, 1, 0, 0, 0, 0, 0, 3, 0, 0)
        index = idle[int(elapsed * 8) % len(idle)]
        if self.breathing or self.pulse > 0:
            index = 8 + int(elapsed * 12) % 2
            if self.attack_type == 'eye':
                index = 6
        elif self.warning is not None:
            progress = 1 - self.warning['remaining'] / self.warning['total']
            index = 4 + min(3, int(progress * 4))
            if self.attack_type == 'eye':
                index = min(index, 6)
        elif self.cast > 0:
            index = 10 if self.cast > .15 else 11
        self.frame = index
        image = animated_frame(self.assets, form, index, bright=self.flash > 0)
        if state == 'transform':
            image = image.copy()
            alpha = 1 - clamp(self.transform / .55, 0, 1)
            if form == 'comilao-boca':
                alpha = clamp((self.transform - .48) / .3, 0, 1)
            image.set_alpha(round(255 * alpha))
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
        self.duration = .38
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
        self.duration = .76 if mode in ('sweep', 'moving') else .64
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
        extension = min(1, self.age / .19, (self.duration - self.age) / .18)
        extension = clamp(extension, 0, 1)
        height = FLOOR - 22
        if self.mode == 'high':
            height = FLOOR - 175
        elif self.mode == 'moving':
            height = FLOOR - 90 - math.sin(self.age / self.duration * math.pi) * 95
        end_x = self.start[0] + (45 - self.start[0]) * extension
        bend_x = max(end_x, self.start[0] - 130)
        self.points = [self.start, (bend_x, height)]
        for index in range(1, 21):
            part = index / 20
            x = bend_x + (end_x - bend_x) * part
            wave = math.sin(part * math.pi * 2 - self.age * 16) * 5 * math.sin(part * math.pi)
            lift = 0
            if self.mode == 'sweep':
                lift = clamp((self.age - .25) / .3, 0, 1) * 110 * extension * part ** 4
            self.points.append((x, height + wave - lift))
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

    def __init__(self, x, speed=440):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = x, 68
        self.speed = speed
        self.image = pygame.Surface((32, 72), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (49, 30, 28), [(0, 0), (31, 0), (16, 71)])
        pygame.draw.polygon(self.image, (151, 183, 47), [(5, 3), (26, 3), (16, 58)])
        pygame.draw.line(self.image, (224, 229, 132), (9, 6), (16, 45), 3)
        self.rect = self.image.get_rect(midtop=(x, round(self.y)))
        self.hitbox = self.rect.inflate(-14, -18)

    def update(self, dt):
        self.y += self.speed * dt
        self.rect.midtop = self.x, round(self.y)
        self.hitbox.center = self.rect.center
        if self.rect.top > FLOOR:
            self.kill()


def prepare_comilao(game, kind=None, chain=None):
    """Define o ataque e seus pontos antes do aviso, sem perseguir o jogador depois."""
    sequence = ['eye', 'low', 'high', 'sweep']
    if game.boss.phase >= 3:
        sequence = ['low', 'spikes', 'high', 'moving', 'eye', 'sweep']
    if kind is None:
        kind = sequence[game.pattern_index % len(sequence)]
        game.pattern_index += 1
    phase = game.boss.phase
    duration = COMILAO_WARNINGS[phase - 1]
    followup = chain is not None
    if followup:
        duration = max(.72, duration - .12)
    else:
        chain = []
        if kind == 'low' and phase >= 2:
            chain = ['high', 'low'] if phase == 4 else ['high']
        elif kind == 'eye' and phase >= 3:
            chain = ['eye']
    warning = {'type': 'comilao', 'kind': kind, 'remaining': duration, 'total': duration,
               'fired': False, 'chain': chain, 'phase': phase,
               'x': game.boss.mouth(0)[0], 'y': game.boss.mouth(0)[1]}
    guidance = {'eye': 'OLHO CARREGANDO: SAIA DAS LINHAS',
                'low': 'LÍNGUA BAIXA: PREPARE O PULO',
                'high': 'LÍNGUA ALTA: FIQUE NO CHÃO',
                'sweep': 'RASTEIRA: PULE A LÍNGUA',
                'moving': 'LÍNGUA SUBINDO: FIQUE NO CHÃO',
                'spikes': 'ESPINHOS: VÁ PARA A FAIXA VERDE'}
    warning['guidance'] = guidance[kind]
    if chain:
        warning['guidance'] += ' · COMBO'
    if kind == 'eye':
        warning['origin'] = game.boss.eye()
        count = (3, 4, 4, 5)[phase - 1]
        warning['ends'] = [(100 + index * 720 / (count - 1), FLOOR) for index in range(count)]
    if kind == 'spikes':
        warning['safe_x'] = clamp(game.player.x, 150, 750)
        warning['lanes'] = [x for x in range(80, 861, 110) if abs(x - warning['safe_x']) > 125]
    game.warnings.append(warning)
    game.attack_timer = COMILAO_INTERVALS[phase - 1]
    game.boss.cast = duration + .9
    game.boss.attack_type = kind
    play_sound(game.assets, 'telegraph')


def release_comilao(game, warning):
    kind = warning['kind']
    phase = warning['phase']
    game.boss.pulse = .16
    game.boss.cast = .65
    if kind == 'eye':
        for end in warning['ends']:
            game.beams.add(EyeRay(warning['origin'], end))
    elif kind == 'spikes':
        for wave in range(3 if phase == 4 else 2):
            for x in warning['lanes']:
                if wave == 0:
                    game.fire.add(Spike(x, COMILAO_SPIKE_SPEED[phase - 1]))
                else:
                    game.scheduled.append({'delay': wave * .34, 'spike_x': x,
                                           'speed': COMILAO_SPIKE_SPEED[phase - 1]})
    else:
        game.beams.add(Tongue((warning['x'], warning['y']), kind))
    chain = warning['chain']
    if chain:
        game.scheduled.append({'delay': .88, 'followup': chain[0], 'chain': chain[1:]})
    play_sound(game.assets, 'attack')


def update_comilao(game, dt):
    game.attack_timer -= dt
    for data in list(game.scheduled):
        data['delay'] -= dt
        if data['delay'] <= 0:
            if 'spike_x' in data:
                game.fire.add(Spike(data['spike_x'], data['speed']))
            else:
                prepare_comilao(game, data['followup'], data['chain'])
            game.scheduled.remove(data)
    for warning in list(game.warnings):
        warning['remaining'] -= dt
        if not warning['fired'] and warning['remaining'] <= 0:
            warning['fired'] = True
            release_comilao(game, warning)
        if warning['remaining'] < -.15:
            game.warnings.remove(warning)
    if game.attack_timer <= 0 and not game.warnings and not game.beams and not game.fire and not game.scheduled:
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
        pygame.draw.line(target, (177, 222, 106), (warning['safe_x'] - 110, FLOOR),
                         (warning['safe_x'] + 110, FLOOR), 6)
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
