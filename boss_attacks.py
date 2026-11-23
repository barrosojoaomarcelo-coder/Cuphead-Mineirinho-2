"""Valores do perfil HARD_ATTACKS do ZIP, em dicionários simples. Frente: Moisés.

Cada posição da tupla corresponde a um dos quatro níveis internos do dragão.
Os números são os mesmos do arquivo recebido; não usamos dataclasses.
"""


def dragon_stage(index):
    """Devolve os parâmetros do nível interno index, de 0 a 3, do dragão.

    Tempos são segundos, velocidades são pixels por segundo e contagens são
    quantidades de projéteis ou ondas. HARD_ATTACKS reúne os quatro dicionários.
    """
    return {
        'normal_speed': (440, 490, 550, 610)[index],
        'interval': (1.95, 1.80, 1.65, 1.50)[index],
        'warning': (.80, .76, .72, .68)[index],
        'special_warning': (.95, .90, .85, .80)[index],
        'flame_warning': .90 if index < 2 else .85,
        'rain_interval': 3.1, 'max_fire': 72,
        'horizontal_speed': (700, 760, 840, 920)[index],
        'horizontal_rows': (2, 2, 3, 4)[index],
        'horizontal_count': (4, 5, 5, 6)[index],
        'horizontal_spacing': (.09, .08, .08, .07)[index],
        'horizontal_gap': .78,
        'giant_speed': (720, 800, 860, 920)[index],
        'giant_count': 1 if index < 2 else 2, 'giant_gap': 1.0,
        'fan_count': (6, 7, 8, 9)[index], 'fan_spread': .19,
        'fan_waves': 1 if index < 2 else 2, 'fan_gap': .30, 'fan_offset': .095,
        'aimed_count': (4, 5, 5, 6)[index], 'aimed_gap': (.18, .17, .16, .15)[index],
        'burst_count': (5, 6, 7, 8)[index], 'burst_gap': (.14, .13, .12, .11)[index],
        'burst_spread': .035 if index < 2 else .045,
        'steps_count': (3, 3, 4, 4)[index], 'steps_gap': .24,
        'sine_count': (4, 5, 6, 6)[index], 'sine_gap': .16,
        'sine_amplitude': (30, 34, 38, 42)[index], 'sine_frequency': 5.2,
        'bounce_count': (2, 2, 3, 3)[index], 'bounce_speed': (300, 320, 350, 380)[index],
        'bounce_gap': .28, 'bounce_gravity': 520,
        'rain_speed': (310, 340, 370, 400)[index], 'rain_waves': (1, 2, 2, 3)[index],
        'rain_gap': (.50, .46, .42, .38)[index],
        'flame_half_width': 26 if index < 2 else 28, 'flame_duration': .5,
    }


HARD_ATTACKS = tuple(dragon_stage(index) for index in range(4))

# A pressão cresce dentro de cada forma do Comilão. Cada golpe de um combo
# recebe seu próprio aviso; a sequência não persegue o jogador.
COMILAO_WARNINGS = (1.0, .92, .86, .78)
COMILAO_INTERVALS = (2.55, 2.35, 2.15, 1.95)
COMILAO_SPIKE_SPEED = (360, 400, 440, 500)
