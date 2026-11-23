"""Dublês APENAS dos sprites e módulos de chefes não enviados pelo usuário.
Os arquivos main/engine/scene/assets/audio/config/poder/pausa são os reais da atualização.
"""
import sys,types
import pygame

def modulo(nome,**attrs):
    m=types.ModuleType(nome);m.__dict__.update(attrs);sys.modules[nome]=m;return m

class Shot(pygame.sprite.Sprite):
    def __init__(self,p):
        super().__init__();self.image=pygame.Surface((22,22),pygame.SRCALPHA)
        self.rect=self.image.get_rect(center=(p.x+40,p.y-60));self.vx=p.shot_speed;self.vy=0
    def update(self,dt):self.rect.x+=round(self.vx*dt)
class Player(pygame.sprite.Sprite):
    def __init__(self,a):
        super().__init__();self.image=pygame.Surface((64,100),pygame.SRCALPHA)
        self.x,self.y=100,622;self.rect=self.image.get_rect(midbottom=(self.x,self.y))
        self.dash_cooldown=0;self.dash_direction=1
        self.hp=3;self.invulnerable=0;self.dash=0;self.facing=1;self.vx=0
        self.jump_buffer=0;self.previous_input={};self.aim_x=1;self.aim_y=0
        self.shot_speed=1800;self.shot_interval=1/20;self.shot_cooldown=0
        self.shooting=False;self.jumped=self.landed=self.dashed=False
    def update(self,dt,controls,*args):
        self.invulnerable=max(0,self.invulnerable-dt)
        self.shot_cooldown=max(0,self.shot_cooldown-dt)
        self.shooting=controls.get('shoot',False)
        self.rect.midbottom=(self.x,self.y)
    def shoot(self):return Shot(self)
class Boss(pygame.sprite.Sprite):
    def __init__(self,a):
        super().__init__();self.image=pygame.Surface((60,100));self.rect=self.image.get_rect(center=(1180,200))
        self.hp=self.max_hp=800;self.phase=1;self.cast=0;self.charge=0;self.mouth_lock=None
        self.warning=None;self.breathing=False;self.transform=0;self.horizontal=None
    def update(self,*a):pass
    def refresh_image(self,*a):pass
class Side(Boss):
    def __init__(self,boss):super().__init__({})
modulo('sprites',Player=Player,Boss=Boss,hitboxes_overlap=lambda a,b:a.rect.colliderect(b.rect))
modulo('attacks',update_attacks=lambda *a:None)
modulo('comilao',Comilao=Boss,update_comilao=lambda *a:None,draw_comilao_warning=lambda *a:None)
modulo('piramide',Piramide=Boss,PyramidSide=Side)
modulo('piramide_attacks',update_piramide=lambda *a:None,draw_piramide_warning=lambda *a:None)
