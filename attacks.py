"""Dez famílias de ataques do dragão, adaptadas do ZIP difícil. Frente: Moisés."""
import math
from config import FLOOR, clamp
from sprites import Fire, Flame
from audio import play_sound
from boss_attacks import HARD_ATTACKS


def schedule(game, delay, data):
    """Inclui em game.scheduled um disparo ou movimento para depois de delay segundos.

    O dicionário data recebe a contagem regressiva; update_attacks executa a ação.
    """
    data['delay'] = delay
    game.scheduled.append(data)


def update_attacks(game, dt):
    """Avança avisos e ações agendadas do dragão usando dt em segundos.

    Libera ataques anunciados, limita bolas de fogo e só prepara outro padrão
    quando os ataques especiais anteriores deixam a arena.
    """
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
            if 'pose_y' in data:
                game.boss.horizontal['row_index'] = data['row']
                game.boss.move_mouth(data['pose_y'], game.elapsed)
            elif len(game.fire) < HARD_ATTACKS[game.boss.phase - 1]['max_fire']:
                game.fire.add(Fire(game.assets, data, game.boss.mouth(game.elapsed)))
                game.boss.cast = max(game.boss.cast, .3)
                game.boss.pulse = .10
            game.scheduled.remove(data)
    boss = game.boss
    if boss.horizontal is not None:
        horizontal = boss.horizontal
        busy = any(f.kind == 'horizontal' for f in game.fire)
        busy = busy or any(d.get('kind') == 'horizontal' or 'pose_y' in d for d in game.scheduled)
        if horizontal['state'] == 'firing' and not busy:
            horizontal['state'] = 'recover'
            base_y = 341 if boss.phase < 3 else 439
            boss.move_mouth(base_y, game.elapsed, .38)
        elif horizontal['state'] == 'recover' and boss.dip_age >= boss.dip_duration:
            boss.horizontal = None
            boss.dip_active = False
    giant_active = any(f.kind == 'giant' for f in game.fire)
    giant_pending = any(d.get('kind') == 'giant' for d in game.scheduled)
    warning_active = any(not w['fired'] for w in game.warnings)
    if game.attack_timer <= 0 and not game.beams and not giant_active and not giant_pending and not warning_active and boss.horizontal is None:
        prepare_attack(game)


def prepare_attack(game, kind=None):
    """Escolhe um padrão do nível atual e devolve seu dicionário de aviso.

    kind permite escolher um padrão nos testes; None percorre a sequência da luta.
    A mira, alturas e corredores são definidos antes do disparo. O aviso fica
    em game.warnings e os parâmetros de dificuldade vêm de HARD_ATTACKS.
    """
    phase = game.boss.phase
    tuning = HARD_ATTACKS[phase - 1]
    sequence = ['horizontal', 'giant', 'flame', 'fan', 'horizontal', 'aimed', 'steps', 'sine', 'bounce', 'burst']
    if phase >= 3:
        sequence = ['horizontal', 'giant', 'flame', 'rain', 'horizontal', 'bounce', 'fan', 'burst', 'sine', 'aimed', 'steps']
    if kind is None:
        kind = sequence[game.pattern_index % len(sequence)]
        game.pattern_index += 1
    duration = tuning['warning']
    if kind in ('giant', 'horizontal'):
        duration = tuning['special_warning']
    elif kind == 'flame':
        duration = tuning['flame_warning']
    if kind in ('flame', 'giant', 'rain', 'horizontal'):
        game.clear_attacks()
    x, y = game.boss.mouth(game.elapsed)
    target_x, target_y = game.player.x, game.player.y - 58
    warning = {'type': kind, 'remaining': duration, 'total': duration, 'x': x, 'y': y,
               'angle': math.atan2(target_y - y, target_x - x), 'phase': phase,
               'target_x': target_x, 'target_y': target_y, 'fired': False}
    if kind == 'flame':
        prepare_flame(game, warning)
        warning['half_width'] = tuning['flame_half_width']
        warning['duration'] = tuning['flame_duration']
    elif kind == 'giant':
        warning['target_y'] = game.player.y - 32
        warning['angle'] = math.atan2(warning['target_y'] - y, target_x - x)
        warning['guidance'] = f"{tuning['giant_count']} BOLA(S) GIGANTE(S): DESVIE EM SEQUÊNCIA!"
        game.boss.mouth_lock = x, y
    else:
        game.boss.mouth_lock = None
    if kind == 'horizontal':
        first = 'low' if (game.horizontal_count % 2 == 0) == (phase < 3) else 'high'
        game.horizontal_count += 1
        rows = []
        for index in range(tuning['horizontal_rows']):
            mode = first if index % 2 == 0 else ('low' if first == 'high' else 'high')
            rows.append({'index': index, 'mode': mode, 'y': 594 if mode == 'low' else 538,
                         'start': index * tuning['horizontal_gap'], 'count': tuning['horizontal_count'],
                         'spacing': tuning['horizontal_spacing'], 'speed': tuning['horizontal_speed']})
        warning.update(rows=rows, mode=first, lane_y=rows[0]['y'], angle=math.pi)
        game.boss.horizontal = {'state': 'windup', 'rows': rows, 'row_index': 0}
        game.boss.move_mouth(rows[0]['y'], game.elapsed, .32)
    if kind == 'rain':
        lane = clamp(math.floor((game.player.x - 65) / 130 + .5), 1, 5)
        warning['safe_x'] = 65 + lane * 130
        warning['lanes'] = [65 + index * 130 for index in range(7) if abs(65 + index * 130 - warning['safe_x']) > 145]
    game.warnings.append(warning)
    game.boss.cast = duration + .4
    game.boss.attack_type = kind
    game.boss.attack_mode = warning.get('mode')
    game.boss.charge = 0
    game.attack_timer = tuning['rain_interval'] if kind == 'rain' else tuning['interval']
    play_sound(game.assets, 'telegraph')
    return warning


