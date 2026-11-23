"""Bônus de pimenta independente do motor: a integração passa retângulos e valores.

Não faz suposições sobre game.player, listas de tiros ou cooldowns do seu engine.
Chame reiniciar() no começo de CADA luta, atualize() somente com tempo de combate,
e use perfil_tiro() ao criar tiros novos. Salve tipo_projetil em cada tiro para
os que já estavam voando conservarem o sprite com que foram disparados.
"""
from dataclasses import dataclass
import math
from pathlib import Path
import pygame


@dataclass(frozen=True)
class RegrasPimenta:
    """Parâmetros imutáveis de duração, reaparição, dimensões e multiplicadores da pimenta."""
    duracao: float = 8.0
    tempo_na_tela: float = 5.0
    multiplicador_cadencia: float = 1.5
    multiplicador_velocidade: float = 1.25
    primeira_coleta_em: float = 6.0
    reaparecer_em: float = 20.0
    tamanho_coleta: int = 52
    tamanho_tiro: int = 36

    def __post_init__(self):
        if min(self.duracao,self.tempo_na_tela,self.multiplicador_cadencia,self.multiplicador_velocidade,
               self.primeira_coleta_em,self.reaparecer_em,self.tamanho_coleta,self.tamanho_tiro)<=0:
            raise ValueError('As regras da pimenta devem ser positivas.')


