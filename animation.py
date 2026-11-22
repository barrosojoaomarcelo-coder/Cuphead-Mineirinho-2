"""Poses elásticas reaproveitadas, sem alterar as caixas de colisão. Frente: Davi."""
import pygame

# Repouso, compressão, preparação, disparo e recuperação.
SCALES = ((1, 1), (1.05, .96), (.96, 1.04), (1.08, .94), (.95, 1.04))


def animated_frame(assets, name, index, pose=0, flipped=False, pivot=None, bright=False):
    """Guarda as imagens transformadas; evita redimensioná-las a cada quadro."""
    key = name, index, pose, flipped, pivot, bright
    cache = assets['animated']
    if key not in cache:
        frames = assets['flipped'] if flipped else assets['frames']
        source = frames[name][index]
        width, height = source.get_size()
        if pivot is None:
            pivot = width / 2, height - 12
        sx, sy = SCALES[pose]
        resized = pygame.transform.smoothscale(source, (round(width * sx), round(height * sy)))
        image = pygame.Surface(source.get_size(), pygame.SRCALPHA)
        image.blit(resized, (round(pivot[0] * (1 - sx)), round(pivot[1] * (1 - sy))))
        if bright:
            image.fill((55, 45, 20, 0), special_flags=pygame.BLEND_RGBA_ADD)
        if len(cache) >= 256:
            cache.pop(next(iter(cache)))
        cache[key] = image
    return cache[key]
