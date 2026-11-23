"""Janela, eventos e telas. Responsável: João Marcelo.

Leia game_screen primeiro: é o loop de inicialização/eventos/atualização/desenho.
"""
import argparse
import json
import math
import os
from pathlib import Path
import pygame
from config import WIDTH, HEIGHT, FPS, STAGE_ORDER, GAME_TITLE
from assets import load_assets
from audio import start_music, update_volume, stop_voices
from engine import GameModel
from scene import Renderer
from tela_inicial import TelaInicial
from controle import ControleJoystick

RULESET = 'mineirinho-1350-pir-com-dra-2026-11'

# Posições no menu -> índices físicos do GameModel existente.
# O motor mantém 0=Dragão, 1=Comilão e 2=Pirâmide.
ORDEM_CHEFES = STAGE_ORDER


def save_folder():
    """Dados pessoais ficam fora da pasta do código."""
    if 'MINEIRINHO_SAVE_DIR' in os.environ:
        return Path(os.environ['MINEIRINHO_SAVE_DIR'])
    # Compatibilidade com quem já configurou a pasta na edição anterior.
    if 'FORNALHA_SAVE_DIR' in os.environ:
        return Path(os.environ['FORNALHA_SAVE_DIR'])
    if os.name == 'nt':
        return Path(os.environ.get('LOCALAPPDATA', Path.home())) / GAME_TITLE
    return Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share')) / GAME_TITLE


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
    pygame.display.set_caption(GAME_TITLE)
    if pygame.mixer.get_init():
        pygame.mixer.set_num_channels(24)
        pygame.mixer.set_reserved(2)
    folder = save_folder()
    if save_dir is not None:
        folder = Path(save_dir)
    filename = folder / 'preferences.json'
    preference_source = filename
    if save_dir is None and folder.name == GAME_TITLE and not filename.exists():
        legacy = folder.with_name('FornalhaDoCastelo') / 'preferences.json'
        if legacy.is_file():
            preference_source = legacy
    best, saved_mute = load_preferences(preference_source)
    assets = load_assets()
    assets['muted'] = muted or saved_mute
    ui = {'window': window, 'windowed_size': size, 'fullscreen': False,
          'canvas': pygame.Surface((WIDTH, HEIGHT)).convert(),
          'clock': pygame.time.Clock(), 'running': True, 'instructions': False,
          'resume_after_help': False, 'buttons': {}, 'viewport': window.get_rect(),
          'assets': assets, 'game': GameModel(assets), 'renderer': Renderer(assets),
          'best': best, 'save_file': filename}
    # O menu usa a gravação enviada; a música da luta começa só ao jogar.
    ui['title_menu'] = TelaInicial(som=not assets['muted'])
    ui['title_menu_active'] = False
    ui['joystick'] = ControleJoystick()
    sync_title_menu(ui)
    return ui


def sync_title_menu(ui):
    """Troca áudio uma única vez por entrada/saída da tela inicial."""
    menu = ui['title_menu']
    wanted = ui['game'].state == 'title'
    if wanted and not ui['title_menu_active']:
        if pygame.mixer.get_init():
            pygame.mixer.stop()
            pygame.mixer.music.pause()
        menu.encerrado = False
        menu.som = not ui['assets']['muted']
        menu.ativar_audio()
        ui['title_menu_active'] = True
    elif not wanted and ui['title_menu_active']:
        menu.parar_audio()
        # O áudio original reserva o canal zero para a trilha.
        if pygame.mixer.get_init():
            pygame.mixer.set_reserved(2)
        start_music(ui['assets'])
        ui['title_menu_active'] = False


def start_selected_stage(ui, number):
    """Menu 1/2/3 -> Pirâmide(2), Comilão(1), Dragão(0)."""
    if number not in (1, 2, 3):
        raise ValueError('A fase deve ser 1, 2 ou 3.')
    ui['instructions'] = False
    ui['resume_after_help'] = False
    stop_voices(ui['assets'])
    ui['game'].start(ORDEM_CHEFES[number - 1])
    ui['renderer'].particles.clear()
    ui['buttons'].clear()
    sync_title_menu(ui)


def start_campaign(ui):
    """Começa a aventura com a introdução antes da Pirâmide."""
    stop_voices(ui['assets'])
    ui['instructions'] = False
    ui['resume_after_help'] = False
    ui['game'].start_story()
    ui['renderer'].particles.clear()
    ui['buttons'].clear()
    sync_title_menu(ui)


def next_stage_in_order(ui):
    """Depois da vitória: Pirâmide -> Comilão -> Dragão -> menu."""
    position = ORDEM_CHEFES.index(ui['game'].stage_index)
    if position + 1 >= len(ORDEM_CHEFES):
        return False
    start_selected_stage(ui, position + 2)
    return True


