"""Cartão de pausa independente para Pygame.

Depois de desenhar a luta no seu canvas:
    pausa.draw(canvas)

Passe eventos e, caso necessário, o ponto de mouse já convertido para as
coordenadas do canvas:
    acao = pausa.handle_event(evento, posicao_logica=ponto_no_canvas)

A ação será 'retornar', 'reiniciar', 'como_jogar', 'menu' ou None.
O componente não pausa o modelo, não reinicia a fase, não muda de tela, não
consome a fila de eventos e não chama display.flip(). Essas ações continuam
sob responsabilidade do laço principal do jogo.
"""
from __future__ import annotations

from collections.abc import Callable
import random
import pygame


class MenuPausa:
    """Quatro opções com navegação de teclado e mouse.

    ``fonte`` pode ser pygame.font.Font ou uma fábrica ``fonte(tamanho)``.
    Sem fonte externa, procura Georgia/serif bold instaladas no sistema.
    ``botoes`` expõe ``{acao: pygame.Rect}`` nas coordenadas do último destino
    de ``draw``. Desenhe uma vez antes de testar cliques de mouse.
    """

    OPCOES = (
        ('retornar', 'RETORNAR'),
        ('reiniciar', 'REINICIAR'),
        ('como_jogar', 'COMO JOGAR'),
        ('menu', 'MENU'),
    )
    CREME = '#e9dcc2'
    BORDA = '#89775b'
    BORDA_INTERNA = '#b6a180'
    TINTA = '#233c44'
    SELECAO = '#9d302c'

    def __init__(self, fonte: pygame.font.Font | Callable | None = None):
        pygame.font.init()
        self.foco = 0
        self.botoes: dict[str, pygame.Rect] = {}
        self.cartao = pygame.Rect(0, 0, 0, 0)
        self._fonte_externa = fonte
        self._fontes: dict[int, pygame.font.Font] = {}
        self._tamanho = None
        self._papel = None
        self._escurecimento = None
        self._textos = {}
        self._altura_letra = 32

    def reset(self):
        """Use ao abrir novamente a pausa para selecionar RETORNAR."""
        self.foco = 0

    def _fonte(self, tamanho):
        if tamanho not in self._fontes:
            if isinstance(self._fonte_externa, pygame.font.Font):
                fonte = self._fonte_externa
            elif self._fonte_externa is not None:
                fonte = self._fonte_externa(tamanho)
            else:
                caminho = pygame.font.match_font(
                    'georgia,liberationserif,dejavuserif,timesnewroman', bold=True)
                fonte = pygame.font.Font(caminho, tamanho)
            self._fontes[tamanho] = fonte
        return self._fontes[tamanho]

    def _layout(self, tamanho):
        if tamanho == self._tamanho:
            return
        self._tamanho = tamanho
        largura, altura = tamanho
        escala = min(largura / 1280, altura / 720)
        cw = max(1, round(640 * escala))
        ch = max(1, round(342 * escala))
        self.cartao = pygame.Rect(0, 0, cw, ch)
        self.cartao.center = (largura // 2, altura // 2)
        self._altura_letra = max(12, round(34 * escala))
        self._textos.clear()
        self.botoes.clear()
        passo = ch * .178
        for i, (acao, _) in enumerate(self.OPCOES):
            botao = pygame.Rect(0, 0, round(cw * .83), max(1, round(passo)))
            botao.center = (self.cartao.centerx,
                            round(self.cartao.top + ch * .235 + i * passo))
            self.botoes[acao] = botao
        self._escurecimento = pygame.Surface(tamanho, pygame.SRCALPHA)
        self._escurecimento.fill((19, 13, 19, 132))
        self._papel = pygame.Surface((cw, ch))
        self._papel.fill(self.CREME)
        # Grão discreto do papel, calculado uma vez por tamanho de canvas.
        rng = random.Random(1930)
        for _ in range(max(1, cw * ch // 43)):
            x, y = rng.randrange(cw), rng.randrange(ch)
            cor = rng.choice(('#e1d3b9', '#e5d7bd', '#ecdfc7'))
            self._papel.set_at((x, y), cor)
        espaco = max(3, round(8 * escala))
        pygame.draw.rect(self._papel, self.BORDA,
                         self._papel.get_rect().inflate(-2, -2),
                         max(1, round(2 * escala)))
        pygame.draw.rect(self._papel, self.BORDA_INTERNA,
                         self._papel.get_rect().inflate(-espaco * 2, -espaco * 2), 1)

    def _texto(self, label, cor):
        chave = (label, cor)
        if chave not in self._textos:
            texto = self._fonte(self._altura_letra).render(label, True, cor)
            # Uma Font externa de tamanho fixo também acompanha o canvas.
            altura_alvo = max(10, self._altura_letra)
            fator = altura_alvo / max(1, texto.get_height())
            largura = max(1, round(texto.get_width() * fator))
            largura_maxima = max(1, round(self.cartao.w * .70))
            if largura > largura_maxima:
                fator *= largura_maxima / largura
            texto = pygame.transform.smoothscale(texto, (
                max(1, round(texto.get_width() * fator)),
                max(1, round(texto.get_height() * fator))))
            self._textos[chave] = texto
        return self._textos[chave]

    def draw(self, destino: pygame.Surface):
        """Escurece a luta e desenha somente o cartão e suas quatro opções.

        Redesenhe a luta normalmente antes de chamar este método em cada quadro.
        O tamanho do destino, a câmera e as coordenadas da arena não são alterados.
        """
        self._layout(destino.get_size())
        destino.blit(self._escurecimento, (0, 0))
        escala = min(destino.get_width() / 1280, destino.get_height() / 720)
        sombra = self.cartao.move(max(1, round(5 * escala)),
                                   max(1, round(7 * escala)))
        camada_sombra = pygame.Surface(destino.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(camada_sombra, (15, 9, 12, 94), sombra)
        destino.blit(camada_sombra, (0, 0))
        destino.blit(self._papel, self.cartao)
        for i, (acao, label) in enumerate(self.OPCOES):
            retangulo = self.botoes[acao]
            cor = self.SELECAO if i == self.foco else self.TINTA
            texto = self._texto(label, cor)
            destino.blit(texto, texto.get_rect(center=retangulo.center))
            if i == self.foco:
                # Duas pequenas marcas mantêm a seleção perceptível sem caixa.
                espaco = max(8, round(17 * escala))
                tamanho = max(2, round(3 * escala))
                for sinal in (-1, 1):
                    x = texto.get_rect(center=retangulo.center).centerx + sinal * (
                        texto.get_width() // 2 + espaco)
                    pygame.draw.circle(destino, self.SELECAO,
                                       (x, retangulo.centery), tamanho)

    def handle_event(self, evento, posicao_logica=None):
        """Retorna a ação confirmada; ``posicao_logica`` já deve estar no canvas."""
        if evento.type == pygame.KEYDOWN:
            tecla = evento.key
            if tecla in (pygame.K_ESCAPE, pygame.K_p):
                return 'retornar'
            if tecla in (pygame.K_UP, pygame.K_w):
                self.foco = (self.foco - 1) % len(self.OPCOES)
            elif tecla in (pygame.K_DOWN, pygame.K_s):
                self.foco = (self.foco + 1) % len(self.OPCOES)
            elif tecla == pygame.K_TAB:
                sentido = -1 if getattr(evento, 'mod', 0) & pygame.KMOD_SHIFT else 1
                self.foco = (self.foco + sentido) % len(self.OPCOES)
            elif tecla in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return self.OPCOES[self.foco][0]
        elif evento.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button != 1:
                return None
            ponto = posicao_logica if posicao_logica is not None else evento.pos
            for indice, (acao, _) in enumerate(self.OPCOES):
                retangulo = self.botoes.get(acao)
                if retangulo is not None and retangulo.collidepoint(ponto):
                    self.foco = indice
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        return acao
                    break
        return None
