"""Desenho, animações e interface visual. Frente: Davi.

As artes e o manifesto vêm do ZIP do grupo. Não altera regras da luta.
"""
import math
import pygame
from config import WIDTH, HEIGHT, FLOOR, STAGE_ORDER, GAME_TITLE, CREATORS_LABEL
from engine import STAGES
from pausa_menu import MenuPausa
from poder_pimenta import desenhar_vidas
from comilao import draw_comilao_warning
from piramide_attacks import draw_piramide_warning

INK = (49, 30, 28)
CREAM = (255, 236, 192)
GOLD = (255, 193, 76)
RED = (172, 46, 37)


class Renderer:
    """Carrega as imagens uma vez e mantém os quadros prontos para desenhar."""

    def __init__(self, assets):
        self.assets = assets
        self.day = assets['day']
        self.night = assets['night']
        self.fonts = {}
        self.pause_menu = MenuPausa(fonte=lambda size: self.font(size, True))
        self.time = 0
        self.particles = []
        self.shake = 0
        self.flash = 0
        self.buttons = {}
        self.previous_hp = 3
        self.previous_shots = 0
        self.previous_hits = 0
        self.previous_state = 'title'
        self.layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def font(self, size, serif=False):
        """Usa fontes do sistema, com substituição automática do Pygame."""
        key = size, serif
        if key not in self.fonts:
            self.fonts[key] = pygame.font.SysFont('Georgia' if serif else 'Arial', size, bold=True)
        return self.fonts[key]

    def text(self, target, message, position, size=24, color=CREAM, center=False, serif=False, outline=False):
        """Desenha texto com contorno opcional para leitura sobre o cenário."""
        font = self.font(size, serif)
        image = font.render(str(message), True, color)
        rect = image.get_rect(center=position) if center else image.get_rect(topleft=position)
        if outline:
            shadow = font.render(str(message), True, INK)
            for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                target.blit(shadow, rect.move(dx, dy))
        target.blit(image, rect)
        return rect

    def emit(self, x, y, count):
        """Partículas decorativas, limitadas para não acumular na memória."""
        for index in range(count):
            angle = index / count * math.tau + self.time
            speed = 40 + index * 37 % 110
            self.particles.append({'x': x, 'y': y, 'vx': math.cos(angle) * speed,
                                   'vy': math.sin(angle) * speed - 30, 'life': .5, 'r': 3 + index % 4})
        self.particles = self.particles[-170:]

    def update(self, dt, model):
        """Compara vida e contadores para desenhar efeitos, sem fila de eventos."""
        if model.state == 'paused':
            return
        p = model.player
        self.time += dt
        if p.hp < self.previous_hp:
            self.shake = .25
            self.flash = .14
            self.emit(p.x, p.y - 60, 12)
        if model.stats['shots'] > self.previous_shots:
            self.emit(p.x + 65 * p.facing, p.y - 83, 2)
        if model.stats['hits'] > self.previous_hits:
            self.emit(1040, 400, 3)
        if model.state == 'transform' and self.previous_state != 'transform':
            self.shake = .4
        if model.state == 'intro' and self.previous_state != 'intro':
            self.particles.clear()
        self.previous_hp = p.hp
        self.previous_shots = model.stats['shots']
        self.previous_hits = model.stats['hits']
        self.previous_state = model.state
        self.shake = max(0, self.shake - dt)
        self.flash = max(0, self.flash - dt)
        for particle in list(self.particles):
            particle['life'] -= dt
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['vy'] += 70 * dt
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw(self, target, model, muted=False, best=None, instructions=False, audio_available=True):
        """Desenha arena, indicadores e botões; devolve mapa de áreas clicáveis."""
        target.blit(self.day, (0, 0))
        if model.stage_index == 2:
            target.blit(self.assets['pyramid'], (0, 0))
            self.layer.fill((10, 1, 28, round(model.night * 65)))
            target.blit(self.layer, (0, 0))
        elif model.stage_index == 1:
            target.blit(self.assets['valley'], (0, 0))
        elif model.night > 0:
            self.night.set_alpha(round(model.night * 255))
            target.blit(self.night, (0, 0))
        model.boss_group.draw(target)
        self._warnings(target, model)
        self._horizontal_cues(target, model)
        pygame.draw.ellipse(target, (70, 53, 43), (round(model.player.x - 34), FLOOR - 2, 68, 8))
        if model.player.dash > 0:
            p = model.player
            for index in range(3):
                x = p.x - p.dash_direction * (40 + index * 22)
                pygame.draw.line(target, CREAM, (x, p.y - 35 - index * 12),
                                 (x - p.dash_direction * 35, p.y - 35 - index * 12), 3)
        if model.state in ('playing', 'paused', 'transform'):
            model.pepper.desenhe_coletavel(target)
        model.player_group.draw(target)
        self._draw_shots(target, model)
        model.beams.draw(target)
        model.fire.draw(target)
        model.minions.draw(target)
        warning = model.boss.warning
        if warning is not None and warning['type'] == 'giant':
            charge = 1 - warning['remaining'] / warning['total']
            self._orb(target, warning['x'], warning['y'], 8 + charge * 33, warning['angle'], True)
        for p in self.particles:
            radius = max(1, round(p['r'] * min(1, p['life'] * 3)))
            x, y = round(p['x']), round(p['y'])
            if p['r'] >= 5:
                pygame.draw.polygon(target, GOLD, [(x, y-radius*2), (x+radius, y-radius),
                    (x+radius*2, y), (x+radius, y+radius), (x, y+radius*2),
                    (x-radius, y+radius), (x-radius*2, y), (x-radius, y-radius)])
            else:
                pygame.draw.circle(target, GOLD, (x, y), radius)
        if model.state == 'transform':
            # Nuvem cartunesca na troca de forma; cresce e desaparece junto da transição.
            strength = math.sin(model.boss.transform * math.pi)
            for index in range(7):
                x = 960 + index * 43
                y = 560 - math.sin(index * 2 + self.time * 8) * 22
                radius = round((25 + index % 3 * 8) * strength)
                if radius > 0:
                    pygame.draw.circle(target, INK, (round(x), round(y)), radius + 3)
                    pygame.draw.circle(target, CREAM, (round(x), round(y)), radius)
        if self.flash > 0:
            self.layer.fill((255, 235, 194, round(self.flash * 300)))
            target.blit(self.layer, (0, 0))
        if self.shake > 0:
            offset = (round(math.sin(self.time * 95) * self.shake * 12), round(math.cos(self.time * 81) * self.shake * 8))
            target.blit(target.copy(), offset)
        self.buttons = {}
        self._hud(target, model, muted, audio_available)
        if model.state == 'intro':
            self.text(target, 'VAI COMEÇAR!', (640, 300), 64, GOLD, True, True, True)
            self.text(target, f'FASE {STAGE_ORDER.index(model.stage_index) + 1} — {STAGES[model.stage_index]}',
                      (640, 365), 28, CREAM, True, outline=True)
        if model.state == 'transform' and .2 < model.boss.transform < .8:
            title = 'O DESPERTAR' if model.stage_index == 0 else 'FOME SEM FIM'
            subtitle = 'A noite chegou ao castelo' if model.stage_index == 0 else 'Cuidado com a língua e os espinhos!'
            if model.stage_index == 2:
                title, subtitle = 'O OLHAR SE DIVIDE', 'Dois olhos, um só inimigo. Observe os trajetos!'
            self.text(target, title, (640, 280), 60, GOLD, True, True, True)
            self.text(target, subtitle, (640, 345), 24, CREAM, True, outline=True)
        if instructions:
            self._instructions(target)
        elif model.state == 'story':
            self._story(target)
        elif model.state == 'paused':
            self.pause_menu.draw(target)
            self.buttons.update(self.pause_menu.botoes)
        elif model.state in ('title', 'dead', 'victory'):
            self._overlay(target, model, best)
        return self.buttons.copy()

    def _draw_shots(self, target, model):
        """O tiro conserva seu tipo de desenho desde o instante do disparo."""
        for shot in model.shots:
            if getattr(shot, 'is_pepper', False):
                image = model.pepper.sprite_projetil(shot.pepper_direction)
                target.blit(image, image.get_rect(center=shot.rect.center))
            else:
                target.blit(shot.image, shot.rect)

    def _warnings(self, target, model):
        """Desenha os avisos de cada chefe usando os pontos já definidos pelos ataques."""
        for w in model.warnings:
            if w['fired']:
                continue
            color = GOLD if int(self.time * 8) % 2 else CREAM
            if w['type'] == 'piramide':
                draw_piramide_warning(self, target, w, color)
                continue
            if w['type'] == 'comilao':
                draw_comilao_warning(self, target, w, color)
                continue
            if w['type'] == 'horizontal':
                continue
            if w['type'] == 'rain':
                for x in w['lanes']:
                    for y in range(65, FLOOR, 24):
                        pygame.draw.line(target, color, (x, y), (x, y + 10), 2)
                pygame.draw.line(target, (191, 225, 151), (w['safe_x'] - 150, FLOOR), (w['safe_x'] + 150, FLOOR), 6)
            else:
                end = (w['end_x'], w['end_y']) if w['type'] == 'flame' else (w['x'] + math.cos(w['angle']) * 1200, w['y'] + math.sin(w['angle']) * 1200)
                start = pygame.Vector2(w['x'], w['y'])
                delta = pygame.Vector2(end) - start
                for part in range(0, 100, 3):
                    pygame.draw.line(target, color, start + delta * (part / 100), start + delta * ((part + 1) / 100), 2)
            # O trajeto visual é mantido; o cabeçalho de instruções foi removido.

    def _horizontal_cues(self, target, model):
        """Mostra a altura da fileira atual do dragão durante preparação e disparo."""
        chain = model.boss.horizontal
        if chain is None:
            return
        rows = chain['rows']
        index = chain['row_index']
        row = rows[index]
        if chain['state'] == 'recover':
            return
        for x in range(30, 930, 30):
            pygame.draw.line(target, GOLD, (x, row['y']), (x + 10, row['y']), 2)
        # Somente o aviso no cenário, sem texto/contador no topo.

    def _orb(self, target, x, y, radius, angle, giant=False):
        """Desenha a bola de fogo decorativa que antecipa o disparo de uma gigante."""
        r = max(3, round(radius))
        direction = pygame.Vector2(math.cos(angle), math.sin(angle))
        normal = pygame.Vector2(-direction.y, direction.x)
        center = pygame.Vector2(x, y)
        tail = [center + normal * r * .8, center - direction * r * 2.7, center - normal * r * .8]
        pygame.draw.polygon(target, INK, tail)
        pygame.draw.polygon(target, (237, 102, 41), [center + normal * r * .6, center - direction * r * 2.4, center - normal * r * .6])
        point = round(x), round(y)
        pygame.draw.circle(target, INK, point, r + (3 if giant else 2))
        pygame.draw.circle(target, (246, 138, 44), point, r)
        pygame.draw.circle(target, (255, 204, 85), point, max(1, round(r * .75)))
        pygame.draw.circle(target, (255, 240, 181), (round(x + r * .15), round(y - r * .1)), max(1, round(r * .4)))

    def _button(self, target, name, label, rect, primary=False):
        """Desenha o botão e registra seu retângulo lógico para tratar cliques."""
        rect = pygame.Rect(rect)
        pygame.draw.rect(target, INK, rect.move(0, 5), border_radius=7)
        pygame.draw.rect(target, GOLD if primary else CREAM, rect, border_radius=7)
        pygame.draw.rect(target, INK, rect, 2, border_radius=7)
        self.text(target, label, rect.center, 22, INK, True)
        self.buttons[name] = rect

    def _hud(self, target, model, muted, audio_available):
        """A arena ocupa o canvas inteiro; só as três vidas ficam sobre ela."""
        desenhar_vidas(target, model.player.hp)

    def _panel(self, target, rect):
        """Escurece a arena e devolve o retângulo do painel informativo desenhado."""
        self.layer.fill((24, 15, 18, 125))
        target.blit(self.layer, (0, 0))
        panel = pygame.Rect(rect)
        pygame.draw.rect(target, INK, panel.move(0, 8), border_radius=16)
        pygame.draw.rect(target, CREAM, panel, border_radius=16)
        pygame.draw.rect(target, INK, panel, 4, border_radius=16)
        return panel

    def _overlay(self, target, model, best):
        """Mostra início antigo, derrota ou vitória, respeitando a ordem atual dos chefes."""
        self._panel(target, (80, 158, 720, 445))
        state = model.state
        final = model.stage_index == STAGE_ORDER[-1]
        title = {'title': GAME_TITLE,
                 'dead': 'Essa foi por pouco...', 'victory': 'NOCAUTE!'}[state]
        if state == 'victory' and final:
            title = 'AVENTURA CONCLUÍDA!'
        badge = 'UM DUELO À MODA MINEIRA' if state == 'title' else 'FIM DO DUELO'
        self.text(target, badge, (120, 186), 19, RED)
        self.text(target, title, (120, 228), 42, INK, serif=True)
        if state == 'title':
            lines = ('Três cenários. Três chefes. Uma aventura mineira.',
                     'Olho da Pirâmide → Comilão → Dragão Vermelho.',
                     'Jogo estudantil inspirado em Cuphead e Mineirinho.')
            label = 'COMEÇAR A AVENTURA'
        elif state == 'dead':
            lines = ('Respire, observe os ataques e tente de novo.',
                     'Use os avisos, o pulo, o agachamento e o dash.',
                     'Você recomeça esta fase com três vidas.')
            label = 'TENTAR NOVAMENTE'
        elif final:
            lines = ('Dragão Vermelho derrotado!',
                     'O castelo voltou a ficar em paz.',
                     'Obrigado por jogar Mineirinho!')
            label = 'VOLTAR AO MENU'
        else:
            next_position = STAGE_ORDER.index(model.stage_index) + 1
            next_name = STAGES[STAGE_ORDER[next_position]]
            lines = (f'{STAGES[model.stage_index]} derrotado!',
                     f'O próximo duelo é contra {next_name}.',
                     'Enter avança; R repete esta fase.')
            label = f'IR PARA A FASE {next_position + 1}'
        for i, line in enumerate(lines):
            self.text(target, line, (120, 298 + i * 32), 22, INK)
        self._button(target, 'play', label, (120, 454, 350, 54), True)
        self._button(target, 'instructions', 'COMO JOGAR', (490, 454, 270, 54))
        if state == 'title':
            self._button(target, 'practice', 'TREINAR A FASE 2', (120, 518, 350, 36))
            self._button(target, 'practice3', 'TREINAR A FASE 3', (490, 518, 270, 36))
        else:
            self.text(target, 'ENTER CONTINUAR    R REPETIR FASE    ESC MENU', (120, 545), 17, INK)
        self.text(target, CREATORS_LABEL, (120, 574), 16, RED)

    def _instructions(self, target):
        """Desenha controles e dica da pimenta e registra o botão de voltar."""
        self._panel(target, (230, 115, 820, 510))
        self.text(target, 'COMO JOGAR', (640, 158), 38, INK, True, True)
        rows = [('Mover / agachar', 'A e D ou setas / S ou seta para baixo'),
                ('Pular', 'Espaço ou Z; segure para ir mais alto'),
                ('Atirar', 'J ou X; pode segurar'),
                ('Mirar para cima', 'W ou seta para cima; combine com A/D'),
                ('Dash / esquiva', 'Shift ou K; aguarde a recarga'),
                ('Pausar / som', 'P ou Esc / M'),
                ('Reiniciar / tela cheia', 'R / F11'),
                ('Controle — mover', 'Analógico esquerdo ou direcional'),
                ('Controle — ações', 'Inferior: pulo | esquerdo: tiro | direito: dash'),
                ('Controle — pausa', 'Start/Options; inferior confirma menus')]
        for i, (label, keys) in enumerate(rows):
            self.text(target, label, (265, 209 + i * 29), 18, RED)
            self.text(target, keys, (515, 209 + i * 29), 17, INK)
        self.text(target, 'Colete a pimenta: tiros rápidos por 8 segundos.', (640, 505), 22, INK, True)
        self._button(target, 'back', 'VOLTAR  [ESC]', (490, 551, 300, 48), True)

    def _story(self, target):
        """Apresenta a narrativa da campanha antes da primeira luta, contra a Pirâmide."""
        self._panel(target, (180, 140, 920, 470))
        self.text(target, 'ANTES DO PRIMEIRO DUELO', (640, 185), 20, RED, True)
        self.text(target, 'Uma jornada por três cenários', (640, 236), 38, INK, True, True)
        lines = ('A jornada começa nas ruínas do Olho da Pirâmide.',
                 'Depois, o Chefe Comilão espera no vale rochoso.',
                 'Por fim, o Dragão Vermelho espera no castelo.',
                 'Observe os ataques e use a pimenta na hora certa.')
        for index, line in enumerate(lines):
            self.text(target, line, (640, 310 + index * 37), 23, INK, True)
        self._button(target, 'play', 'ENFRENTAR A PIRÂMIDE', (260, 495, 400, 55), True)
        self._button(target, 'menu', 'VOLTAR AO MENU', (680, 495, 320, 55))
        self.text(target, 'ENTER CONTINUAR     ESC MENU', (640, 580), 18, RED, True)
