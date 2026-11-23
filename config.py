"""Constantes do jogo. Moisés ajusta os valores de dificuldade aqui."""
WIDTH = 1280
HEIGHT = 720
FLOOR = 622
FPS = 60
GAME_TITLE = 'Mineirinho'
CREATORS_LABEL = 'Criadores: Davi, Moisés e João Marcelo'

LIVES = 3
# Índices físicos preservados: 0=Dragão, 1=Comilão, 2=Pirâmide.
STAGE_ORDER = (2, 1, 0)
DRAGON_HP = 480
BASE_SHOT_SPEED = 1350
DRAGON_SHOT_SPEED = BASE_SHOT_SPEED
DRAGON_SHOT_INTERVAL = 1 / 12
BOSS_HP = 800
PLAYER_SPEED = 310
GRAVITY = 1850
JUMP_SPEED = 680
SHOT_SPEED = BASE_SHOT_SPEED
SHOT_INTERVAL = 1 / 20
DASH_SPEED = 800
DASH_TIME = 0.21
DASH_COOLDOWN = 0.55
HURT_TIME = 1.8
TRANSFORM_TIME = 3.6

# Pimenta: tempo disponível separado do tempo do poder após coletar.
PEPPER_VISIBLE_TIME = 5.0
PEPPER_DURATION = 8.0
PEPPER_FIRST_SPAWN = 6.0
PEPPER_RESPAWN = 20.0
PEPPER_FIRE_RATE = 1.5
PEPPER_SHOT_SPEED = 1.25

# Mixagem: trilha abaixo dos efeitos; voz ocupa um canal separado.
MUSIC_VOLUME = 0.20
MUSIC_DURING_VOICE = 0.12
VOICE_VOLUME = 0.95
EFFECT_VOLUME = 0.40
SHOT_VOLUME = 0.08
HIT_VOLUME = 0.12


def clamp(value, minimum, maximum):
    """Mantém um valor dentro de um intervalo."""
    return max(minimum, min(maximum, value))
