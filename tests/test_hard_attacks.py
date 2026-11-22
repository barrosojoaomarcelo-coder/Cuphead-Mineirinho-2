"""Pressão dos dois chefes e esquivas reais, sem proteção nos testes de esquiva."""
import math
import tempfile
import unittest
import pygame
import main
from attacks import prepare_attack
from boss_attacks import HARD_ATTACKS
from comilao import prepare_comilao
from engine import GameModel
from piramide_attacks import prepare_piramide
from sprites import Fire, hitboxes_overlap
from test_game import advance, playable


class HardAttackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory()
        cls.ui = main.initialize(save_dir=cls.folder.name, muted=True)
        cls.assets = cls.ui['assets']

    @classmethod
    def tearDownClass(cls):
        pygame.quit()
        cls.folder.cleanup()

    def dragon(self, phase=1, kind=None, x=190):
        g = playable(self.assets, phase)
        g.player.x = x
        g.player.refresh_image()
        w = prepare_attack(g, kind) if kind else None
        g.attack_timer = 999
        return g, w

    def comilao(self, phase=1):
        g = self.ui['game']
        g.start(1)
        advance(g, 1.8)
        g.boss.phase = phase
        g.boss.hp = g.boss.max_hp * (1, .73, .49, .23)[phase - 1]
        g.attack_timer = 999
        g.refresh_boss()
        return g

    def test_horizontal_rows_allow_jumping_and_crouching(self):
        for phase in range(1, 5):
            for alternate in (False, True):
                for x in (190, 550):
                    for hz in (30, 60, 120):
                        with self.subTest(phase=phase, alternate=alternate, x=x, hz=hz):
                            g, _ = self.dragon(phase, x=x)
                            g.horizontal_count = int(alternate)
                            w = prepare_attack(g, 'horizontal')
                            g.attack_timer = 999
                            starts = [w['total'] + row['start'] + (w['x'] - x) / row['speed'] - .23
                                      for row in w['rows'] if row['mode'] == 'low']
                            last = w['rows'][-1]
                            end = w['total'] + last['start'] + (last['count'] - 1) * last['spacing'] + (w['x'] + 70) / last['speed'] + .6
                            for tick in range(round(end * hz)):
                                now = tick / hz
                                jumping = any(start <= now < start + .66 for start in starts)
                                g.step(1 / hz, {'jump': jumping, 'down': not jumping})
                            self.assertEqual((g.player.hp, g.state), (3, 'playing'))
                            self.assertIsNone(g.boss.horizontal)

    def test_giant_chain_allows_two_separate_jumps(self):
        for phase in (3, 4):
            for x in (190, 550):
                for hz in (30, 60, 120):
                    with self.subTest(phase=phase, x=x, hz=hz):
                        g, w = self.dragon(phase, 'giant', x)
                        tuning = HARD_ATTACKS[phase - 1]
                        travel = (w['x'] - x) / (-math.cos(w['angle']) * tuning['giant_speed'])
                        starts = [w['total'] + i * tuning['giant_gap'] + travel - .28
                                  for i in range(tuning['giant_count'])]
                        for tick in range(round((starts[-1] + 1.2) * hz)):
                            now = tick / hz
                            g.step(1 / hz, {'jump': any(start <= now < start + .66 for start in starts)})
                        self.assertEqual(g.player.hp, 3)

    def test_pending_second_giant_stays_exclusive(self):
        g, w = self.dragon(4, 'giant')
        advance(g, w['total'] + .1)
        g.fire.empty()
        g.attack_timer = 0
        advance(g, .15)
        self.assertFalse(g.warnings)
        self.assertTrue(any(d.get('kind') == 'giant' for d in g.scheduled))

    def test_horizontal_volume_and_height_match_each_announced_row(self):
        for phase in range(1, 5):
            g, w = self.dragon(phase, 'horizontal')
            g.player.invulnerable = 1000  # Apenas contagem e fluxo.
            count = 0
            seen = set()
            for _ in range(6 * 120):
                g.step(1 / 120, {})
                for fire in g.fire:
                    if fire not in seen:
                        seen.add(fire)
                        count += 1
                        self.assertEqual(fire.y, 594 if fire.y > 570 else 538)
                        self.assertEqual(fire.vy, 0)
                        self.assertEqual(fire.vx, -(700, 760, 840, 920)[phase - 1])
            self.assertEqual(count, (2 * 4, 2 * 5, 3 * 5, 4 * 6)[phase - 1])

    def test_dragon_idle_player_is_under_real_pressure(self):
        g, _ = self.dragon()
        g.attack_timer = .1
        advance(g, 24)
        self.assertEqual((g.player.hp, g.state), (0, 'dead'))

    def test_holding_fire_without_dodging_cannot_win_any_stage(self):
        for stage in range(3):
            for hz in (30, 60, 120):
                with self.subTest(stage=stage, hz=hz):
                    g = GameModel(self.assets)
                    g.start(stage)
                    advance(g, 1.8, hz=hz)
                    for _ in range(60 * hz):
                        g.step(1 / hz, {'shoot': True})
                        if g.state in ('victory', 'dead'):
                            break
                    self.assertEqual((g.state, g.player.hp), ('dead', 0))

    def test_dragon_zip_weapon_is_restored_without_leaking_to_other_stages(self):
        for hz in (30, 60, 120):
            g = GameModel(self.assets)
            for stage in (0, 1, 2, 0):
                with self.subTest(stage=stage, hz=hz):
                    g.start(stage)
                    advance(g, 1.8, hz=hz)
                    g.attack_timer = 999
                    expected_hp, expected_shots, expected_speed = (480, 12, 1450) if stage == 0 else (800, 20, 1800)
                    self.assertEqual((g.boss.hp, g.boss.max_hp), (expected_hp, expected_hp))
                    advance(g, 1, {'shoot': True}, hz=hz)
                    self.assertEqual(g.stats['shots'], expected_shots)
                    shot = g.player.shoot()
                    self.assertAlmostEqual(math.hypot(shot.vx, shot.vy), expected_speed)

    def test_dragon_transformation_restarts_horizontal_sequence_like_zip(self):
        for previous_count in (0, 1, 2, 3):
            g, _ = self.dragon()
            g.horizontal_count = previous_count
            g.damage_boss(g.boss.max_hp * .5)
            self.assertEqual(g.horizontal_count, 0)
            advance(g, 3.7)
            w = prepare_attack(g, 'horizontal')
            self.assertEqual(w['rows'][0]['mode'], 'high')

    def test_pyramid_safe_lanes_are_reachable_with_movement_and_dash(self):
        for phase in (3, 4):
            for kind in ('cross', 'diamond', 'floor', 'ricochet'):
                for x in (220, 450, 640, 850, 1080):
                    for hz in (30, 60, 120):
                        with self.subTest(phase=phase, kind=kind, x=x, hz=hz):
                            g = GameModel(self.assets)
                            g.start(2)
                            advance(g, 1.8, hz=hz)
                            g.boss.phase = phase
                            g.boss.hp = g.boss.max_hp * (.49 if phase == 3 else .23)
                            g.player.x = x
                            g.player.refresh_image()
                            g.boss_group.update(0, g.elapsed, 'playing')
                            w = prepare_piramide(g, kind)
                            g.attack_timer = 999
                            # Alvo dentro da faixa, sem mudar posição durante a esquiva.
                            targets = [max(left + 12, min(x, right - 12))
                                       for left, right in w['safe']]
                            target = min(targets, key=lambda spot: abs(spot - x))
                            # Reserva 0,15 s para reação. O dash é acionado uma
                            # vez, longe do instante ativo: sua proteção não cobre o raio.
                            advance(g, .15, hz=hz)
                            use_dash = abs(target - x) > 180
                            for tick in range(round((w['total'] + .5) * hz)):
                                delta = target - g.player.x
                                g.step(1 / hz, {'right': delta > 5, 'left': delta < -5,
                                               'dash': use_dash and tick == 0})
                            self.assertEqual(g.player.hp, 3)

    def test_comilao_final_combo_has_three_individually_warned_strikes(self):
        g = self.comilao(4)
        prepare_comilao(g, 'low')
        g.attack_timer = 999
        modes = []
        seen = []
        for _ in range(6 * 120):
            for w in g.warnings:
                if not any(w is old for old in seen):
                    seen.append(w)
                    modes.append(w['kind'])
                    self.assertGreaterEqual(w['total'], .72)
            g.step(1 / 120, {})
            # Não há proteção de teste: jogador parado recebe dano, mas cada
            # contato respeita o intervalo normal entre perdas de vida.
        self.assertEqual(modes[:3], ['low', 'high', 'low'])
        self.assertLess(g.player.hp, 3)

    def test_comilao_combo_has_a_real_jump_crouch_solution(self):
        for hz in (30, 60, 120):
            g = self.comilao(4)
            prepare_comilao(g, 'low')
            g.attack_timer = 999
            for _ in range(5 * hz):
                jump = False
                for warning in g.warnings:
                    if warning['kind'] == 'low' and not warning['fired'] and warning['remaining'] < .13:
                        jump = True
                # Segura o salto até a descida, sem gerar um salto automático.
                jump = jump or (not g.player.on_ground and g.player.vy < 0)
                g.step(1 / hz, {'jump': jump, 'down': not jump})
            self.assertEqual(g.player.hp, 3)

    def test_comilao_three_spike_waves_keep_one_safe_corridor(self):
        for x in (53, 190, 550, 850):
            g = self.comilao(4)
            g.player.x = x
            g.player.refresh_image()
            prepare_comilao(g, 'spikes')
            g.attack_timer = 999
            warning = g.warnings[-1]
            target = warning['safe_x']
            # Anda até a faixa anunciada, sem proteção de teste.
            advance(g, .35, {'right': x < target, 'left': x > target})
            advance(g, 3)
            self.assertEqual(g.player.hp, 3)
            self.assertFalse(g.scheduled or g.fire)

    def test_pause_and_all_terminal_paths_remove_pending_combos(self):
        for boss_stage in (0, 1):
            for ending in ('dead', 'victory', 'transform', 'reset'):
                if boss_stage == 0:
                    g, w = self.dragon(1, 'horizontal')
                else:
                    g = self.comilao(2)
                    prepare_comilao(g, 'low')
                    w = g.warnings[-1]
                advance(g, w['total'] + .05)
                self.assertTrue(g.scheduled)
                before = [d.copy() for d in g.scheduled]
                g.pause()
                advance(g, 2)
                self.assertEqual(g.scheduled, before)
                g.resume()
                if ending == 'dead':
                    g.player.hp = 1
                    g.player.invulnerable = 0
                    g.hurt_player()
                elif ending == 'reset':
                    g.reset()
                else:
                    g.damage_boss(g.boss.max_hp if ending == 'victory' else g.boss.max_hp * .6)
                self.assertFalse(g.scheduled or g.warnings or g.beams or g.fire)
                self.assertIsNone(g.boss.horizontal)

    def test_fast_projectile_cannot_skip_player_between_frames(self):
        g, _ = self.dragon()
        fire = Fire(self.assets, {'x': 240, 'y': g.player.y - 50, 'vx': -3000, 'vy': 0, 'r': 14}, (0, 0))
        fire.update(1 / 30)
        self.assertFalse(g.player.hitbox.colliderect(fire.hitbox))
        self.assertTrue(hitboxes_overlap(g.player, fire))

    def test_distinct_animation_poses_do_not_change_player_hitbox(self):
        g = self.comilao()
        for name in ('comilao-corpo', 'comilao-boca'):
            hashes = {hash(pygame.image.tobytes(frame, 'RGBA')) for frame in self.assets['frames'][name]}
            self.assertEqual(len(hashes), 12)
        box = g.player.hitbox.copy()
        first = g.player.image
        g.player.land_time = .1
        g.player.refresh_image()
        self.assertEqual(g.player.hitbox, box)
        self.assertIsNot(g.player.image, first)
        self.assertLessEqual(len(self.assets['animated']), 256)


if __name__ == '__main__':
    unittest.main()
