"""Invocações, anéis e lasers do Olho da Pirâmide. Frente: Moisés; avisos: Davi."""
import pygame
from config import FLOOR
from piramide import Servant, EnergyRing, PyramidLaser
from audio import play_sound

GREEN = (160, 234, 90)
PURPLE = (226, 114, 244)


def laser_paths(kind, height=350, mirrored=False):
    """Pontos anunciados dos padrões dos esboços, sem seguir o jogador."""
    left, right = (145, height), (1130, height)
    if kind == 'horizontal':
        paths = [(left, right)]
    elif kind == 'cross':
        paths = [(left, (755, 602)), (right, (525, 602))]
    elif kind == 'diamond':
        paths = [(left, (640, 150), right), (left, (640, 602), right), ((640, 150), (640, 602))]
    elif kind == 'floor':
        paths = [(left, (410, 602), (870, 602), right)]
    else:
        paths = [(left, (700, 602), (470, 350), (1100, 190))]
    if mirrored:
        paths = [tuple((1280 - x, y) for x, y in points) for points in paths]
    return paths


def safe_floor_lanes(paths):
    """Marca apenas trechos onde o jogador em pé cabe fora dos raios."""
    safe = []
    start = None
    for x in range(220, 1081, 20):
        box = pygame.Rect(x - 24, FLOOR - 110, 48, 110)
        blocked = any(box.clipline(points[i], points[i + 1])
                      for points in paths for i in range(len(points) - 1))
        if not blocked and start is None:
            start = x
        if blocked and start is not None:
            if x - start >= 60:
                safe.append((start, x - 20))
            start = None
    if start is not None and 1080 - start >= 40:
        safe.append((start, 1080))
    return safe


def prepare_piramide(game, kind=None):
    """Escolhe um padrão da forma atual e devolve o aviso guardado em game.warnings.

    Na primeira forma prepara criaturas ou anéis; na segunda fixa trajetos de
    laser e calcula as faixas verdes. A mira é definida antes do disparo.
    """
    phase = game.boss.phase
    sequence = ['snakes', 'rings_low', 'bats', 'rings_high', 'swarm', 'rings_fan']
    if phase >= 3:
        sequence = ['horizontal', 'cross', 'ricochet', 'diamond', 'floor']
    if kind is None:
        kind = sequence[game.pattern_index % len(sequence)]
        game.pattern_index += 1
    duration = (1.05, .95, 1.15, .95)[phase - 1]
    warning = {'type': 'piramide', 'kind': kind, 'phase': phase, 'remaining': duration,
               'total': duration, 'fired': False, 'origin': game.boss.eye(), 'target_y': game.player.y - 55}
    if phase >= 3:
        game.clear_attacks()  # Um padrão de laser nunca cobre restos do anterior.
        low = kind == 'horizontal' and game.breath_count % 2 == 0
        game.breath_count += int(kind == 'horizontal')
        height = 590 if low else 350
        game.boss.target_eye_y = height
        warning['paths'] = laser_paths(kind, height, game.pattern_index % 2 == 0 and kind == 'ricochet')
        if kind == 'ricochet':
            first = game.boss.eye('left', height)
            last = game.boss.eye('right', height)
            if game.pattern_index % 2 == 0:
                first, last = last, first
            warning['paths'] = [(first, (game.player.x, FLOOR - 35), (640, 180), last)]
        warning['safe'] = safe_floor_lanes(warning['paths'])
        if kind == 'horizontal':
            warning['guidance'] = 'RAIO BAIXO: PREPARE O PULO' if low else 'RAIO ALTO: FIQUE NO CHÃO'
            warning['low'] = low
        else:
            warning['guidance'] = {'cross': 'RAIOS CRUZADOS: SAIA DO CENTRO',
                'diamond': 'LOSANGO: AFASTE-SE DA LINHA CENTRAL',
                'floor': 'REFLEXO NO CHÃO: PULE OU VÁ PARA A LATERAL',
                'ricochet': 'MIRA FIXA: MOVA-SE PARA A FAIXA VERDE'}[kind]
    elif kind.startswith('rings'):
        warning['guidance'] = 'ANÉIS BAIXOS: PULE OU USE DASH' if kind != 'rings_high' else 'ANÉIS ALTOS: FIQUE NO CHÃO'
        if kind == 'rings_fan':
            warning['guidance'] = 'ANÉIS ALTERNADOS: PULE OS BAIXOS, FIQUE NO CHÃO NOS ALTOS'
    else:
        warning['guidance'] = 'SERES INVOCADOS: ATIRE PARA ABRIR CAMINHO'
    game.warnings.append(warning)
    game.boss.attack_type = kind
    game.boss.cast = duration + .5
    game.attack_timer = (2.55, 2.30, 2.7, 2.35)[phase - 1]
    play_sound(game.assets, 'telegraph')
    return warning


