"""Os nove padrões de ataque do dragão. Responsável: Moisés.

Um aviso guarda os dados do ataque. Depois do prazo, cria os sprites.
"""
import math
from config import FLOOR, clamp
from sprites import Fire, Flame
from audio import play_sound


def schedule(game, delay, data):
    """Marca um projétil para sair após delay segundos."""
    data['delay'] = delay
    game.scheduled.append(data)


def update_attacks(game, dt):
    """Atualiza avisos, dispara projéteis agendados e escolhe o próximo ataque."""
    game.attack_timer -= dt
    for warning in list(game.warnings):
        warning['remaining'] -= dt
        if not warning['fired']:
            game.boss.charge = clamp(1 - warning['remaining'] / warning['total'], 0, 1)
            if warning['remaining'] <= 0:
                warning['fired'] = True
                release_attack(game, warning)
        if warning['remaining'] <= -.15:
            game.warnings.remove(warning)
    for data in list(game.scheduled):
        data['delay'] -= dt
        if data['delay'] <= 0:
            game.fire.add(Fire(game.assets, data, game.boss.mouth(game.elapsed)))
            game.boss.cast = max(game.boss.cast, .3)
            game.scheduled.remove(data)
    giant_active = False
    for fire in game.fire:
        if fire.kind == 'giant':
            giant_active = True
    warning_active = False
    for warning in game.warnings:
        if not warning['fired']:
            warning_active = True
    if game.attack_timer <= 0 and not game.beams and not giant_active and not warning_active:
        prepare_attack(game)


def prepare_attack(game, kind=None):
    """Escolhe o padrão e anuncia a direção antes de lançar o ataque."""
    phase = game.boss.phase
    sequence = ['giant', 'flame', 'fan', 'aimed', 'steps', 'sine', 'bounce', 'burst']
    if phase >= 3:
        sequence = ['flame', 'giant', 'rain', 'bounce', 'fan', 'burst', 'sine', 'aimed', 'steps']
    if kind is None:
        kind = sequence[game.pattern_index % len(sequence)]
        game.pattern_index += 1
    duration = 1.3
    if phase >= 3:
        duration = 1.2
    if kind == 'flame':
        duration = 1.4
    elif kind == 'giant':
        duration = 1.35
    x, y = game.boss.mouth(game.elapsed)
    target_x = game.player.x
    target_y = game.player.y - 58
    warning = {'type': kind, 'remaining': duration, 'total': duration,
               'x': x, 'y': y, 'angle': math.atan2(target_y - y, target_x - x),
               'phase': phase, 'target_x': target_x, 'target_y': target_y, 'fired': False}
    if kind in ('flame', 'giant', 'rain'):
        game.clear_attacks()  # O especial não se sobrepõe a uma rajada antiga.
    if kind == 'flame':
        prepare_flame(game, warning)
    elif kind == 'giant':
        warning['target_y'] = game.player.y - 32
        warning['angle'] = math.atan2(warning['target_y'] - y, target_x - x)
        warning['guidance'] = 'BOLA GIGANTE: PULE OU DESVIE!'
        game.boss.mouth_lock = x, y
    else:
        game.boss.mouth_lock = None
    if kind == 'rain':
        lane = clamp(math.floor((game.player.x - 95) / 150 + .5), 0, 5)
        warning['safe_x'] = 95 + lane * 150
        warning['lanes'] = []
        for index in range(6):
            lane_x = 95 + index * 150
            if abs(lane_x - warning['safe_x']) > 195:
                warning['lanes'].append(lane_x)
    game.warnings.append(warning)
    game.boss.cast = duration + .4
    game.boss.attack_type = kind
    game.boss.attack_mode = warning.get('mode')
    game.boss.charge = 0
    intervals = [0, 3.7, 3.7, 3.45, 3.2]
    game.attack_timer = intervals[phase]
    if kind == 'rain':
        game.attack_timer = 3.8
    if kind in ('flame', 'giant'):
        play_sound(game.assets, 'telegraph')


def prepare_flame(game, warning):
    """Alterna sopros baixos e altos, apontados para a posição anunciada."""
    mode = 'low'
    target_y = FLOOR - 18
    guidance = 'RAJADA BAIXA: PREPARE O PULO'
    if game.breath_count % 2 == 1:
        mode = 'high'
        target_y = FLOOR - 165
        guidance = 'RAJADA ALTA: FIQUE NO CHÃO'
    game.breath_count += 1
    warning['mode'] = mode
    warning['target_y'] = target_y
    warning['angle'] = math.atan2(target_y - warning['y'], warning['target_x'] - warning['x'])
    warning['end_x'] = 20
    warning['end_y'] = warning['y'] + math.tan(warning['angle']) * (20 - warning['x'])
    warning['guidance'] = guidance
    game.boss.mouth_lock = warning['x'], warning['y']


def release_attack(game, warning):
    """Nove casos explícitos: fica fácil estudar um ataque por vez."""
    w = warning
    w['fired'] = True
    phase = w['phase']
    kind = w['type']
    speed = [0, 205, 220, 230, 245][phase]
    game.boss.charge = 0
    if kind == 'flame':
        game.fire.empty()
        game.scheduled.clear()
        game.beams.add(Flame(w))
        game.boss.cast = .65
    elif kind == 'giant':
        game.fire.empty()
        game.scheduled.clear()
        giant_speed = 205
        if phase >= 3:
            giant_speed = 215
        schedule(game, 0, {'x': w['x'], 'y': w['y'], 'angle': w['angle'],
                           'speed': giant_speed, 'r': 44, 'kind': 'giant'})
        game.boss.cast = .65
    elif kind == 'fan':
        count = [0, 3, 3, 4, 5][phase]
        radius = 14
        if phase >= 3:
            radius = 15
        for index in range(count):
            angle = w['angle'] + (index - (count - 1) / 2) * .24
            schedule(game, 0, {'angle': angle, 'speed': speed, 'r': radius})
    elif kind in ('aimed', 'burst'):
        count = 2
        if phase >= 3:
            count = 3
        for index in range(count):
            schedule(game, index * .28, {'angle': w['angle'], 'speed': speed, 'r': 14})
    elif kind == 'steps':
        for index in range(2):
            target_y = FLOOR - 38
            if index == 1:
                target_y = FLOOR - 180
            angle = math.atan2(target_y - w['y'], w['target_x'] - w['x'])
            schedule(game, index * .36, {'angle': angle, 'speed': speed, 'r': 14})
    elif kind == 'sine':
        count = 3
        amplitude = 20
        if phase >= 3:
            count = 4
            amplitude = 27
        for index in range(count):
            angle = w['angle'] + (index - (count - 1) / 2) * .15
            schedule(game, index * .23, {'angle': angle, 'speed': speed, 'kind': 'sine',
                                        'amplitude': amplitude, 'frequency': 4.1, 'r': 14})
    elif kind == 'bounce':
        vx = -195
        if phase >= 3:
            vx = -205
        schedule(game, 0, {'kind': 'bounce', 'vx': vx, 'vy': -145, 'gravity': 420, 'bounces': 1, 'r': 18})
    elif kind == 'rain':
        for x in w['lanes']:
            schedule(game, 0, {'x': x, 'y': 68, 'vx': 0, 'vy': 210, 'r': 14, 'kind': 'rain'})
    play_sound(game.assets, 'attack')