def logical_mouse_position(ui, position):
    """Converte o mouse da janela para a arena, ignorando as margens."""
    width, height = ui['window'].get_size()
    scale = min(width / WIDTH, height / HEIGHT)
    size = max(1, round(WIDTH * scale)), max(1, round(HEIGHT * scale))
    viewport = pygame.Rect((width - size[0]) // 2, (height - size[1]) // 2, *size)
    if not viewport.collidepoint(position):
        return None
    return ((position[0] - viewport.x) * WIDTH / viewport.w,
            (position[1] - viewport.y) * HEIGHT / viewport.h)


def handle_title_event(ui, event):
    """Encaminha cliques/teclas ao menu e confirma a fase escolhida."""
    menu = ui['title_menu']
    point = None
    if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
        point = logical_mouse_position(ui, event.pos)
        if point is None:
            return
    if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
        toggle_help(ui)
        return
    chosen = menu.handle_event(event, posicao_logica=point)
    # M e o botão de som continuam usando a preferência do jogo.
    muted = not menu.som
    if muted != ui['assets']['muted']:
        ui['assets']['muted'] = muted
        save_preferences(ui)
    if menu.encerrado:
        ui['running'] = False
    elif chosen is not None:
        if chosen == 1:
            start_campaign(ui)
        else:
            start_selected_stage(ui, chosen)


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
        pause_game(ui)
        ui['instructions'] = True


def pause_game(ui):
    previous = ui['game'].state
    ui['game'].pause()
    if previous != 'paused' and ui['game'].state == 'paused':
        ui['renderer'].pause_menu.reset()


def restart_stage(ui):
    stop_voices(ui['assets'])
    ui['instructions'] = False
    ui['resume_after_help'] = False
    ui['game'].start(ui['game'].stage_index)
    ui['renderer'].particles.clear()
    ui['renderer'].pause_menu.reset()
    sync_title_menu(ui)


def button_action(ui, name):
    """Mouse e teclado chamam as mesmas ações."""
    game = ui['game']
    if name == 'sound':
        ui['assets']['muted'] = not ui['assets']['muted']
        update_volume(ui['assets'])
        if ui['game'].state == 'title':
            menu = ui['title_menu']
            menu.som = not ui['assets']['muted']
            if menu.som:
                menu.ativar_audio()
            else:
                menu.parar_audio()
        save_preferences(ui)
    elif name == 'retornar':
        game.resume()
    elif name == 'reiniciar':
        restart_stage(ui)
    elif name in ('instructions', 'back', 'como_jogar'):
        toggle_help(ui)
    elif name == 'play':
        if game.state == 'paused':
            game.resume()
        elif game.state == 'title':
            start_campaign(ui)
        elif game.state == 'story':
            start_selected_stage(ui, 1)
        elif game.state == 'victory':
            if not next_stage_in_order(ui):
                stop_voices(ui['assets'])
                game.reset()
                ui['title_menu'].selecionado = 0
                ui['title_menu'].foco = -1
        elif game.state == 'dead':
            restart_stage(ui)
        else:
            return
        ui['renderer'].particles.clear()
    elif name == 'practice':
        start_selected_stage(ui, 2)
        ui['renderer'].particles.clear()
    elif name == 'practice3':
        start_selected_stage(ui, 3)
        ui['renderer'].particles.clear()
    elif name == 'menu':
        stop_voices(ui['assets'])
        game.reset()
        ui['instructions'] = False
        ui['resume_after_help'] = False
        ui['renderer'].particles.clear()
    sync_title_menu(ui)


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
    elif game.state == 'paused':
        if key == pygame.K_r:
            button_action(ui, 'reiniciar')
        else:
            action = ui['renderer'].pause_menu.handle_event(pygame.event.Event(pygame.KEYDOWN, key=key, mod=pygame.key.get_mods()))
            if action:
                button_action(ui, action)
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
            pause_game(ui)
    elif key == pygame.K_r and game.state != 'title':
        restart_stage(ui)


def handle_event(ui, event):
    controle = ui['joystick']
    em_menu = ui['instructions'] or ui['game'].state in ('title', 'story', 'paused', 'dead', 'victory')
    teclas = controle.handle_event(event, menu=em_menu,
                                  paused=ui['game'].state == 'paused' and not ui['instructions'])
    if controle.desconectou:
        pause_game(ui)
    for tecla in teclas:
        if ui['game'].state == 'title' and not ui['instructions']:
            handle_title_event(ui, pygame.event.Event(pygame.KEYDOWN, key=tecla))
        else:
            handle_key(ui, tecla)
    if event.type == pygame.QUIT:
        ui['running'] = False
    elif event.type == pygame.WINDOWFOCUSLOST:
        pause_game(ui)
        if ui['title_menu_active']:
            ui['title_menu'].handle_event(event)
    elif event.type == pygame.WINDOWFOCUSGAINED:
        if ui['title_menu_active']:
            ui['title_menu'].handle_event(event)
    elif event.type == pygame.VIDEORESIZE and not ui['fullscreen']:
        size = max(640, event.w), max(360, event.h)
        ui['windowed_size'] = size
        ui['window'] = pygame.display.set_mode(size, pygame.RESIZABLE)
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
        toggle_fullscreen(ui)
    elif ui['game'].state == 'title' and not ui['instructions']:
        handle_title_event(ui, event)
    elif (ui['game'].state == 'paused' and not ui['instructions']
          and event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN)):
        point = logical_mouse_position(ui, event.pos)
        if point is None:
            return
        action = ui['renderer'].pause_menu.handle_event(event, posicao_logica=point)
        if action:
            button_action(ui, action)
    elif event.type == pygame.KEYDOWN:
        handle_key(ui, event.key)
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        point = logical_mouse_position(ui, event.pos)
        if point is not None:
            for name, rect in ui['buttons'].items():
                if rect.collidepoint(point):
                    button_action(ui, name)
                    break


