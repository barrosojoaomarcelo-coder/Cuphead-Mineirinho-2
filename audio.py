"""Carregamento e reprodução de WAV, como no handout. Responsável: Davi."""
from pathlib import Path
import pygame


def load_sounds():
    """Carrega os sons uma vez. Sem dispositivo de áudio, retorna vazio."""
    sounds = {}
    if not pygame.mixer.get_init():
        return sounds
    folder = Path(__file__).resolve().parent / 'assets' / 'sounds'
    for filename in folder.glob('*.wav'):
        sound = pygame.mixer.Sound(str(filename))
        sound.set_volume(0.28)
        if filename.stem == 'music':
            sound.set_volume(1)
        sounds[filename.stem] = sound
    return sounds


def play_sound(assets, name):
    """Toca um efeito, se o som estiver ativado."""
    if not assets['muted'] and name in assets['sounds']:
        assets['sounds'][name].play()


def start_music(assets):
    """A trilha usa uma faixa reservada para não ser cortada pelos tiros."""
    if 'music' in assets['sounds']:
        channel = pygame.mixer.Channel(0)
        channel.play(assets['sounds']['music'], loops=-1)
        update_volume(assets)


def update_volume(assets):
    """Aplica a preferência de som à trilha e aos efeitos."""
    if pygame.mixer.get_init():
        if assets['muted']:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()
        pygame.mixer.Channel(0).set_volume(0.18)
