"""Constantes do jogo. Moisés ajusta os valores de dificuldade aqui."""
WIDTH = 1280
HEIGHT = 720
FLOOR = 622
FPS = 60

LIVES = 3
BOSS_HP = 360
PLAYER_SPEED = 310
GRAVITY = 1850
JUMP_SPEED = 680
SHOT_SPEED = 1450
SHOT_INTERVAL = 1 / 12
DASH_SPEED = 800
DASH_TIME = 0.21
DASH_COOLDOWN = 0.55
HURT_TIME = 1.8
TRANSFORM_TIME = 3.6


def clamp(value, minimum, maximum):
    """Mantém um valor dentro de um intervalo."""
    return max(minimum, min(maximum, value))
