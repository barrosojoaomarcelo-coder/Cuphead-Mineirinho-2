"""Janela, eventos e telas. Responsável: João Marcelo.

Leia game_screen primeiro: é o loop de inicialização/eventos/atualização/desenho.
"""
import argparse
import json
import math
import os
from pathlib import Path
import pygame
from config import WIDTH, HEIGHT, FPS
from assets import load_assets
from audio import start_music, update_volume
from engine import GameModel
from scene import Renderer

RULESET = 'tres-chefes-20tiros-2026-11'


def save_folder():
    """Dados pessoais ficam fora da pasta do código."""
    if 'FORNALHA_SAVE_DIR' in os.environ:
        return Path(os.environ['FORNALHA_SAVE_DIR'])
    if os.name == 'nt':
        return Path(os.environ.get('LOCALAPPDATA', Path.home())) / 'FornalhaDoCastelo'
    return Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share')) / 'FornalhaDoCastelo'


def load_preferences(filename):
    """Arquivo inexistente ou inválido começa com as preferências padrão."""
    try:
        with open(filename, encoding='utf-8') as file:
            data = json.load(file)
        best = data.get('best')
        if data.get('ruleset') != RULESET:
            best = None  # O recorde antigo não compara lutas com regras diferentes.
        if type(best) not in (int, float) or not math.isfinite(best) or best <= 0:
            best = None
        return best, data.get('muted') is True
    except (OSError, ValueError, AttributeError):
        return None, False


def save_preferences(ui):
    try:
        filename = ui['save_file']
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump({'best': ui['best'], 'muted': ui['assets']['muted'], 'ruleset': RULESET}, file)
    except OSError:
        pass  # Ainda é possível jogar sem gravar o recorde.


def initialize(size=(1152, 648), save_dir=None, muted=False):
    """Inicializa Pygame, carrega assets e cria a primeira tela."""
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.init()
    window = pygame.display.set_mode(size, pygame.RESIZABLE)
    pygame.display.set_caption('A Fornalha do Castelo | Davi, Moisés e João Marcelo')
    if pygame.mixer.get_init():
        pygame.mixer.set_num_channels(24)
        pygame.mixer.set_reserved(1)
    folder = save_folder()
    if save_dir is not None:
        folder = Path(save_dir)
    filename = folder / 'preferences.json'
    best, saved_mute = load_preferences(filename)
    assets = load_assets()
    assets['muted'] = muted or saved_mute
    ui = {'window': window, 'windowed_size': size, 'fullscreen': False,
          'canvas': pygame.Surface((WIDTH, HEIGHT)).convert(),
          'clock': pygame.time.Clock(), 'running': True, 'instructions': False,
          'resume_after_help': False, 'buttons': {}, 'viewport': window.get_rect(),
          'assets': assets, 'game': GameModel(assets), 'renderer': Renderer(assets),
          'best': best, 'save_file': filename}
    start_music(assets)
    return ui


def toggle_fullscreen(ui):
    ui['fullscreen'] = not ui['fullscreen']
    if ui['fullscreen']:
        ui['windowed_size'] = ui['window'].get_size()
        ui['window'] = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        ui['window'] = pygame.display.set_mode(ui['windowed_size'], pygame.RESIZABLE)


def toggle_help(ui):
    game = ui['game']
    if ui['instructions']:
        ui['instructions'] = False
        if ui['resume_after_help']:
            game.resume()
        ui['resume_after_help'] = False
    else:
        ui['resume_after_help'] = game.state in ('playing', 'intro', 'transform')
        game.pause()
        ui['instructions'] = True


def button_action(ui, name):
    """Mouse e teclado chamam as mesmas ações."""
    game = ui['game']
    if name == 'sound':
        ui['assets']['muted'] = not ui['assets']['muted']
        update_volume(ui['assets'])
        save_preferences(ui)
    elif name in ('instructions', 'back'):
        toggle_help(ui)
    elif name == 'play':
        if game.state == 'paused':
            game.resume()
        elif game.state == 'title':
            game.start_story()
        elif game.state == 'story':
            game.start()
        elif game.state == 'victory':
            if not game.next_stage():
                game.reset()
        elif game.state == 'dead':
            game.start(game.stage_index)
        else:
            return
        ui['renderer'].particles.clear()
    elif name == 'practice':
        game.start(1)
        ui['renderer'].particles.clear()
    elif name == 'practice3':
        game.start(2)
        ui['renderer'].particles.clear()
    elif name == 'menu':
        game.reset()
        ui['renderer'].particles.clear()


