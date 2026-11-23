"""Música, efeitos e vozes originais. Responsável: Davi."""
from pathlib import Path
import pygame
from config import (MUSIC_VOLUME, MUSIC_DURING_VOICE, VOICE_VOLUME, EFFECT_VOLUME,
                    SHOT_VOLUME, HIT_VOLUME)

MUSIC_CHANNEL = 0
VOICE_CHANNEL = 1


def _reserve_channels():
    """Reserva os canais de música e voz antes de reproduzir os efeitos."""
    if pygame.mixer.get_init():
        if pygame.mixer.get_num_channels() < 3:
            pygame.mixer.set_num_channels(8)
        # Sound.play() fica livre para usar os demais canais sem cortar vozes.
        pygame.mixer.set_reserved(2)


def load_sounds():
    """Carrega WAV antigos e substitui trilha/dano pelos OGG enviados."""
    sounds = {}
    if not pygame.mixer.get_init():
        return sounds
    _reserve_channels()
    root = Path(__file__).resolve().parent / 'assets'
    for filename in (root / 'sounds').glob('*.wav'):
        sound = pygame.mixer.Sound(str(filename))
        volumes = {'music': 1.0, 'shoot': SHOT_VOLUME, 'hit': HIT_VOLUME}
        sound.set_volume(volumes.get(filename.stem, EFFECT_VOLUME))
        sounds[filename.stem] = sound
    additions = {'music': 'tema_mineirinho.ogg', 'hurt': 'dano_ai.ogg',
                 'pimentinha': 'pimentinha.ogg'}
    for name, filename in additions.items():
        sound = pygame.mixer.Sound(str(root / 'audio' / filename))
        sound.set_volume(1.0)  # Canal aplica a mixagem de música/voz.
        sounds[name] = sound
    return sounds


def play_sound(assets, name):
    """Dano/coleta usam voz reservada; demais efeitos mantêm seus canais."""
    if not pygame.mixer.get_init() or assets['muted'] or name not in assets['sounds']:
        return
    _reserve_channels()
    if name in ('hurt', 'pimentinha'):
        voice = pygame.mixer.Channel(VOICE_CHANNEL)
        voice.set_volume(VOICE_VOLUME)
        if voice.get_busy():
            voice.queue(assets['sounds'][name])
        else:
            voice.play(assets['sounds'][name])
        update_volume(assets)
    else:
        assets['sounds'][name].play()


def start_music(assets):
    """Mesmo tema do menu nas três fases; não sobrepõe outra faixa."""
    if pygame.mixer.get_init() and 'music' in assets['sounds']:
        _reserve_channels()
        pygame.mixer.Channel(MUSIC_CHANNEL).play(assets['sounds']['music'], loops=-1, fade_ms=120)
        update_volume(assets)


def stop_voices(assets):
    """Limpa falas antigas ao reiniciar/trocar de fase ou voltar ao menu."""
    if pygame.mixer.get_init():
        pygame.mixer.Channel(VOICE_CHANNEL).stop()
        update_volume(assets)


def update_volume(assets):
    """Mantém trilha baixa e acompanha mute sem fazer vozes antigas voltarem."""
    if not pygame.mixer.get_init():
        return
    muted = bool(assets['muted'])
    music = pygame.mixer.Channel(MUSIC_CHANNEL)
    voice = pygame.mixer.Channel(VOICE_CHANNEL)
    if muted:
        # O menu tem seu próprio controle de música no mesmo canal zero.
        # Silencia o canal e interrompe somente efeitos/vozes pendentes.
        for index in range(1, pygame.mixer.get_num_channels()):
            pygame.mixer.Channel(index).stop()
    volume = MUSIC_DURING_VOICE if voice.get_busy() else MUSIC_VOLUME
    music.set_volume(0.0 if muted else volume)
    voice.set_volume(0.0 if muted else VOICE_VOLUME)