class PoderPimenta:
    """Um coletável por vez; atualização pausa junto com a luta.

    arena: pygame.Rect da área jogável real; chao_y: coordenada do piso.
    jogador_rect: retângulo de colisão real passado pelo seu motor.
    Não altera vida, dano, colisão, velocidade de movimento nem dash do jogador.
    """
    def __init__(self, arena, chao_y, *, regras=None, imagem=None):
        self.regras=regras or RegrasPimenta()
        if isinstance(imagem, pygame.Surface):
            desenho=imagem.copy()
        else:
            caminho=Path(imagem) if imagem else Path(__file__).resolve().parent/'assets/powerups/pimenta.png'
            desenho=pygame.image.load(str(caminho))
        if pygame.display.get_surface(): desenho=desenho.convert_alpha()
        desenho=desenho.subsurface(desenho.get_bounding_rect(min_alpha=10)).copy()
        self.imagem=desenho
        self.coleta_sprite=self._ajustar(desenho,self.regras.tamanho_coleta)
        # Tip aponta para a direita após girar o sprite diagonal original.
        horizontal=pygame.transform.rotate(desenho,135)
        horizontal=horizontal.subsurface(horizontal.get_bounding_rect(min_alpha=10)).copy()
        self.tiro_direita=self._ajustar(horizontal,self.regras.tamanho_tiro)
        self._sprites={}
        self.reiniciar(arena,chao_y)

    @staticmethod
    def _ajustar(imagem,maior_lado):
        fator=maior_lado/max(imagem.get_size())
        return pygame.transform.smoothscale(imagem,(max(1,round(imagem.get_width()*fator)),
                                                      max(1,round(imagem.get_height()*fator))))

    def reiniciar(self,arena=None,chao_y=None):
        """Limpa o bônus e inicia a espera da primeira coleta dentro da arena recebida."""
        if arena is not None: self.arena=pygame.Rect(arena)
        if chao_y is not None: self.chao_y=float(chao_y)
        if self.arena.w<self.regras.tamanho_coleta or self.arena.h<self.regras.tamanho_coleta:
            raise ValueError('Arena pequena demais para o coletável.')
        self.tempo=0.0
        self.restante=0.0
        self.espera=self.regras.primeira_coleta_em
        self.coletavel=False
        self.visivel_restante=0.0
        self.numero_coletas=0
        self.retangulo=pygame.Rect(0,0,self.regras.tamanho_coleta-10,self.regras.tamanho_coleta-10)
        self._posicionar()

    def _posicionar(self):
        # Fica na região central alcançável; evite posições ocupadas por chefes
        # passando uma arena segura adequada a cada fase na integração.
        frac=.34 if self.numero_coletas%2==0 else .62
        self.retangulo.center=(round(self.arena.left+self.arena.w*frac),round(self.chao_y-38))
        self.retangulo.clamp_ip(self.arena)
        self._centro_base=self.retangulo.center

    def ajustar_arena(self,arena,chao_y):
        """Atualiza limites após a transformação sem renovar os temporizadores."""
        arena=pygame.Rect(arena)
        if arena.w<self.regras.tamanho_coleta or arena.h<self.regras.tamanho_coleta:
            raise ValueError('Arena pequena demais para o coletável.')
        self.arena=arena
        self.chao_y=float(chao_y)
        base=self.retangulo.copy()
        base.center=(self._centro_base[0],round(self.chao_y-38))
        base.clamp_ip(arena)
        self._centro_base=base.center
        self.retangulo.clamp_ip(arena)

    @property
    def ativo(self): return self.restante>0

    @property
    def tipo_projetil(self): return 'pimenta' if self.ativo else 'pao'

    def atualize(self,dt,jogador_rect,*,em_combate=True):
        """Retorna ('coletou_pimenta',) UMA vez por coleta, senão ().

        dt em segundos. Pausa, introdução, transformação, derrota e vitória:
        passe em_combate=False para congelar coleta, animação e temporizador.
        """
        if dt<0 or not math.isfinite(dt): raise ValueError('dt deve ser finito e não negativo.')
        if not em_combate or dt==0: return ()
        self.tempo+=dt
        self.restante=max(0.0,self.restante-dt)
        surgiu_agora=False
        if not self.coletavel:
            self.espera=max(0.0,self.espera-dt)
            if self.espera<=0:
                self.coletavel=True
                self.visivel_restante=self.regras.tempo_na_tela
                surgiu_agora=True
                self._posicionar()
        if self.coletavel:
            if not surgiu_agora:
                self.visivel_restante=max(0.0,self.visivel_restante-dt)
            if self.visivel_restante<=0:
                self.coletavel=False
                self.espera=self.regras.reaparecer_em
                return ()
            self.retangulo.center=(self._centro_base[0],round(self._centro_base[1]+math.sin(self.tempo*3)*5))
            self.retangulo.clamp_ip(self.arena)
            if self.retangulo.colliderect(pygame.Rect(jogador_rect)):
                self.coletavel=False
                self.visivel_restante=0.0
                # Recoleta renova o tempo; não acumula multiplicadores.
                self.restante=self.regras.duracao
                self.espera=self.regras.reaparecer_em
                self.numero_coletas+=1
                return ('coletou_pimenta',)
        return ()

    def perfil_tiro(self,intervalo_base,velocidade_base):
        """Retorna intervalo/velocidade calculados dos valores base, sem acumular.

        O intervalo MENOR aumenta a cadência. O motor mantém seu integrador,
        limite de projéteis e verificação de colisões varridas existentes.
        """
        if not self.ativo: return intervalo_base,velocidade_base
        return (intervalo_base/self.regras.multiplicador_cadencia,
                velocidade_base*self.regras.multiplicador_velocidade)

    def desenhe_coletavel(self,tela):
        """Desenha a pimenta disponível sem alterar seu temporizador ou caixa de coleta."""
        if self.coletavel:
            tela.blit(self.coleta_sprite,self.coleta_sprite.get_rect(center=self.retangulo.center))

    def sprite_projetil(self,direcao=(1,0)):
        """Imagem girada da pimenta. O motor continua dono da posição e hitbox."""
        dx,dy=direcao
        angulo=round(math.degrees(math.atan2(-dy,dx))/5)*5 if dx or dy else 0
        angulo%=360
        if angulo not in self._sprites:
            self._sprites[angulo]=pygame.transform.rotate(self.tiro_direita,angulo)
        return self._sprites[angulo]


def desenhar_vidas(tela,vidas):
    """Desenha SOMENTE três corações no canto inferior esquerdo, sem faixa."""
    vidas=max(0,min(3,int(vidas)))
    tamanho=max(18,round(min(tela.get_width()/1280,tela.get_height()/720)*29))
    esquerda=max(14,round(tela.get_width()*.022))
    base=tela.get_height()-max(12,round(tela.get_height()*.025))
    for i in range(3):
        x=esquerda+i*(tamanho+7)
        pontos=[]
        for n in range(56):
            a=n/56*math.tau
            px=16*math.sin(a)**3
            py=13*math.cos(a)-5*math.cos(2*a)-2*math.cos(3*a)-math.cos(4*a)
            pontos.append((x+tamanho/2+px/33*tamanho,base-tamanho/2-py/32*tamanho))
        pygame.draw.polygon(tela,'#26161b',pontos)
        if i<vidas:
            cx=x+tamanho/2;cy=base-tamanho/2
            internos=[(cx+(px-cx)*.79,cy+(py-cy)*.79) for px,py in pontos]
            pygame.draw.polygon(tela,'#d93835',internos)
