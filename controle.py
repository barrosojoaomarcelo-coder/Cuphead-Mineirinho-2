"""Joystick/gamepad Pygame, sem dependências adicionais.

SDL GameController normaliza Xbox/PlayStation reconhecidos. Controles genéricos
usam o mapa editável abaixo. Teclado e mouse continuam no laço principal.

Interface: handle_event(evento, menu=False, paused=False) -> lista de teclas;
read_controls() -> dicionário das ações contínuas; desconectou indica remoção
do controle ativo no último evento. Chame handle_event para TODOS os eventos
JOY*/CONTROLLER*, inclusive os de conexão/desconexão.

A/Cruz: pular/confirmar; X/Quadrado: atirar; B/Círculo: dash/voltar;
Y/Triângulo: mirar para cima; Start/Options: pausa; Back/Select: voltar.
Analógico esquerdo ou direcional: mover, agachar e navegar nos menus.
R1/RB também atira; L1/LB também dá dash nos controles SDL reconhecidos.
"""
from __future__ import annotations
import pygame
try:
    from pygame._sdl2 import controller as controller_api
except ImportError:
    controller_api = None

ZONA_MORTA = 0.22
ZONA_SOLTAR_MENU = 0.14
EIXOS_GENERICOS = {'x': 0, 'y': 1}
BOTOES_GENERICOS = {'jump': 0, 'dash': 1, 'shoot': 2, 'up': 3,
                     'back': 6, 'start': 7}
ACOES = ('left', 'right', 'up', 'down', 'jump', 'shoot', 'dash')


def _tipo(nome):
    return getattr(pygame, nome, -999)