def handle_key(ui, key):
    """Teclas de menu são eventos; movimento contínuo é lido em read_controls."""
    game = ui['game']
    if key == pygame.K_F11:
        toggle_fullscreen(ui)
    elif key == pygame.K_m:
        button_action(ui, 'sound')
    elif key == pygame.K_h:
        toggle_help(ui)
    elif ui['instructions']:
        if key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER):
            toggle_help(ui)
    elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
        if game.state in ('title', 'story', 'dead', 'victory', 'paused'):
            button_action(ui, 'play')
    elif key in (pygame.K_ESCAPE, pygame.K_p):
        if game.state == 'paused':
            game.resume()
        elif game.state in ('story', 'dead', 'victory'):
            if key == pygame.K_ESCAPE:
                button_action(ui, 'menu')
        elif game.state == 'title':
            if key == pygame.K_ESCAPE:
                ui['running'] = False
        else:
            game.pause()
    elif key == pygame.K_r and game.state != 'title':
        game.start(game.stage_index)
        ui['renderer'].particles.clear()


def handle_event(ui, event):
    if event.type == pygame.QUIT:
        ui['running'] = False
    elif event.type == pygame.WINDOWFOCUSLOST:
        ui['game'].pause()
    elif event.type == pygame.VIDEORESIZE and not ui['fullscreen']:
        size = max(640, event.w), max(360, event.h)
        ui['windowed_size'] = size
        ui['window'] = pygame.display.set_mode(size, pygame.RESIZABLE)
    elif event.type == pygame.KEYDOWN:
        handle_key(ui, event.key)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        viewport = ui['viewport']
        if viewport.collidepoint(event.pos):
            x = (event.pos[0] - viewport.x) * WIDTH / viewport.w
            y = (event.pos[1] - viewport.y) * HEIGHT / viewport.h
            for name, rect in ui['buttons'].items():
                if rect.collidepoint(x, y):
                    button_action(ui, name)
                    break


def read_controls():
    """Dicionário simples de teclas pressionadas neste quadro."""
    keys = pygame.key.get_pressed()
    return {'left': keys[pygame.K_a] or keys[pygame.K_LEFT],
            'right': keys[pygame.K_d] or keys[pygame.K_RIGHT],
            'up': keys[pygame.K_w] or keys[pygame.K_UP],
            'down': keys[pygame.K_s] or keys[pygame.K_DOWN],
            'jump': keys[pygame.K_SPACE] or keys[pygame.K_z],
            'shoot': keys[pygame.K_j] or keys[pygame.K_x],
            'dash': keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_k]}


def update_game(ui, dt, controls):
    game = ui['game']
    game.step(dt, controls)
    ui['renderer'].update(dt, game)
    if game.state == 'victory' and game.stage_index == 0:
        if ui['best'] is None or game.elapsed < ui['best']:
            ui['best'] = game.elapsed
            save_preferences(ui)


def draw_screen(ui):
    """Desenha na arena e depois ajusta a imagem ao tamanho da janela."""
    assets = ui['assets']
    buttons = ui['renderer'].draw(ui['canvas'], ui['game'], assets['muted'],
                                  ui['best'], ui['instructions'], bool(assets['sounds']))
    if ui['instructions']:
        for name in list(buttons):
            if name not in ('back', 'sound'):
                del buttons[name]
    ui['buttons'] = buttons
    width, height = ui['window'].get_size()
    scale = min(width / WIDTH, height / HEIGHT)
    size = max(1, round(WIDTH * scale)), max(1, round(HEIGHT * scale))
    viewport = pygame.Rect((width - size[0]) // 2, (height - size[1]) // 2, *size)
    ui['viewport'] = viewport
    ui['window'].fill((24, 17, 19))
    image = pygame.transform.smoothscale(ui['canvas'], size)
    ui['window'].blit(image, viewport)
    pygame.display.flip()


def game_screen(ui, max_frames=None, screenshot=None):
    """Loop principal: relógio, eventos, atualização e desenho, nessa ordem."""
    frames = 0
    while ui['running']:
        dt = ui['clock'].tick(FPS) / 1000
        for event in pygame.event.get():
            handle_event(ui, event)
        controls = read_controls()
        update_game(ui, dt, controls)
        draw_screen(ui)
        frames += 1
        if max_frames is not None and frames >= max_frames:
            break
    if screenshot is not None:
        pygame.image.save(ui['canvas'], str(screenshot))


def main():
    parser = argparse.ArgumentParser(description='A Fornalha do Castelo — versão da aula')
    parser.add_argument('--mute', action='store_true')
    parser.add_argument('--frames', type=int, help='encerrar após N quadros para testar')
    parser.add_argument('--screenshot', type=Path)
    parser.add_argument('--stage', type=int, choices=(1, 2, 3), help='abrir uma fase diretamente')
    args = parser.parse_args()
    if args.frames is not None and args.frames < 1:
        parser.error('--frames deve ser maior que zero')
    try:
        ui = initialize(muted=args.mute)
        if args.stage is not None:
            ui['game'].start(args.stage - 1)
        game_screen(ui, args.frames, args.screenshot)
    except (pygame.error, FileNotFoundError) as error:
        print('Não foi possível iniciar:', error)
        print('Extraia o ZIP inteiro e instale requirements.txt com Python 3.12.')
        return 1
    finally:
        pygame.quit()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
