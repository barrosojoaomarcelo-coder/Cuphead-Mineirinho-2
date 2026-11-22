"""Terceiro chefe, lasers, invocações, integração e tiros rápidos."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import tempfile
import unittest
import pygame
import main
from config import BOSS_HP, FLOOR, SHOT_SPEED
from engine import GameModel
from sprites import Bread
from piramide import Piramide, PyramidSide, Servant, EnergyRing, PyramidLaser
from piramide_attacks import prepare_piramide, release_piramide
from test_game import advance


class PyramidTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory()
        cls.ui = main.initialize(save_dir=cls.folder.name, muted=True)
        cls.assets = cls.ui['assets']

    @classmethod
    def tearDownClass(cls):
        pygame.quit()
        cls.folder.cleanup()

    def game(self, phase=1):
        g = GameModel(self.assets)
        g.start(2)
        advance(g, 1.8)
        g.boss.phase = phase
        g.boss.hp = BOSS_HP * (1, .73, .49, .23)[phase - 1]
        g.attack_timer = 999
        advance(g, .05)
        return g

    def test_third_stage_has_two_bodies_but_one_health_pool(self):
        g = self.game(3)
        self.assertIsInstance(g.boss, Piramide)
        self.assertEqual(len(g.boss_group), 2)
        before = g.boss.hp
        for body in g.boss_group:
            g.shots.add(Bread(self.assets, body.hitbox.centerx, FLOOR - 50, 0, 0))
        g.check_collisions()
        self.assertEqual(g.boss.hp, before - 2)
        self.assertEqual(g.stats['hits'], 2)
        self.assertFalse(g.shots)

    def test_left_eye_cannot_take_damage_before_transformation(self):
        g = self.game()
        side = next(body for body in g.boss_group if isinstance(body, PyramidSide))
        self.assertEqual(side.hitbox.size, (0, 0))
        g.shots.add(Bread(self.assets, 100, 550, 0, 0))
        before = g.boss.hp
        g.check_collisions()
        self.assertEqual(g.boss.hp, before)

    def test_final_simultaneous_hits_finish_shared_boss_once(self):
        g = self.game(4)
        g.boss.hp = 1
        for body in g.boss_group:
            g.shots.add(Bread(self.assets, body.hitbox.centerx, FLOOR - 50, 0, 0))
        g.check_collisions()
        self.assertEqual((g.state, g.boss.hp, g.stats['hits']), ('victory', 0, 1))

    def test_all_first_form_attacks_have_warning_before_launch(self):
        for kind in ('snakes', 'bats', 'swarm', 'rings_low', 'rings_high', 'rings_fan'):
            g = self.game()
            w = prepare_piramide(g, kind)
            g.attack_timer = 999
            advance(g, w['total'] - .15)
            self.assertFalse(g.minions or g.beams)
            advance(g, .22)
            self.assertTrue(g.minions or g.beams)

    def test_minions_advance_towards_player_and_can_be_shot(self):
        for kind in ('snake', 'bat'):
            g = self.game()
            servant = Servant(self.assets, kind, 600, FLOOR if kind == 'snake' else 400, 180, 540)
            g.minions.add(servant)
            advance(g, .3)
            self.assertLess(servant.x, 600)
            before = g.boss.hp
            for _ in range(servant.hp):
                g.shots.add(Bread(self.assets, *servant.hitbox.center, 0, 0))
            g.check_collisions()
            self.assertFalse(g.minions)
            self.assertEqual(g.boss.hp, before)

    def test_minion_contact_costs_one_life(self):
        g = self.game()
        g.minions.add(Servant(self.assets, 'snake', g.player.x, FLOOR, 0))
        g.check_collisions()
        self.assertEqual(g.player.hp, 2)

    def test_ring_has_hollow_center_and_damaging_rim(self):
        g = self.game()
        ring = EnergyRing((500, 400), 400, 0)
        g.player.hitbox = pygame.Rect(498, 398, 4, 4)
        self.assertFalse(ring.touches(g.player))
        g.player.hitbox.center = (529, 400)
        self.assertTrue(ring.touches(g.player))

    def test_high_ring_clears_grounded_player_and_low_ring_has_jump_solution(self):
        for hz in (30, 60, 120):
            g = self.game()
            g.beams.add(EnergyRing((500, FLOOR - 170), FLOOR - 170, 310))
            advance(g, 1.7, hz=hz)
            self.assertEqual(g.player.hp, 3)
            g = self.game()
            g.beams.add(EnergyRing((500, FLOOR - 35), FLOOR - 35, 310))
            advance(g, .74, hz=hz)
            advance(g, .7, {'jump': True}, hz=hz)
            self.assertEqual(g.player.hp, 3)

    def test_every_laser_has_a_safe_marked_lane_without_extra_protection(self):
        for phase in (3, 4):
            for kind in ('cross', 'diamond', 'floor', 'ricochet'):
                for hz in (30, 60, 120):
                    with self.subTest(phase=phase, kind=kind, hz=hz):
                        g = self.game(phase)
                        w = prepare_piramide(g, kind)
                        g.attack_timer = 999
                        self.assertTrue(w['safe'])
                        start, end = w['safe'][0]
                        g.player.x = (start + end) / 2
                        g.player.refresh_image()
                        advance(g, w['total'] + .65, hz=hz)
                        self.assertEqual(g.player.hp, 3)

    def test_low_horizontal_laser_can_be_jumped_at_all_frame_rates(self):
        for hz in (30, 60, 120):
            g = self.game(3)
            w = prepare_piramide(g, 'horizontal')
            g.attack_timer = 999
            advance(g, w['total'] - .15, hz=hz)
            advance(g, .7, {'jump': True}, hz=hz)
            self.assertEqual(g.player.hp, 3)

    def test_high_horizontal_laser_is_safe_on_floor(self):
        g = self.game(3)
        g.breath_count = 1
        w = prepare_piramide(g, 'horizontal')
        g.attack_timer = 999
        advance(g, w['total'] + .65)
        self.assertEqual(g.player.hp, 3)

    def test_laser_hits_once_and_dash_protects(self):
        for dash, hp in ((False, 2), (True, 3)):
            g = self.game(3)
            g.beams.add(PyramidLaser([(145, FLOOR - 35), (1130, FLOOR - 35)], (255, 100, 100)))
            if dash:
                g.player.dash = .21
            advance(g, .1)
            self.assertEqual(g.player.hp, hp)

    def test_aimed_reflection_keeps_announced_points_after_player_moves(self):
        g = self.game(4)
        w = prepare_piramide(g, 'ricochet')
        points = [tuple(path) for path in w['paths']]
        g.player.x = 900
        release_piramide(g, w)
        self.assertEqual([beam.points for beam in g.beams], points)

    def test_half_health_changes_form_and_clears_all_minions_and_rings(self):
        g = self.game()
        g.minions.add(Servant(self.assets, 'snake', 500, FLOOR, 180))
        g.beams.add(EnergyRing((600, 400), 400, 310))
        g.scheduled.append({'delay': 10, 'kind': 'bat'})
        g.damage_boss(BOSS_HP * .5)
        self.assertEqual((g.state, g.boss.phase), ('transform', 3))
        self.assertFalse(g.minions or g.beams or g.scheduled)
        advance(g, 3.7)
        self.assertEqual((g.state, g.night), ('playing', 1))
        self.assertTrue(all(body.hitbox.width > 0 for body in g.boss_group))

    def test_pause_freezes_minions_rings_and_pending_invocations(self):
        g = self.game()
        prepare_piramide(g, 'swarm')
        advance(g, 1.2)
        g.pause()
        before = [(m.x, m.y, m.age) for m in g.minions]
        pending = [data.copy() for data in g.scheduled]
        advance(g, 2)
        self.assertEqual(before, [(m.x, m.y, m.age) for m in g.minions])
        self.assertEqual(pending, g.scheduled)

    def test_third_stage_retry_menu_and_final_victory_controls(self):
        ui = self.ui
        main.button_action(ui, 'practice3')
        self.assertEqual((ui['game'].stage_index, ui['game'].state), (2, 'intro'))
        ui['game'].player.hp = 1
        main.handle_key(ui, pygame.K_r)
        self.assertEqual((ui['game'].stage_index, ui['game'].player.hp), (2, 3))
        ui['game'].state = 'victory'
        main.handle_key(ui, pygame.K_RETURN)
        self.assertEqual(ui['game'].state, 'title')

    def test_no_boss_health_bar_and_all_three_screens_render(self):
        for stage in range(3):
            g = GameModel(self.assets)
            g.start(stage)
            g.state = 'playing'
            self.ui['renderer'].draw(self.ui['canvas'], g)
            self.assertEqual(self.ui['canvas'].get_at((700, 52))[:3], (49, 30, 28))

    def test_twenty_fast_shots_per_second_at_multiple_frame_rates(self):
        for hz in (30, 60, 120):
            g = self.game()
            advance(g, 1, {'shoot': True}, hz=hz)
            self.assertEqual(g.stats['shots'], 20)
            shot = g.player.shoot()
            self.assertEqual(shot.vx, SHOT_SPEED)
            self.assertEqual(SHOT_SPEED, 1800)

    def test_complete_third_encounter_takes_real_projectile_damage(self):
        for hz in (30, 60, 120):
            g = self.game()
            g.attack_timer = .1
            g.player.invulnerable = 1000  # Só testa o fluxo completo, não a dificuldade.
            transformed = False
            for _ in range(hz * 70):
                g.step(1 / hz, {'shoot': True})
                transformed = transformed or g.state == 'transform'
                if g.state == 'victory':
                    break
            self.assertTrue(transformed)
            self.assertEqual((g.state, g.boss.hp, g.stats['hits']), ('victory', 0, BOSS_HP))
            self.assertFalse(g.minions or g.beams or g.scheduled)


if __name__ == '__main__':
    unittest.main()
