"""Estados, grupos e regras da luta. Responsável: Moisés.

A atualização segue a aula: mover sprites, verificar colisões e atualizar estado.
"""
import math
import pygame
import config as c
from sprites import Player, Boss, hitboxes_overlap
from audio import play_sound
from attacks import update_attacks
from comilao import Comilao, update_comilao
from piramide import Piramide, PyramidSide
from piramide_attacks import update_piramide

STAGES = ('Dragão Vermelho', 'Chefe Comilão', 'Olho da Pirâmide')


class GameModel:
    """Coordena os grupos; cada objeto móvel é um pygame.sprite.Sprite."""

    def __init__(self, assets):
        self.assets = assets
        self.reset()

    def reset(self, stage_index=0):
        """Cria uma partida limpa e devolve o jogo ao menu."""
        self.state = 'title'
        self.stage_index = stage_index
        self.previous_state = 'playing'
        self.elapsed = 0
        self.state_time = 0
        self.night = 0
        self.pattern_index = 0
        self.breath_count = 0
        self.horizontal_count = 0
        self.attack_timer = .85
        self.warnings = []
        self.scheduled = []
        self.stats = {'shots': 0, 'hits': 0, 'dashes': 0}
        self.player = Player(self.assets)
        self.boss = Boss(self.assets)
        if stage_index == 1:
            self.boss = Comilao(self.assets)
        elif stage_index == 2:
            self.boss = Piramide(self.assets)
        self.player_group = pygame.sprite.Group(self.player)
        self.boss_group = pygame.sprite.Group(self.boss)
        if stage_index == 2:
            self.boss_group.add(PyramidSide(self.boss))
        self.shots = pygame.sprite.Group()
        self.fire = pygame.sprite.Group()
        self.beams = pygame.sprite.Group()
        self.minions = pygame.sprite.Group()

    def start(self, stage_index=0):
        """Enter começa uma nova partida com uma breve apresentação."""
        if stage_index not in range(len(STAGES)):
            return False
        self.reset(stage_index)
        self.state = 'intro'
        play_sound(self.assets, 'start')
        return True

    def start_story(self):
        self.reset()
        self.state = 'story'

    def next_stage(self):
        """Avança após vencer; o terceiro chefe encerra a aventura."""
        if self.state == 'victory' and self.stage_index + 1 < len(STAGES):
            return self.start(self.stage_index + 1)
        return False

    def pause(self):
        if self.state in ('playing', 'intro', 'transform'):
            self.previous_state = self.state
            self.state = 'paused'
            self.player.jump_buffer = 0

    def resume(self):
        if self.state == 'paused':
            self.state = self.previous_state
            self.player.previous_input = {}

    def step(self, dt, controls):
        """Uma atualização por quadro; dt é o tempo em segundos de Clock.tick."""
        if not math.isfinite(dt) or dt <= 0:
            return
        if self.state in ('title', 'story', 'paused', 'dead', 'victory'):
            return
        dt = min(dt, .05)  # Evita um salto grande após uma travada da janela.
        self.state_time += dt
        if self.state == 'intro':
            if self.state_time >= 1.7:
                self.state = 'playing'
                self.state_time = 0
            return
        self.elapsed += dt
        if self.state == 'transform':
            self.update_transformation(dt, controls)
            return
        limit = 920
        if self.boss.phase >= 3:
            limit = 860
        if self.stage_index == 1:
            limit = 850
        left_limit = 53
        if self.stage_index == 2:
            limit = 930
            if self.boss.phase >= 3:
                left_limit, limit = 195, 1085
        self.player_group.update(dt, controls, True, limit, left_limit)
        self.boss_group.update(dt, self.elapsed, self.state)
        self.player_actions()
        if self.stage_index == 2:
            update_piramide(self, dt)
        elif self.stage_index == 1:
            update_comilao(self, dt)
        else:
            update_attacks(self, dt)
        self.shots.update(dt)
        self.fire.update(dt)
        self.beams.update(dt)
        self.minions.update(dt)
        self.check_collisions()
        self.refresh_boss()

    def player_actions(self):
        """Os sons são chamados diretamente, sem uma fila interna de eventos."""
        p = self.player
        if p.jumped:
            play_sound(self.assets, 'jump')
        if p.landed:
            play_sound(self.assets, 'land')
        if p.dashed:
            self.stats['dashes'] += 1
            play_sound(self.assets, 'dash')
        if p.shooting and p.shot_cooldown <= .000001:
            self.shots.add(p.shoot())
            p.shot_cooldown += c.SHOT_INTERVAL
            self.stats['shots'] += 1
            play_sound(self.assets, 'shoot')

    def refresh_boss(self):
        """O desenho do dragão acompanha o aviso e o ataque atuais."""
        self.boss.warning = None
        for warning in self.warnings:
            if not warning['fired']:
                self.boss.warning = warning
                break
        self.boss.breathing = bool(self.beams)
        if self.boss.warning is None and not self.beams and self.boss.cast <= 0:
            self.boss.mouth_lock = None
            self.boss.charge = 0
        self.boss.refresh_image(self.elapsed, self.state)

    def check_collisions(self):
        """Usa groupcollide e spritecollide com caixas de colisão menores."""
        hits = pygame.sprite.groupcollide(self.boss_group, self.shots, False, True, hitboxes_overlap)
        for boss, shots in hits.items():
            for shot in shots:
                if self.state != 'playing':
                    break
                self.stats['hits'] += 1
                self.damage_boss(1)
            play_sound(self.assets, 'hit')
        if self.state != 'playing':
            return
        minion_hits = pygame.sprite.groupcollide(self.minions, self.shots, False, True, hitboxes_overlap)
        for servant, shots in minion_hits.items():
            servant.hp -= len(shots)
            if servant.hp <= 0:
                servant.kill()
            play_sound(self.assets, 'hit')
        if pygame.sprite.spritecollide(self.player, self.minions, True, hitboxes_overlap):
            self.hurt_player()
        hits = pygame.sprite.spritecollide(self.player, self.fire, True, hitboxes_overlap)
        if len(hits) > 0:
            self.hurt_player()
        for beam in self.beams:
            if beam.touches(self.player):
                beam.touched = True
                self.hurt_player()
        if pygame.sprite.spritecollide(self.player, self.boss_group, False, hitboxes_overlap):
            self.hurt_player()

    def clear_attacks(self):
        self.fire.empty()
        self.beams.empty()
        self.minions.empty()
        self.warnings.clear()
        self.scheduled.clear()
        self.boss.warning = None
        self.boss.breathing = False
        self.boss.horizontal = None
        self.boss.dip_active = False
        self.boss.dip_y = 0
        self.boss.pulse = 0

    def damage_boss(self, amount):
        """Vida do chefe decide os níveis, a transformação e a vitória."""
        if self.state != 'playing' or amount <= 0:
            return
        b = self.boss
        b.hp = max(0, b.hp - amount)
        b.flash = .07
        if b.hp == 0:
            self.state = 'victory'
            self.state_time = 0
            self.clear_attacks()
            self.shots.empty()
            b.mouth_lock = None
            play_sound(self.assets, 'victory')
        elif b.phase < 3 and b.hp <= b.max_hp * .5:
            self.begin_transformation()
        elif b.hp <= b.max_hp * .25:
            self.change_phase(4)
        elif b.hp <= b.max_hp * .75:
            self.change_phase(2)

    def change_phase(self, phase):
        if phase > self.boss.phase:
            self.boss.phase = phase
            self.attack_timer = max(self.attack_timer, .9)
            play_sound(self.assets, 'phase')

    def begin_transformation(self):
        self.boss.phase = 3
        self.state = 'transform'
        self.state_time = 0
        self.boss.transform = 0
        self.boss.cast = 0
        self.boss.charge = 0
        self.boss.attack_type = None
        self.boss.mouth_lock = None
        self.clear_attacks()
        self.shots.empty()
        self.pattern_index = 0
        self.breath_count = 0
        play_sound(self.assets, 'transform')

    def update_transformation(self, dt, controls):
        self.boss.transform = min(1, self.state_time / c.TRANSFORM_TIME)
        self.night = self.boss.transform
        left_limit, right_limit = (195, 1085) if self.stage_index == 2 else (53, 860)
        self.player_group.update(dt, controls, False, right_limit, left_limit)
        self.boss_group.update(dt, self.elapsed, self.state)
        if self.state_time >= c.TRANSFORM_TIME:
            self.state = 'playing'
            self.state_time = 0
            self.night = 1
            self.attack_timer = 1
            self.player.invulnerable = max(self.player.invulnerable, 1.1)

    def hurt_player(self):
        """Dash e intervalo após dano impedem perder várias vidas de uma vez."""
        p = self.player
        if self.state != 'playing' or p.invulnerable > 0 or p.dash > 0:
            return False
        p.hp = max(0, p.hp - 1)
        p.invulnerable = c.HURT_TIME
        p.vx = -p.facing * 110
        play_sound(self.assets, 'hurt')
        if p.hp == 0:
            self.state = 'dead'
            self.state_time = 0
            self.clear_attacks()
            self.boss.mouth_lock = None
            play_sound(self.assets, 'death')
        return True
