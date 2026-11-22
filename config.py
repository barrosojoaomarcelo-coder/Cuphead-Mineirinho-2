"""Constantes do jogo. Moisés ajusta os valores de dificuldade aqui."""
WIDTH = 1280
HEIGHT = 720
FLOOR = 622
FPS = 60

LIVES = 3
# 800 acertos a 20 tiros/s preservam os 40 s de fogo da versão difícil
# anterior (480 a 12/s), sem perder a resposta rápida do pão de queijo.
BOSS_HP = 800
PLAYER_SPEED = 310
GRAVITY = 1850
JUMP_SPEED = 680
SHOT_SPEED = 1800
SHOT_INTERVAL = 1 / 20
DASH_SPEED = 800
DASH_TIME = 0.21
DASH_COOLDOWN = 0.55
HURT_TIME = 1.8
TRANSFORM_TIME = 3.6


def clamp(value, minimum, maximum):
    """Mantém um valor dentro de um intervalo."""
    return max(minimum, min(maximum, value))