def release_piramide(game, warning):
    """Libera lasers ou agenda criaturas e anéis a partir dos pontos do aviso.

    Os dois olhos usam os mesmos padrões de laser; a vida compartilhada é
    tratada pelo motor, não por esta função de criação dos perigos.
    """
    w = warning
    kind, phase = w['kind'], w['phase']
    game.boss.pulse = .16
    game.boss.cast = .5
    if 'paths' in w:
        for index, points in enumerate(w['paths']):
            game.beams.add(PyramidLaser(points, GREEN if index % 2 == 0 else PURPLE,
                                       .46 if phase == 3 else .50))
    elif kind.startswith('rings'):
        count = 3 if phase == 1 else 4
        for index in range(count):
            high = kind == 'rings_high' or (kind == 'rings_fan' and index % 2 == 1)
            game.scheduled.append({'delay': index * .80, 'kind': 'ring', 'origin': w['origin'],
                                   'lane_y': FLOOR - (170 if high else 35), 'speed': 310 if phase == 1 else 350})
    else:
        kinds = ['snake', 'snake'] if kind == 'snakes' else ['bat', 'bat', 'bat']
        if kind == 'swarm':
            kinds = ['snake', 'bat', 'snake', 'bat']
        for index, servant in enumerate(kinds):
            game.scheduled.append({'delay': index * .36, 'kind': servant,
                'x': 1010 + index * 22, 'y': FLOOR if servant == 'snake' else 300 + index * 45,
                'speed': (175 if servant == 'snake' else 220) + (phase - 1) * 25,
                'target_y': w['target_y']})
    play_sound(game.assets, 'attack')


def update_piramide(game, dt):
    """Avança os atrasos e avisos e inicia outro padrão quando os lasers terminam.

    Limita as criaturas simultâneas a seis e retira ações já executadas da fila.
    """
    game.attack_timer -= dt
    for data in list(game.scheduled):
        data['delay'] -= dt
        if data['delay'] <= 0:
            if data['kind'] == 'ring':
                game.beams.add(EnergyRing(data['origin'], data['lane_y'], data['speed']))
            elif len(game.minions) < 6:
                game.minions.add(Servant(game.assets, data['kind'], data['x'], data['y'], data['speed'], data['target_y']))
            game.scheduled.remove(data)
    for warning in list(game.warnings):
        warning['remaining'] -= dt
        if not warning['fired'] and warning['remaining'] <= 0:
            warning['fired'] = True
            release_piramide(game, warning)
        if warning['remaining'] < -.15:
            game.warnings.remove(warning)
    lasers_active = any(isinstance(beam, PyramidLaser) for beam in game.beams)
    if game.attack_timer <= 0 and not game.warnings and not game.scheduled and not lasers_active:
        prepare_piramide(game)


def draw_piramide_warning(renderer, target, warning, color):
    """Desenha trajetos anunciados e faixas seguras sem modificar a lógica dos ataques."""
    w = warning
    if 'paths' in w:
        for points in w['paths']:
            for index in range(len(points) - 1):
                start = pygame.Vector2(points[index])
                delta = pygame.Vector2(points[index + 1]) - start
                for part in range(0, 100, 4):
                    pygame.draw.line(target, color, start + delta * (part / 100),
                                     start + delta * ((part + 2) / 100), 2)
        if w['kind'] != 'horizontal':
            for left, right in w['safe']:
                pygame.draw.line(target, GREEN, (left, FLOOR), (right, FLOOR), 5)
    else:
        origin = w['origin']
        radius = round(18 + (1 - w['remaining'] / w['total']) * 20)
        pygame.draw.circle(target, color, origin, radius, 3)
        if w['kind'].startswith('rings'):
            y = FLOOR - (170 if w['kind'] == 'rings_high' else 35)
            pygame.draw.ellipse(target, GREEN, (690, y - 49, 58, 98), 3)
    message = w['guidance']
    if w.get('low') and w['remaining'] < .17:
        message = 'PULE AGORA!'
    renderer.text(target, message, (640, 105), 24, color, True, outline=True)