def prepare_flame(game, warning):
    """Preenche o aviso do sopro alternando as alturas baixa e alta.

    Fixa os pontos do raio e a boca do chefe para o desenho e a colisão
    continuarem usando o mesmo trajeto depois que o jogador se mover.
    """
    mode = 'low'
    target_y = FLOOR - 18
    guidance = 'RAJADA BAIXA: PREPARE O PULO'
    if game.breath_count % 2 == 1:
        mode, target_y = 'high', FLOOR - 165
        guidance = 'RAJADA ALTA: FIQUE NO CHÃO'
    game.breath_count += 1
    warning.update(mode=mode, target_y=target_y, guidance=guidance, end_x=20)
    warning['angle'] = math.atan2(target_y - warning['y'], warning['target_x'] - warning['x'])
    warning['end_y'] = warning['y'] + math.tan(warning['angle']) * (20 - warning['x'])
    game.boss.mouth_lock = warning['x'], warning['y']


def release_attack(game, warning):
    """Converte o aviso em sopro ou ações de disparo agendadas.

    Usa a mira e os parâmetros guardados no aviso; update_attacks cria as bolas
    quando cada atraso termina. Também atualiza a pose e o som do ataque.
    """
    w = warning
    w['fired'] = True
    phase, kind = w['phase'], w['type']
    t = HARD_ATTACKS[phase - 1]
    speed = t['normal_speed']
    game.boss.charge = 0
    game.boss.pulse = .13
    if kind == 'horizontal':
        game.boss.horizontal = {'state': 'firing', 'rows': w['rows'], 'row_index': 0}
        for row in w['rows']:
            if row['index'] > 0:
                schedule(game, row['start'] - .34, {'pose_y': row['y'], 'row': row['index']})
            for index in range(row['count']):
                schedule(game, row['start'] + index * row['spacing'],
                         {'kind': 'horizontal', 'x': w['x'], 'y': row['y'],
                          'row': row['index'], 'mode': row['mode'], 'vx': -row['speed'], 'vy': 0, 'r': 14})
    elif kind == 'flame':
        game.fire.empty()
        game.scheduled.clear()
        game.beams.add(Flame(w))
        game.boss.cast = .65
    elif kind == 'giant':
        game.fire.empty()
        game.scheduled.clear()
        for index in range(t['giant_count']):
            schedule(game, index * t['giant_gap'],
                     {'x': w['x'], 'y': w['y'], 'angle': w['angle'], 'speed': t['giant_speed'],
                      'r': 44, 'kind': 'giant', 'chain_index': index})
        game.boss.cast = (t['giant_count'] - 1) * t['giant_gap'] + .65
    elif kind == 'fan':
        for wave in range(t['fan_waves']):
            for index in range(t['fan_count']):
                angle = w['angle'] + (index - (t['fan_count'] - 1) / 2) * t['fan_spread'] + wave * t['fan_offset']
                schedule(game, wave * t['fan_gap'], {'angle': angle, 'speed': speed, 'r': 14 if phase < 3 else 15})
    elif kind in ('aimed', 'burst'):
        for index in range(t[kind + '_count']):
            offset = ((index % 3) - 1) * t['burst_spread'] if kind == 'burst' else 0
            schedule(game, index * t[kind + '_gap'], {'angle': w['angle'] + offset, 'speed': speed, 'r': 14})
    elif kind == 'steps':
        for index in range(t['steps_count']):
            target_y = FLOOR - (180 if index % 2 else 38)
            angle = math.atan2(target_y - w['y'], w['target_x'] - w['x'])
            schedule(game, index * t['steps_gap'], {'angle': angle, 'speed': speed, 'r': 14})
    elif kind == 'sine':
        for index in range(t['sine_count']):
            angle = w['angle'] + (index - (t['sine_count'] - 1) / 2) * .15
            schedule(game, index * t['sine_gap'], {'angle': angle, 'speed': speed, 'kind': 'sine',
                     'amplitude': t['sine_amplitude'], 'frequency': t['sine_frequency'], 'r': 14})
    elif kind == 'bounce':
        for index in range(t['bounce_count']):
            schedule(game, index * t['bounce_gap'], {'kind': 'bounce', 'vx': -t['bounce_speed'], 'vy': -145,
                     'gravity': t['bounce_gravity'], 'bounces': 1, 'r': 18})
    elif kind == 'rain':
        for wave in range(t['rain_waves']):
            for x in w['lanes']:
                schedule(game, wave * t['rain_gap'], {'x': x, 'y': 68, 'vx': 0, 'vy': t['rain_speed'], 'r': 14, 'kind': 'rain'})
    play_sound(game.assets, 'attack')
