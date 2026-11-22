"""Carrega artes e escolhe quadros de animação. Responsável: Davi."""
import json
import math
from pathlib import Path
import pygame
from audio import load_sounds
from config import WIDTH, HEIGHT, clamp

ROOT = Path(__file__).resolve().parent


def load_image(filename, size):
    """Carrega uma imagem com transparência e ajusta o tamanho."""
    image = pygame.image.load(str(ROOT / filename)).convert_alpha()
    return pygame.transform.smoothscale(image, size)


def load_sheet(spec, size):
    """Separa os quadros de uma folha de sprites em uma lista."""
    sheet = pygame.image.load(str(ROOT / spec['url'])).convert_alpha()
    width = sheet.get_width() // spec['cols']
    height = sheet.get_height() // spec['rows']
    frames = []
    for index in range(spec['count']):
        x = index % spec['cols'] * width
        y = index // spec['cols'] * height
        frame = sheet.subsurface((x, y, width, height))
        frames.append(pygame.transform.smoothscale(frame, size))
    return frames


def load_assets():
    """Imagens e sons ficam prontos antes do loop, como no exemplo da aula."""
    with open(ROOT / 'assets' / 'manifest.json', encoding='utf-8') as file:
        manifest = json.load(file)
    assets = {'manifest': manifest, 'frames': {}, 'flipped': {}, 'muted': False, 'animated': {}}
    for name, spec in manifest['player']['actions'].items():
        frames = load_sheet(spec, (174, 174))
        assets['frames'][name] = frames
        assets['flipped'][name] = []
        for frame in frames:
            assets['flipped'][name].append(pygame.transform.flip(frame, True, False))
    for name, spec in manifest['dragon'].items():
        assets['frames'][name] = load_sheet(spec, (442, 442))
    for name in ('comilao-corpo', 'comilao-boca'):
        filename = 'comilao-corpo-animado' if name == 'comilao-corpo' else 'comilao-boca-animada'
        spec = {'url': 'assets/' + filename + '.png', 'cols': 4, 'rows': 3, 'count': 12}
        assets['frames'][name] = load_sheet(spec, (442, 442))
    assets['valley'] = load_image('assets/vale-comilao.png', (WIDTH, HEIGHT))
    assets['pyramid'] = load_image('assets/piramide-cenario.png', (WIDTH, HEIGHT))
    sheets = [('piramide-base', 4, 3, 12, (500, 500)),
              ('piramide-olho-esquerdo', 3, 2, 6, (300, 480)),
              ('piramide-olho-direito', 3, 2, 6, (300, 480)),
              ('servo-serpente', 3, 2, 6, (80, 110)),
              ('servo-morcego', 3, 2, 6, (112, 100))]
    for name, cols, rows, count, size in sheets:
        spec = {'url': 'assets/' + name + '.png', 'cols': cols, 'rows': rows, 'count': count}
        assets['frames'][name] = load_sheet(spec, size)
    assets['day'] = load_image(manifest['background']['day'], (WIDTH, HEIGHT))
    assets['night'] = load_image(manifest['background']['night'], (WIDTH, HEIGHT))
    assets['bread'] = load_image(manifest['bread']['url'], (22, 22))
    assets['sounds'] = load_sounds()
    assets['fire_images'] = {}
    return assets


def player_pose(player):
    """Escolhe uma ação e o índice do quadro usando if/elif."""
    p = player
    if p.dash > 0:
        if p.dash > .09:
            return '06_dash', 1
        return '06_dash', 2
    if p.shooting and p.aim_y < 0:
        if p.aim_x != 0:
            return '09_atirar_diagonal', int(p.anim_time * 19) % 4
        return '05_atirar_cima', int(p.anim_time * 19) % 4
    if p.crouch:
        if p.shooting:
            return '08_pular_atirar', 1
        return '06_dash', 0
    if not p.on_ground:
        action = '03_pulo'
        if p.shooting:
            action = '08_pular_atirar'
        if p.jump_age < .09:
            frame = 2
        elif p.vy < -200:
            frame = 3
        elif abs(p.vy) <= 200:
            frame = 4
        else:
            frame = 5
        return action, frame
    if p.land_time > 0:
        action = '03_pulo'
        if p.shooting:
            action = '08_pular_atirar'
        if p.land_time > .08:
            return action, 6
        return action, 7
    if abs(p.vx) > 38:
        if p.shooting:
            return '07_correr_atirar', int(p.anim_time * 14) % 8
        return '02_corrida', int(p.anim_time * 14) % 8
    if p.shooting:
        return '04_atirar_frente', int(p.anim_time * 19) % 4
    time = p.anim_time % 3.3
    if time < 2.75:
        return '01_parado', 0
    if time < 2.9:
        return '01_parado', 1
    if time < 3.05:
        return '01_parado', 2
    return '01_parado', 3


def fire_image(assets, radius, angle):
    """Desenha a bola de fogo e guarda a imagem para reutilizar."""
    direction = round(math.degrees(angle) / 15) * 15
    key = radius, direction
    if key not in assets['fire_images']:
        r = int(radius)
        image = pygame.Surface((r * 5, r * 3), pygame.SRCALPHA)
        center = (r * 3, r * 1.5)
        pygame.draw.polygon(image, (49, 30, 28), [(r * 3, r * .6), (0, r * 1.5), (r * 3, r * 2.4)])
        pygame.draw.polygon(image, (237, 102, 41), [(r * 3, r * .8), (r * .2, r * 1.5), (r * 3, r * 2.2)])
        pygame.draw.circle(image, (49, 30, 28), center, r + 2)
        pygame.draw.circle(image, (246, 138, 44), center, r)
        pygame.draw.circle(image, (255, 204, 85), center, max(1, round(r * .75)))
        pygame.draw.circle(image, (255, 240, 181), center, max(1, round(r * .4)))
        # A bola fica centralizada no sprite; a cauda se estende para trás.
        centered = pygame.Surface((r * 7, r * 7), pygame.SRCALPHA)
        centered.blit(image, (r * .5, r * 2))
        assets['fire_images'][key] = pygame.transform.rotate(centered, -direction)
    return assets['fire_images'][key]


def flame_image(beam):
    """Cria a imagem do sopro entre a boca e o ponto avisado na arena."""
    start = pygame.Vector2(beam.x, beam.y)
    delta = pygame.Vector2(beam.end_x, beam.end_y) - start
    normal = pygame.Vector2(-delta.y, delta.x).normalize()
    opening = clamp(beam.age / .075, 0, 1)
    closing = clamp((beam.duration - beam.age) / .09, 0, 1)
    bounds = pygame.Rect(min(beam.x, beam.end_x) - 45, min(beam.y, beam.end_y) - 45,
                         abs(delta.x) + 90, abs(delta.y) + 90)
    bounds = bounds.clip(pygame.Rect(0, 0, WIDTH, HEIGHT))
    image = pygame.Surface(bounds.size, pygame.SRCALPHA)
    for factor, color in ((1.08, (49, 30, 28)), (1, (237, 102, 41)), (.66, (255, 187, 67)), (.29, (255, 240, 174))):
        upper = []
        lower = []
        for index in range(26):
            part = index / 25
            width = (8 + beam.half_width * 1.1 * part) * factor * closing
            wave = math.sin(part * 29 - beam.age * 25) * width * .17
            position = start + delta * part * opening - pygame.Vector2(bounds.topleft)
            upper.append(position + normal * (width + wave))
            lower.append(position - normal * (width - wave))
        pygame.draw.polygon(image, color, upper + list(reversed(lower)))
    return image, bounds
