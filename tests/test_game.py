"""Regras e integração da versão simplificada, sem abrir uma janela real."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import json
import math
from pathlib import Path
import tempfile
import unittest
import pygame
from assets import load_assets
from engine import GameModel
from sprites import Player, Boss, Bread, Fire, Flame, hitboxes_overlap
from attacks import prepare_attack, release_attack, update_attacks
from config import FLOOR, BOSS_HP, HURT_TIME, TRANSFORM_TIME
import main


def advance(game, seconds, controls=None, hz=60):
    if controls is None:
        controls = {}
    for _ in range(round(seconds * hz)):
        game.step(1 / hz, controls)


def playable(assets, phase=1, protected=False):
    game = GameModel(assets)
    game.start()
    advance(game, 1.8)
    game.boss.phase = phase
    game.boss.hp = BOSS_HP * (1, .73, .49, .23)[phase - 1]
    game.night = int(phase >= 3)
    game.refresh_boss()
    if protected:
        game.player.invulnerable = 1000
    return game


def prepare(game, kind, mode=None):
    for _ in range(3):
        prepare_attack(game, kind)
        game.attack_timer = 999
        warning = game.warnings[-1]
        if mode is None or warning.get('mode') == mode:
            return warning
    raise AssertionError('Modo não encontrado')


def release(game, warning):
    game.warnings.clear()
    release_attack(game, warning)
    game.attack_timer = 999
    game.step(1 / 60, {})


class GameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.mixer.pre_init(22050, -16, 1)
        pygame.init()
        pygame.display.set_mode((1280, 720))
        cls.assets = load_assets()
        cls.assets['muted'] = True

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def game(self, phase=1, protected=False):
        return playable(self.assets, phase, protected)

    def test_real_sprites_and_groups(self):
        g = self.game()
        self.assertIsInstance(g.player, pygame.sprite.Sprite)
        self.assertIsInstance(g.boss, pygame.sprite.Sprite)
        self.assertIsInstance(g.shots, pygame.sprite.Group)
        self.assertIsInstance(g.fire, pygame.sprite.Group)
        self.assertIsInstance(g.beams, pygame.sprite.Group)
        self.assertIsInstance(g.player.image, pygame.Surface)
        self.assertIsInstance(g.player.rect, pygame.Rect)

    def test_reset_clears_combat(self):
        g = self.game()
        g.hurt_player()
        release(g, prepare(g, 'flame'))
        g.start()
        self.assertEqual((g.state, g.player.hp, g.boss.phase, g.boss.hp), ('intro', 3, 1, BOSS_HP))
        self.assertFalse(g.shots or g.fire or g.beams or g.warnings or g.scheduled)
        self.assertEqual(g.stats, {'shots': 0, 'hits': 0, 'dashes': 0})

    def test_movement_and_limits(self):
        g = self.game(protected=True)
        advance(g, 4, {'right': True})
        self.assertEqual(g.player.x, 920)
        advance(g, 4, {'left': True})
        self.assertEqual(g.player.x, 53)
        g.boss.phase = 3
        advance(g, 4, {'right': True})
        self.assertEqual(g.player.x, 860)

    def test_jump_release_and_landing(self):
        hold, tap = self.game(protected=True), self.game(protected=True)
        lowest_hold = lowest_tap = FLOOR
        for i in range(100):
            hold.step(1 / 60, {'jump': i < 45})
            tap.step(1 / 60, {'jump': i < 4})
            lowest_hold = min(lowest_hold, hold.player.y)
            lowest_tap = min(lowest_tap, tap.player.y)
        self.assertLess(lowest_hold, lowest_tap - 35)
        self.assertEqual((hold.player.y, tap.player.y), (FLOOR, FLOOR))

    def test_buffered_jump(self):
        g = self.game()
        g.player.y = FLOOR - 5
        g.player.vy = 250
        g.player.on_ground = False
        g.player.coyote = 0
        advance(g, .07, {'jump': True})
        self.assertLess(g.player.vy, -400)
        self.assertFalse(g.player.on_ground)

    def test_dash_protection_and_cooldown(self):
        g = self.game()
        g.step(1 / 60, {'dash': True, 'right': True})
        self.assertGreater(g.player.x, 190)
        self.assertFalse(g.hurt_player())
        g.step(1 / 60, {})
        g.step(1 / 60, {'dash': True})
        self.assertEqual(g.stats['dashes'], 1)
        advance(g, .6)
        g.step(1 / 60, {'dash': True})
        self.assertEqual(g.stats['dashes'], 2)

    def test_three_lives_and_hurt_grace(self):
        g = self.game()
        g.attack_timer = 999
        for hp in (2, 1, 0):
            self.assertTrue(g.hurt_player())
            self.assertFalse(g.hurt_player())
            self.assertEqual(g.player.hp, hp)
            advance(g, HURT_TIME + .1)
        self.assertEqual(g.state, 'dead')

    def test_pause_freezes_midair_and_inputs(self):
        g = self.game()
        g.step(1 / 60, {'jump': True})
        before = g.player.y, g.player.vy, g.elapsed
        g.pause()
        advance(g, 2, {'shoot': True, 'dash': True, 'jump': True})
        self.assertEqual((g.player.y, g.player.vy, g.elapsed), before)
        self.assertEqual((g.stats['shots'], g.stats['dashes']), (0, 0))
        g.resume()
        g.step(1 / 60, {})
        self.assertGreater(g.player.vy, before[1])

    def test_shot_cadence_and_fingertip(self):
        g = self.game(protected=True)
        advance(g, 1, {'shoot': True})
        self.assertEqual(g.stats['shots'], 12)
        p = g.player
        shot = p.shoot()
        muzzle = self.assets['manifest']['player']['actions'][p.action]['muzzles'][p.frame]
        self.assertAlmostEqual(shot.x, p.x + (muzzle[0] - 120) * 174 / 256)
        self.assertAlmostEqual(shot.y, p.y + (muzzle[1] - 240) * 174 / 256)

    def test_aim_directions_and_sprite_cleanup(self):
        g = self.game()
        for controls, direction in (({'up': True}, (0, -1)), ({'up': True, 'right': True}, (1, -1)),
                                    ({'left': True}, (-1, 0))):
            g.player.update(1 / 60, dict(controls, shoot=True))
            shot = g.player.shoot()
            self.assertEqual((g.player.aim_x, g.player.aim_y), direction)
            self.assertAlmostEqual(math.hypot(shot.vx, shot.vy), 1450)
        g.shots.add(shot)
        shot.update(2)
        self.assertFalse(g.shots)

    def test_shot_damages_once_and_is_removed(self):
        g = self.game()
        shot = Bread(self.assets, 1050, 400, 1, 0)
        g.shots.add(shot)
        g.check_collisions()
        g.check_collisions()
        self.assertEqual(g.boss.hp, BOSS_HP - 1)
        self.assertEqual(g.stats['hits'], 1)
        self.assertFalse(g.shots)

    def test_forms_and_night_transition(self):
        g = self.game(protected=True)
        g.damage_boss(91)
        self.assertEqual(g.boss.phase, 2)
        g.damage_boss(90)
        self.assertEqual((g.state, g.boss.phase), ('transform', 3))
        hp = g.boss.hp
        g.damage_boss(100)
        self.assertEqual(g.boss.hp, hp)
        advance(g, TRANSFORM_TIME + .1)
        self.assertEqual((g.state, g.night), ('playing', 1))
        g.damage_boss(90)
        self.assertEqual(g.boss.phase, 4)
        g.damage_boss(360)
        self.assertEqual(g.state, 'victory')
        self.assertFalse(g.shots or g.beams or g.fire)

    def test_nine_patterns_at_all_tiers(self):
        for phase in range(1, 5):
            for kind in ('fan', 'aimed', 'burst', 'steps', 'sine', 'bounce', 'rain', 'flame', 'giant'):
                with self.subTest(phase=phase, pattern=kind):
                    g = self.game(phase, True)
                    w = prepare(g, kind)
                    self.assertGreaterEqual(w['total'], 1.2)
                    advance(g, w['total'] + .8)
                    self.assertLessEqual(len(g.fire), 40)
                    self.assertLessEqual(len(g.beams), 1)
                    self.assertLess(len(g.scheduled), 15)
                    for fire in g.fire:
                        self.assertTrue(math.isfinite(fire.x) and math.isfinite(fire.y))
                        self.assertIsInstance(fire.image, pygame.Surface)

    def test_fan_count_and_speed(self):
        for phase in range(1, 5):
            g = self.game(phase, True)
            release(g, prepare(g, 'fan'))
            self.assertEqual(len(g.fire), (0, 3, 3, 4, 5)[phase])
            self.assertTrue(all(math.hypot(f.vx, f.vy) <= 246 for f in g.fire))

    def test_rain_safe_corridor_and_bounce(self):
        g = self.game(4, True)
        warning = prepare(g, 'rain')
        self.assertIn(len(warning['lanes']), (3, 4))
        self.assertTrue(all(abs(x - warning['safe_x']) > 195 for x in warning['lanes']))
        release(g, warning)
        self.assertTrue(all(f.vx == 0 and f.vy == 210 for f in g.fire))
        g.clear_attacks()
        release(g, prepare(g, 'bounce'))
        self.assertEqual(len(g.fire), 1)
        fire = list(g.fire)[0]
        self.assertEqual(fire.bounces, 1)
        advance(g, 1.5)
        self.assertEqual(fire.bounces, 0)

    def test_burst_keeps_warned_direction(self):
        g = self.game(4, True)
        w = prepare(g, 'burst')
        angle = w['angle']
        g.player.x = 720
        release(g, w)
        advance(g, .65, {'left': True})
        self.assertTrue(all(abs(math.atan2(f.vy, f.vx) - angle) < 1e-8 for f in g.fire))

    def test_special_clears_old_hazards(self):
        for kind in ('flame', 'giant', 'rain'):
            g = self.game(protected=True)
            release(g, prepare(g, 'fan'))
            self.assertTrue(g.fire)
            prepare(g, kind)
            self.assertFalse(g.fire or g.beams or g.scheduled)
            self.assertEqual(len(g.warnings), 1)

    def test_giant_does_not_overlap_other_patterns(self):
        g = self.game(protected=True)
        release(g, prepare(g, 'giant'))
        g.attack_timer = 0
        advance(g, .65)
        self.assertEqual(len(g.fire), 1)
        self.assertEqual(list(g.fire)[0].kind, 'giant')
        self.assertFalse(g.warnings or g.beams)

    def test_low_flame_hits_once(self):
        for hz in (30, 60, 120):
            g = self.game()
            w = prepare(g, 'flame', 'low')
            advance(g, w['total'] + .65, hz=hz)
            self.assertEqual(g.player.hp, 2)
            self.assertFalse(g.beams)

    def test_jump_avoids_low_flame(self):
        g = self.game()
        w = prepare(g, 'flame', 'low')
        advance(g, w['total'] - .17)
        advance(g, .72, {'jump': True})
        self.assertEqual(g.player.hp, 3)

    def test_dash_avoids_full_flame(self):
        g = self.game()
        w = prepare(g, 'flame', 'low')
        advance(g, w['total'] - .04)
        advance(g, .7, {'dash': True, 'right': True})
        self.assertEqual(g.player.hp, 3)

    def test_high_flame_avoided_on_ground(self):
        g = self.game()
        w = prepare(g, 'flame', 'high')
        advance(g, w['total'] + .65, {'down': True})
        self.assertEqual(g.player.hp, 3)

    def test_flame_pauses_and_remembers_aim(self):
        g = self.game(protected=True)
        w = prepare(g, 'flame', 'low')
        g.player.x = 740
        release(g, w)
        beam = list(g.beams)[0]
        self.assertEqual((beam.end_x, beam.end_y), (w['end_x'], w['end_y']))
        age = beam.age
        g.pause()
        advance(g, 2)
        self.assertEqual(beam.age, age)
        g.resume()
        advance(g, .65)
        self.assertFalse(g.beams)

    def test_terminal_paths_clear_beams(self):
        for path in ('death', 'victory', 'transform', 'reset'):
            g = self.game()
            release(g, prepare(g, 'flame'))
            if path == 'death':
                g.player.hp = 1
                g.hurt_player()
            elif path == 'victory':
                g.damage_boss(360)
            elif path == 'transform':
                g.damage_boss(181)
            else:
                g.reset()
            self.assertFalse(g.beams or g.warnings)

    def test_full_encounter_wins_at_three_frame_rates(self):
        for hz in (30, 60, 120):
            g = self.game(protected=True)
            saw_transform = False
            for _ in range(hz * 50):
                g.step(1 / hz, {'shoot': True})
                if g.state == 'transform':
                    saw_transform = True
                if g.state == 'victory':
                    break
            self.assertTrue(saw_transform)
            self.assertEqual((g.state, g.stats['hits'], g.night), ('victory', 360, 1))
            self.assertTrue(30 <= g.elapsed <= 45)

    def test_invalid_time_ignored(self):
        g = self.game()
        before = g.elapsed
        for dt in (0, -1, math.inf, math.nan):
            g.step(dt, {})
        self.assertEqual(g.elapsed, before)


class InterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.storage = tempfile.TemporaryDirectory()
        cls.ui = main.initialize(size=(960, 540), save_dir=cls.storage.name, muted=True)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()
        cls.storage.cleanup()

    def setUp(self):
        self.ui['game'].reset()
        self.ui['instructions'] = False
        self.ui['resume_after_help'] = False
        self.ui['running'] = True
        self.ui['best'] = None

    def key(self, key):
        main.handle_event(self.ui, pygame.event.Event(pygame.KEYDOWN, key=key))

    def test_all_screens_and_assets(self):
        for state in ('title', 'intro', 'playing', 'paused', 'dead', 'victory', 'transform'):
            self.ui['game'].state = state
            main.draw_screen(self.ui)
        self.assertEqual(len(self.ui['assets']['frames']['head']), 8)
        self.assertEqual(len(self.ui['assets']['sounds']), 14)

    def test_start_pause_restart(self):
        g = self.ui['game']
        self.key(pygame.K_RETURN)
        self.assertEqual(g.state, 'intro')
        self.key(pygame.K_p)
        self.assertEqual(g.state, 'paused')
        self.key(pygame.K_ESCAPE)
        self.assertEqual(g.state, 'intro')
        g.player.hp = 1
        self.key(pygame.K_r)
        self.assertEqual((g.state, g.player.hp), ('intro', 3))

    def test_help_freezes_and_returns(self):
        g = self.ui['game']
        g.state = 'playing'
        self.key(pygame.K_h)
        self.assertTrue(self.ui['instructions'])
        self.assertEqual(g.state, 'paused')
        main.draw_screen(self.ui)
        self.assertIn('back', self.ui['buttons'])
        self.assertNotIn('play', self.ui['buttons'])
        self.key(pygame.K_ESCAPE)
        self.assertEqual(g.state, 'playing')

    def test_help_from_pause_stays_paused(self):
        self.ui['game'].state = 'playing'
        self.ui['game'].pause()
        self.key(pygame.K_h)
        self.key(pygame.K_ESCAPE)
        self.assertEqual(self.ui['game'].state, 'paused')

    def test_focus_loss(self):
        self.ui['game'].state = 'playing'
        main.handle_event(self.ui, pygame.event.Event(pygame.WINDOWFOCUSLOST))
        self.assertEqual(self.ui['game'].state, 'paused')

    def test_resize_and_scaled_click(self):
        main.handle_event(self.ui, pygame.event.Event(pygame.VIDEORESIZE, w=1000, h=800))
        main.draw_screen(self.ui)
        rect = self.ui['buttons']['play']
        view = self.ui['viewport']
        point = (round(view.x + rect.centerx * view.w / 1280), round(view.y + rect.centery * view.h / 720))
        main.handle_event(self.ui, pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=point))
        self.assertEqual(self.ui['game'].state, 'intro')
        self.assertGreater(view.y, 0)

    def test_fullscreen_roundtrip(self):
        main.toggle_fullscreen(self.ui)
        self.assertTrue(self.ui['fullscreen'])
        main.draw_screen(self.ui)
        main.toggle_fullscreen(self.ui)
        self.assertFalse(self.ui['fullscreen'])
        main.draw_screen(self.ui)

    def test_save_sound_and_best(self):
        self.ui['best'] = 42.5
        self.key(pygame.K_m)
        best, muted = main.load_preferences(self.ui['save_file'])
        self.assertEqual(best, 42.5)
        self.assertEqual(muted, self.ui['assets']['muted'])
        self.ui['save_file'].write_text('{broken', encoding='utf-8')
        self.assertEqual(main.load_preferences(self.ui['save_file']), (None, False))

    def test_victory_updates_record(self):
        self.ui['game'].state = 'victory'
        self.ui['game'].elapsed = 37.5
        main.update_game(self.ui, 1 / 60, {})
        self.assertEqual(self.ui['best'], 37.5)
        self.assertEqual(main.load_preferences(self.ui['save_file'])[0], 37.5)

    def test_quit(self):
        main.handle_event(self.ui, pygame.event.Event(pygame.QUIT))
        self.assertFalse(self.ui['running'])


if __name__ == '__main__':
    unittest.main()