def read_controls(ui=None):
    """Dicionário simples de teclas pressionadas neste quadro."""
    keys = pygame.key.get_pressed()
    controls = {'left': keys[pygame.K_a] or keys[pygame.K_LEFT],
            'right': keys[pygame.K_d] or keys[pygame.K_RIGHT],
            'up': keys[pygame.K_w] or keys[pygame.K_UP],
            'down': keys[pygame.K_s] or keys[pygame.K_DOWN],
            'jump': keys[pygame.K_SPACE] or keys[pygame.K_z],
            'shoot': keys[pygame.K_j] or keys[pygame.K_x],
            'dash': keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_k]}
    if ui is not None:
        for action, pressed in ui['joystick'].read_controls().items():
            controls[action] = bool(controls.get(action, False) or pressed)
    return controls


def update_game(ui, dt, controls):
    sync_title_menu(ui)
    game = ui['game']
    if game.state == 'title':
        ui['title_menu'].update(dt)
        return
    game.step(dt, controls)
    ui['renderer'].update(dt, game)
    sync_title_menu(ui)
    if game.state != 'title':
        update_volume(ui['assets'])
    if game.state == 'victory' and game.stage_index == 0:
        if ui['best'] is None or game.elapsed < ui['best']:
            ui['best'] = game.elapsed
            save_preferences(ui)


def draw_screen(ui):
    """Desenha na arena e depois ajusta a imagem ao tamanho da janela."""
    assets = ui['assets']
    if ui['game'].state == 'title' and not ui['instructions']:
        ui['title_menu'].draw(ui['canvas'])
        buttons = {}
    else:
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
            # Fechar a janela interrompe o lote antes de atualizar/desenhar.
            if not ui['running']:
                break
        if not ui['running']:
            break
        controls = read_controls(ui)
        if ui['joystick'].desconectou:
            pause_game(ui)
        update_game(ui, dt, controls)
        draw_screen(ui)
        frames += 1
        if max_frames is not None and frames >= max_frames:
            break
    if screenshot is not None:
        pygame.image.save(ui['canvas'], str(screenshot))


def main():
    parser = argparse.ArgumentParser(description=f'{GAME_TITLE} — jogo em Pygame')
    parser.add_argument('--mute', action='store_true')
    parser.add_argument('--frames', type=int, help='encerrar após N quadros para testar')
    parser.add_argument('--screenshot', type=Path)
    parser.add_argument('--stage', type=int, choices=(1, 2, 3), help='abrir diretamente: 1=Pirâmide, 2=Comilão, 3=Dragão')
    args = parser.parse_args()
    if args.frames is not None and args.frames < 1:
        parser.error('--frames deve ser maior que zero')
    try:
        ui = initialize(muted=args.mute)
        if args.stage is not None:
            start_selected_stage(ui, args.stage)
        game_screen(ui, args.frames, args.screenshot)
    except (pygame.error, FileNotFoundError) as error:
        print('Não foi possível iniciar:', error)
        print('Extraia o ZIP inteiro e instale requirements.txt com Python 3.12.')
        return 1
    finally:
        if 'ui' in locals():
            ui['joystick'].fechar()
        pygame.quit()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
