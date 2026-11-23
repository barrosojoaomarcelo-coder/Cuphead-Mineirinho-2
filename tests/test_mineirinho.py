"""Regressões da revisão da main, usando as artes, sons e chefes reais."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import math
import tempfile
import unittest
from unittest.mock import patch
import pygame
import audio
import config
import main


class MainRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory()
        cls.ui = main.initialize(save_dir=cls.folder.name, muted=True)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()
        cls.folder.cleanup()

    def setUp(self):
        self.ui['assets']['muted'] = True
        self.ui['title_menu'].som = False
        main.button_action(self.ui, 'menu')
        self.ui['title_menu'].selecionado = 0
        self.ui['title_menu'].foco = -1

    def key(self, key):
        main.handle_event(self.ui, pygame.event.Event(pygame.KEYDOWN, key=key))

    def enter_fight(self):
        game = self.ui['game']
        for _ in range(36):
            main.update_game(self.ui, .05, {})
        self.assertEqual(game.state, 'playing')
        game.attack_timer = 999
        return game

    def test_campaign_has_story_and_consistent_results_and_credits(self):
        self.assertEqual(pygame.display.get_caption()[0], 'Mineirinho')
        main.draw_screen(self.ui)
        rendered = {key[0] for key in self.ui['title_menu'].textos}
        self.assertIn('Criadores: Davi, Moisés e João Marcelo', rendered)
        self.key(pygame.K_RETURN)
        self.assertEqual(self.ui['game'].state, 'story')
        self.key(pygame.K_RETURN)
        for stage, next_name in ((2, 'Chefe Comilão'), (1, 'Dragão Vermelho'), (0, None)):
            game = self.enter_fight()
            self.assertEqual(game.stage_index, stage)
            game.damage_boss(game.boss.max_hp)
            self.assertEqual(game.state, 'victory')
            renderer = self.ui['renderer']
            with patch.object(renderer, 'text', wraps=renderer.text) as text:
                main.draw_screen(self.ui)
                lines = [call.args[1] for call in text.call_args_list]
            self.assertIn(config.CREATORS_LABEL, lines)
            if next_name:
                self.assertIn(f'O próximo duelo é contra {next_name}.', lines)
            else:
                self.assertIn('AVENTURA CONCLUÍDA!', lines)
                self.assertIn('Obrigado por jogar Mineirinho!', lines)
            self.key(pygame.K_RETURN)
        self.assertEqual(self.ui['game'].state, 'title')

    def test_scaled_mouse_selects_each_stage_and_ignores_margins(self):
        for size in ((960, 540), (1000, 800), (1600, 600)):
            for number, stage in ((1, 2), (2, 1), (3, 0)):
                main.button_action(self.ui, 'menu')
                main.handle_event(self.ui, pygame.event.Event(pygame.VIDEORESIZE, w=size[0], h=size[1]))
                main.draw_screen(self.ui)
                view = self.ui['viewport']
                # A margem não pertence ao menu, mesmo quando está na altura de um botão.
                if view.x or view.y:
                    main.handle_event(self.ui, pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(0, 0)))
                    self.assertEqual(self.ui['game'].state, 'title')
                menu = self.ui['title_menu']
                for point in (menu.nivel_rects[number - 1].center, menu.iniciar_rect.center):
                    position = (round(view.x + point[0] * view.w / 1280),
                                round(view.y + point[1] * view.h / 720))
                    main.handle_event(self.ui, pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=position))
                self.assertEqual(self.ui['game'].stage_index, stage)
                self.assertEqual(self.ui['game'].state, 'story' if number == 1 else 'intro')

    def test_quiet_shots_survive_mute_without_interrupting_voices(self):
        main.start_selected_stage(self.ui, 1)
        assets = self.ui['assets']
        assets['muted'] = False
        sounds = assets['sounds']
        for name, volume in (('shoot', .08), ('hit', .12), ('jump', .40)):
            self.assertAlmostEqual(sounds[name].get_volume(), volume, delta=.01)
        audio.start_music(assets)
        audio.play_sound(assets, 'hurt')
        for _ in range(30):
            audio.play_sound(assets, 'shoot')
        self.assertEqual(pygame.mixer.Channel(1).get_sound(), sounds['hurt'])
        self.assertEqual(pygame.mixer.Channel(0).get_sound(), sounds['music'])
        self.assertAlmostEqual(pygame.mixer.Channel(0).get_volume(), .12, delta=.01)
        main.button_action(self.ui, 'sound')
        self.assertFalse(pygame.mixer.Channel(1).get_busy())
        self.assertEqual(pygame.mixer.Channel(0).get_volume(), 0)
        main.button_action(self.ui, 'sound')
        self.assertAlmostEqual(sounds['shoot'].get_volume(), .08, delta=.01)
        self.assertAlmostEqual(pygame.mixer.Channel(0).get_volume(), .20, delta=.01)
        assets['muted'] = True
        audio.update_volume(assets)

    def test_pepper_collects_expires_and_resets_the_new_speed_in_all_stages(self):
        for number in (1, 2, 3):
            main.start_selected_stage(self.ui, number)
            game = self.enter_fight()
            self.assertEqual(game.player.shot_speed, 1350)
            for _ in range(122):
                game.step(.05, {})
            self.assertTrue(game.pepper.coletavel)
            game.player.x = game.pepper.retangulo.centerx
            game.step(.01, {'shoot': True})
            self.assertTrue(game.pepper.ativo)
            self.assertEqual(game.player.shot_speed, 1687.5)
            shot = game.player.shoot()
            self.assertAlmostEqual(math.hypot(shot.vx, shot.vy), 1687.5)
            game.pause()
            remaining = game.pepper.restante
            game.step(.05, {})
            self.assertEqual(game.pepper.restante, remaining)
            game.resume()
            for _ in range(161):
                game.step(.05, {})
            self.assertFalse(game.pepper.ativo)
            self.assertEqual(game.player.shot_speed, 1350)
            main.restart_stage(self.ui)
            self.assertEqual(game.player.shot_speed, 1350)
            self.assertEqual(game.player.hp, 3)


if __name__ == '__main__':
    unittest.main()