class ControleJoystick:
    def __init__(self):
        self.joystick = None
        self.controller = None
        self.instance_id = None
        self.nome = ''
        self.desconectou = False
        self._eixos_menu = {0: 0, 1: 0}
        self._hat_menu = (0, 0)
        self._em_menu = False
        self._bloqueados = set()
        pygame.joystick.init()
        if controller_api is not None:
            try:
                controller_api.init()
                controller_api.set_eventstate(True)
            except pygame.error:
                pass  # Um joystick genérico ainda pode funcionar.
        self._procurar()

    @property
    def conectado(self):
        return self.joystick is not None

    def _procurar(self):
        if self.conectado:
            return
        for index in range(pygame.joystick.get_count()):
            if self._abrir(index):
                return

    def _abrir(self, index):
        joy = None
        try:
            joy = pygame.joystick.Joystick(index)
            joy.init()
            identifier = joy.get_instance_id()
            normalized = None
            if controller_api is not None:
                try:
                    if controller_api.is_controller(index):
                        normalized = controller_api.Controller.from_joystick(joy)
                except pygame.error:
                    normalized = None
            self.joystick, self.controller = joy, normalized
            self.instance_id = identifier
            self.nome = joy.get_name()
            self._limpar_navegacao()
            return True
        except (pygame.error, IndexError):
            if joy is not None:
                try:
                    joy.quit()
                except pygame.error:
                    pass
            return False

    def _limpar_navegacao(self):
        self._eixos_menu = {0: 0, 1: 0}
        self._hat_menu = (0, 0)

    def fechar(self):
        for device in (self.controller, self.joystick):
            if device is not None:
                try:
                    device.quit()
                except pygame.error:
                    pass
        self.joystick = self.controller = None
        self.instance_id = None
        self.nome = ''
        self._bloqueados.clear()
        self._limpar_navegacao()

    @staticmethod
    def _valor_eixo(valor):
        value = float(valor)
        # Joystick usa float; SDL Controller.get_axis usa inteiro de 16 bits.
        if abs(value) > 1:
            value /= 32768.0
        return max(-1.0, min(1.0, value))

    def _botao(self, numero):
        if self.controller is not None:
            return bool(self.controller.get_button(numero))
        if numero < self.joystick.get_numbuttons():
            return bool(self.joystick.get_button(numero))
        return False

    def _eixo(self, numero):
        if self.controller is not None:
            return self._valor_eixo(self.controller.get_axis(numero))
        if numero < self.joystick.get_numaxes():
            return self._valor_eixo(self.joystick.get_axis(numero))
        return 0.0

    def read_controls(self):
        resultado = dict.fromkeys(ACOES, False)
        if not self.conectado:
            return resultado
        try:
            if self.controller is not None:
                x = self._eixo(pygame.CONTROLLER_AXIS_LEFTX)
                y = self._eixo(pygame.CONTROLLER_AXIS_LEFTY)
                esquerda = self._botao(pygame.CONTROLLER_BUTTON_DPAD_LEFT)
                direita = self._botao(pygame.CONTROLLER_BUTTON_DPAD_RIGHT)
                cima = self._botao(pygame.CONTROLLER_BUTTON_DPAD_UP)
                baixo = self._botao(pygame.CONTROLLER_BUTTON_DPAD_DOWN)
                resultado.update(
                    jump=self._botao(pygame.CONTROLLER_BUTTON_A),
                    shoot=(self._botao(pygame.CONTROLLER_BUTTON_X)
                           or self._botao(pygame.CONTROLLER_BUTTON_RIGHTSHOULDER)),
                    dash=(self._botao(pygame.CONTROLLER_BUTTON_B)
                          or self._botao(pygame.CONTROLLER_BUTTON_LEFTSHOULDER)),
                    up=self._botao(pygame.CONTROLLER_BUTTON_Y))
            else:
                x = self._eixo(EIXOS_GENERICOS['x'])
                y = self._eixo(EIXOS_GENERICOS['y'])
                hat = self.joystick.get_hat(0) if self.joystick.get_numhats() else (0, 0)
                esquerda, direita, cima, baixo = hat[0] < 0, hat[0] > 0, hat[1] > 0, hat[1] < 0
                for acao in ('jump', 'shoot', 'dash', 'up'):
                    resultado[acao] = self._botao(BOTOES_GENERICOS[acao])
            resultado.update(left=esquerda or x < -ZONA_MORTA,
                             right=direita or x > ZONA_MORTA,
                             up=resultado['up'] or cima or y < -ZONA_MORTA,
                             down=baixo or y > ZONA_MORTA)
        except (pygame.error, IndexError):
            # O evento de remoção pode chegar depois desta leitura.
            self.fechar()
            self.desconectou = True
        for acao in tuple(self._bloqueados):
            if not resultado[acao]:
                self._bloqueados.discard(acao)
            resultado[acao] = False
        return resultado

    def _navegar_eixo(self, eixo, valor):
        anterior = self._eixos_menu[eixo]
        if abs(valor) < ZONA_SOLTAR_MENU:
            atual = 0
        elif valor < -ZONA_MORTA:
            atual = -1
        elif valor > ZONA_MORTA:
            atual = 1
        else:
            atual = anterior
        self._eixos_menu[eixo] = atual
        if not atual or atual == anterior:
            return []
        return [((pygame.K_LEFT, pygame.K_RIGHT) if eixo == 0 else
                 (pygame.K_UP, pygame.K_DOWN))[1 if atual > 0 else 0]]

    def _tecla_botao(self, botao, menu, paused):
        if self.controller is not None:
            start, back = pygame.CONTROLLER_BUTTON_START, pygame.CONTROLLER_BUTTON_BACK
            confirm, cancel = pygame.CONTROLLER_BUTTON_A, pygame.CONTROLLER_BUTTON_B
            dpad = {pygame.CONTROLLER_BUTTON_DPAD_UP: pygame.K_UP,
                    pygame.CONTROLLER_BUTTON_DPAD_DOWN: pygame.K_DOWN,
                    pygame.CONTROLLER_BUTTON_DPAD_LEFT: pygame.K_LEFT,
                    pygame.CONTROLLER_BUTTON_DPAD_RIGHT: pygame.K_RIGHT}
        else:
            start, back = BOTOES_GENERICOS['start'], BOTOES_GENERICOS['back']
            confirm, cancel = BOTOES_GENERICOS['jump'], BOTOES_GENERICOS['dash']
            dpad = {}
        if botao == start:
            return [pygame.K_p if paused or not menu else pygame.K_RETURN]
        if botao == back:
            return [pygame.K_ESCAPE]
        if not menu:
            return []
        if botao == confirm:
            self._bloqueados.add('jump')
            return [pygame.K_RETURN]
        if botao == cancel:
            self._bloqueados.add('dash')
            return [pygame.K_ESCAPE]
        return [dpad[botao]] if botao in dpad else []

    def handle_event(self, evento, menu=False, paused=False):
        """Mapeia só eventos de controle; eventos de teclado não são duplicados.

        menu=True para title/story/paused/dead/victory/ajuda. paused=True
        faz Start devolver P (retornar à luta), em vez de confirmar a opção.
        O chamador pausa quando ``desconectou`` fica True durante uma luta.
        """
        self.desconectou = False
        if bool(menu) != self._em_menu:
            self._limpar_navegacao()
            self._em_menu = bool(menu)
        tipo = evento.type
        if tipo in (_tipo('JOYDEVICEADDED'), _tipo('CONTROLLERDEVICEADDED')):
            if not self.conectado:
                self._abrir(evento.device_index)
            return []
        if tipo in (_tipo('JOYDEVICEREMOVED'), _tipo('CONTROLLERDEVICEREMOVED')):
            identifier = getattr(evento, 'instance_id', None)
            if identifier == self.instance_id and self.conectado:
                self.fechar()
                self.desconectou = True
                self._procurar()
            return []
        if not self.conectado:
            return []
        identifier = getattr(evento, 'instance_id', getattr(evento, 'joy', None))
        if identifier is not None and identifier != self.instance_id:
            return []
        # SDL emite também eventos JOY para o mesmo aparelho: ignore duplicatas.
        if self.controller is not None:
            if tipo == _tipo('CONTROLLERBUTTONDOWN'):
                return self._tecla_botao(evento.button, menu, paused)
            if tipo == _tipo('CONTROLLERAXISMOTION') and menu and evento.axis in (0, 1):
                return self._navegar_eixo(evento.axis, self._valor_eixo(evento.value))
            return []
        if tipo == _tipo('JOYBUTTONDOWN'):
            return self._tecla_botao(evento.button, menu, paused)
        if tipo == _tipo('JOYAXISMOTION') and menu:
            for eixo, numero in enumerate((EIXOS_GENERICOS['x'], EIXOS_GENERICOS['y'])):
                if evento.axis == numero:
                    return self._navegar_eixo(eixo, self._valor_eixo(evento.value))
        if tipo == _tipo('JOYHATMOTION') and menu and evento.hat == 0:
            anterior = self._hat_menu
            self._hat_menu = evento.value
            teclas = []
            if evento.value[0] and evento.value[0] != anterior[0]:
                teclas.append(pygame.K_RIGHT if evento.value[0] > 0 else pygame.K_LEFT)
            if evento.value[1] and evento.value[1] != anterior[1]:
                teclas.append(pygame.K_UP if evento.value[1] > 0 else pygame.K_DOWN)
            return teclas
        return []
