"""Progressão, colisões e ataques da segunda fase, com dispositivos virtuais."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import tempfile
import unittest
import pygame
import main
from engine import GameModel
from comilao import Comilao, Tongue, EyeRay, Spike, prepare_comilao
from config import FLOOR


def advance(game, seconds, controls=None, hz=60):
    for _ in range(round(seconds * hz)):
        game.step(1 / hz, controls or {})


class ComilaoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory()
        cls.ui = main.initialize(save_dir=cls.folder.name, muted=True)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()
        cls.folder.cleanup()

    def game(self):
        game = GameModel(self.ui['assets'])
        game.start(1)
        advance(game, 1.8)
        game.attack_timer = 999
        return game

    def test_campaign_needs_victory_and_stops_at_undefined_third_boss(self):
        g = GameModel(self.ui['assets'])
        g.start_story()
        self.assertEqual(g.state, 'story')
        self.assertFalse(g.next_stage())
        g.start()
        advance(g, 1.8)
        g.damage_boss(360)
        self.assertTrue(g.next_stage())
        self.assertEqual((g.stage_index, g.state, g.player.hp), (1, 'intro', 3))
        advance(g, 1.8)
        g.damage_boss(360)
        self.assertFalse(g.next_stage())
        self.assertFalse(g.start(2))
        self.assertEqual((g.stage_index, g.state), (1, 'victory'))

    def test_telegraphs_precede_all_six_attacks(self):
        for kind in ('eye', 'low', 'high', 'sweep', 'spikes', 'moving'):
            with self.subTest(kind=kind):
                g = self.game()
                prepare_comilao(g, kind)
                g.attack_timer = 999
                advance(g, 1.2)
                self.assertFalse(g.beams or g.fire)
                advance(g, .2)
                self.assertTrue(g.beams or g.fire)
                advance(g, 4)
                self.assertFalse(g.beams or g.fire or g.warnings)

    def test_rays_keep_three_warned_directions(self):
        g = self.game()
        prepare_comilao(g, 'eye')
        ends = list(g.warnings[0]['ends'])
        origin = g.warnings[0]['origin']
        g.player.x = 700
        g.attack_timer = 999
        advance(g, 1.4)
        self.assertEqual([r.end for r in g.beams], ends)
        self.assertTrue(all(r.start == origin for r in g.beams))

    def test_low_tongue_hits_once_and_high_misses_grounded_player(self):
        for mode, expected in (('low', 2), ('high', 3)):
            g = self.game()
            g.beams.add(Tongue(g.boss.mouth(0), mode))
            advance(g, 1)
            self.assertEqual(g.player.hp, expected)

    def test_timed_jump_and_dash_avoid_low_tongue(self):
        g = self.game()
        g.beams.add(Tongue(g.boss.mouth(0), 'low'))
        advance(g, .7, {'jump': True})
        self.assertEqual(g.player.hp, 3)
        g = self.game()
        tongue = Tongue(g.boss.mouth(0), 'low')
        tongue.age = .22
        tongue.refresh_image()
        g.beams.add(tongue)
        g.player.dash = .21
        g.player.dash_direction = -1
        advance(g, .15)
        self.assertEqual(g.player.hp, 3)

    def test_spike_corridor_and_cleanup(self):
        g = self.game()
        prepare_comilao(g, 'spikes')
        warning = g.warnings[0]
        self.assertTrue(all(abs(x - warning['safe_x']) > 180 for x in warning['lanes']))
        g.attack_timer = 999
        advance(g, 4)
        self.assertEqual(g.player.hp, 3)
        self.assertFalse(g.fire)

    def test_transformation_and_all_screens(self):
        g = self.game()
        self.assertIsInstance(g.boss, Comilao)
        g.damage_boss(180)
        self.assertEqual(g.state, 'transform')
        advance(g, 3.7)
        self.assertEqual((g.state, g.boss.phase), ('playing', 3))
        for state in ('intro', 'playing', 'transform', 'paused', 'dead', 'victory'):
            g.state = state
            self.ui['renderer'].draw(self.ui['canvas'], g)
        for name in ('comilao-corpo', 'comilao-boca'):
            self.assertEqual(len(self.ui['assets']['frames'][name]), 8)
            self.assertEqual(self.ui['assets']['frames'][name][0].get_at((0, 0)).a, 0)

    def test_retry_and_keyboard_advance_preserve_correct_stage(self):
        self.ui['game'] = g = self.game()
        g.player.hp = 1
        main.handle_key(self.ui, pygame.K_r)
        self.assertEqual((g.stage_index, g.player.hp, g.state), (1, 3, 'intro'))
        g.state = 'victory'
        main.handle_key(self.ui, pygame.K_RETURN)
        self.assertEqual(g.state, 'title')

    def test_pause_freezes_tongue_and_terminal_states_clear_it(self):
        for state in ('dead', 'victory', 'transform'):
            g = self.game()
            tongue = Tongue(g.boss.mouth(0), 'low')
            g.beams.add(tongue)
            g.pause()
            advance(g, 1)
            self.assertEqual(tongue.age, 0)
            g.resume()
            if state == 'dead':
                g.player.hp = 1
                g.hurt_player()
            else:
                g.damage_boss(360 if state == 'victory' else 180)
            self.assertEqual(g.state, state)
            self.assertFalse(g.beams)

    def test_second_stage_does_not_replace_dragon_record(self):
        self.ui['game'] = g = self.game()
        self.ui['best'] = 40
        g.state, g.elapsed = 'victory', 10
        main.update_game(self.ui, 1 / 60, {})
        self.assertEqual(self.ui['best'], 40)

    def test_complete_second_encounter_at_multiple_frame_rates(self):
        for hz in (30, 60, 120):
            g = self.game()
            g.attack_timer = .1
            g.player.invulnerable = 1000  # Verifica fluxo; não mede dificuldade humana.
            for _ in range(hz * 85):
                g.step(1 / hz, {'shoot': True})
                if g.state == 'victory':
                    break
            self.assertEqual((g.state, g.stats['hits'], g.player.hp), ('victory', 360, 3))


if __name__ == '__main__':
    unittest.main()
