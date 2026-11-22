"""Desenho, animações e interface visual. Frente: Davi.

As artes e o manifesto vêm do ZIP do grupo. Não altera regras da luta.
"""
import math
import pygame
from config import WIDTH, HEIGHT, FLOOR, DASH_COOLDOWN, clamp

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
        if model.night > 0:
            self.night.set_alpha(round(model.night * 255))
            target.blit(self.night, (0, 0))
        model.boss_group.draw(target)
        self._warnings(target, model)
        pygame.draw.ellipse(target, (70, 53, 43), (round(model.player.x - 34), FLOOR - 2, 68, 8))
        model.player_group.draw(target)
        model.shots.draw(target)
        model.beams.draw(target)
        model.fire.draw(target)
        warning = model.boss.warning
        if warning is not None and warning['type'] == 'giant':
            charge = 1 - warning['remaining'] / warning['total']
            self._orb(target, warning['x'], warning['y'], 8 + charge * 33, warning['angle'], True)
        p = model.player
        if p.dash_cooldown > 0:
            rect = pygame.Rect(round(p.x - 10), round(p.y + 5), 20, 20)
            progress = max(.01, 1 - p.dash_cooldown / DASH_COOLDOWN)
            pygame.draw.arc(target, CREAM, rect, -math.pi / 2, -math.pi / 2 + math.tau * progress, 3)
        for p in self.particles:
            pygame.draw.circle(target, GOLD, (round(p['x']), round(p['y'])), max(1, round(p['r'] * min(1, p['life'] * 3))))
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
        if model.state == 'transform' and .2 < model.boss.transform < .8:
            self.text(target, 'O DESPERTAR', (640, 280), 60, GOLD, True, True, True)
            self.text(target, 'A noite chegou ao castelo', (640, 345), 24, CREAM, True, outline=True)
        if instructions:
            self._instructions(target)
        elif model.state in ('title', 'paused', 'dead', 'victory'):
            self._overlay(target, model, best)
        return self.buttons.copy()

    def _warnings(self, target, model):
        for w in model.warnings:
            if w['fired']:
                continue
            color = GOLD if int(self.time * 8) % 2 else CREAM
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
            if w.get('guidance'):
                jump_now = w['type'] == 'flame' and w['mode'] == 'low' and w['remaining'] < .2
                self.text(target, 'PULE AGORA!' if jump_now else w['guidance'], (640, 105), 30 if jump_now else 23,
                          GOLD, True, outline=True)

    def _orb(self, target, x, y, radius, angle, giant=False):
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
        rect = pygame.Rect(rect)
        pygame.draw.rect(target, INK, rect.move(0, 5), border_radius=7)
        pygame.draw.rect(target, GOLD if primary else CREAM, rect, border_radius=7)
        pygame.draw.rect(target, INK, rect, 2, border_radius=7)
        self.text(target, label, rect.center, 22, INK, True)
        self.buttons[name] = rect

    def _hud(self, target, model, muted, audio_available):
        pygame.draw.rect(target, INK, (0, 0, WIDTH, 65))
        self.text(target, 'FORNALHA DO CASTELO', (25, 18), 23, GOLD, serif=True)
        for i in range(3):
            x = 410 + i * 35
            color = RED if i < model.player.hp else (87, 68, 58)
            pygame.draw.circle(target, color, (x - 6, 25), 9)
            pygame.draw.circle(target, color, (x + 6, 25), 9)
            pygame.draw.polygon(target, color, [(x - 14, 29), (x + 14, 29), (x, 47)])
        minutes, seconds = divmod(int(model.elapsed), 60)
        self.text(target, f'{minutes:02d}:{seconds:02d}', (570, 19), 24)
        self.text(target, 'O DESPERTAR' if model.boss.phase >= 3 else 'DRAGÃO VERMELHO', (695, 22), 19)
        sound_label = 'SOM: SIM'
        if muted:
            sound_label = 'SOM: NÃO'
        if not audio_available:
            sound_label = 'SEM ÁUDIO'
        self._button(target, 'sound', sound_label, (1065, 10, 185, 40))
        pygame.draw.rect(target, INK, (0, 674, WIDTH, 46))
        self.text(target, 'A/D  MOVER    ESPAÇO  PULAR    J  ATIRAR    W  MIRAR    SHIFT  DASH    P  PAUSA    R  REINICIAR', (640, 698), 18, CREAM, True)

    def _panel(self, target, rect):
        self.layer.fill((24, 15, 18, 125))
        target.blit(self.layer, (0, 0))
        panel = pygame.Rect(rect)
        pygame.draw.rect(target, INK, panel.move(0, 8), border_radius=16)
        pygame.draw.rect(target, CREAM, panel, border_radius=16)
        pygame.draw.rect(target, INK, panel, 4, border_radius=16)
        return panel

    def _overlay(self, target, model, best):
        self._panel(target, (80, 158, 720, 445))
        state = model.state
        badges = {'title': 'UM DUELO À MODA MINEIRA', 'paused': 'PARTIDA PAUSADA'}
        badge = badges.get(state, 'FIM DO DUELO')
        title = {'title': 'A Fornalha do Castelo', 'paused': 'Uma pausa para respirar', 'dead': 'Essa foi por pouco...', 'victory': 'NOCAUTE!'}[state]
        self.text(target, badge, (120, 186), 19, RED)
        self.text(target, title, (120, 228), 42 if state != 'paused' else 36, INK, serif=True)
        lines = {
            'title': ('Três vidas. Um dragão. Muito pão de queijo.', 'Observe os avisos e encontre a hora de atacar.', 'Jogo estudantil inspirado na ação de Cuphead.'),
            'paused': ('A batalha espera por você.', 'Pressione P ou Esc para continuar.', 'Use F11 para alternar a tela cheia.'),
            'dead': ('Respire, observe os ataques e tente de novo.', 'Pule as rajadas baixas; fique no chão nas altas.', 'O dash oferece uma breve proteção.'),
            'victory': ('O Dragão Vermelho foi derrotado!', 'Você venceu as duas formas da primeira luta.', 'Obrigado por jogar.'),
        }[state]
        for i, line in enumerate(lines):
            self.text(target, line, (120, 298 + i * 32), 22, INK)
        if state in ('dead', 'victory'):
            accuracy = round(model.stats['hits'] / model.stats['shots'] * 100) if model.stats['shots'] else 0
            self.text(target, f'TEMPO {model.elapsed:.1f}s  |  PRECISÃO {accuracy}%', (120, 406), 20, RED)
        elif best is not None:
            self.text(target, f'MELHOR TEMPO: {best:.1f}s', (120, 406), 20, RED)
        labels = {'paused': 'CONTINUAR', 'title': 'COMEÇAR O DUELO'}
        label = labels.get(state, 'TENTAR NOVAMENTE')
        self._button(target, 'play', label, (120, 454, 350, 54), True)
        self._button(target, 'instructions', 'COMO JOGAR', (490, 454, 270, 54))
        self.text(target, 'ENTER  JOGAR / CONTINUAR     H  AJUDA     F11  TELA CHEIA', (120, 545), 17, INK)
        self.text(target, 'Davi  •  Moisés  •  João Marcelo', (120, 574), 16, RED)

    def _instructions(self, target):
        self._panel(target, (230, 115, 820, 510))
        self.text(target, 'COMO JOGAR', (640, 158), 38, INK, True, True)
        rows = [('Mover / agachar', 'A e D ou setas / S ou seta para baixo'),
                ('Pular', 'Espaço ou Z; segure para ir mais alto'),
                ('Atirar', 'J ou X; pode segurar'),
                ('Mirar para cima', 'W ou seta para cima; combine com A/D'),
                ('Dash / esquiva', 'Shift ou K; aguarde a recarga'),
                ('Pausar / som', 'P ou Esc / M'),
                ('Reiniciar / tela cheia', 'R / F11')]
        for i, (label, keys) in enumerate(rows):
            self.text(target, label, (265, 211 + i * 38), 21, RED)
            self.text(target, keys, (515, 211 + i * 38), 20, INK)
        self.text(target, 'Acerte o dragão e sobreviva às duas formas para vencer.', (640, 505), 22, INK, True)
        self._button(target, 'back', 'VOLTAR  [ESC]', (490, 551, 300, 48), True)
