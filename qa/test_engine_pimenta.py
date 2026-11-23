"""Regressão da integração real engine/pimenta, usando dublês dos sprites/ataques não enviados."""
import os,sys,types,unittest
from pathlib import Path
os.environ['SDL_VIDEODRIVER']='dummy';os.environ['SDL_AUDIODRIVER']='dummy'
import pygame
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
def modulo(nome,**attrs):
    m=types.ModuleType(nome);m.__dict__.update(attrs);sys.modules[nome]=m;return m
const=dict(WIDTH=1280,HEIGHT=720,FLOOR=622,FPS=60,LIVES=3,DRAGON_HP=480,DRAGON_SHOT_SPEED=1350,
 DRAGON_SHOT_INTERVAL=1/12,BOSS_HP=800,SHOT_SPEED=1350,SHOT_INTERVAL=1/20,HURT_TIME=1.8,TRANSFORM_TIME=3.6,
 PEPPER_DURATION=8,PEPPER_VISIBLE_TIME=5,PEPPER_FIRE_RATE=1.5,PEPPER_SHOT_SPEED=1.25,
 PEPPER_FIRST_SPAWN=6,PEPPER_RESPAWN=20,STAGE_ORDER=(2,1,0))
modulo('config',**const)
sons=[];modulo('audio',play_sound=lambda a,n:sons.append(n))
class Shot(pygame.sprite.Sprite):
    def __init__(self,p):
        super().__init__();self.image=pygame.Surface((22,22),pygame.SRCALPHA)
        self.rect=self.image.get_rect(center=(p.x+40,p.y-60));self.vx=p.shot_speed;self.vy=0
    def update(self,dt):self.rect.x+=round(self.vx*dt)
class Player(pygame.sprite.Sprite):
    def __init__(self,a):
        super().__init__();self.image=pygame.Surface((64,100),pygame.SRCALPHA)
        self.x,self.y=100,622;self.rect=self.image.get_rect(midbottom=(self.x,self.y))
        self.hp=3;self.invulnerable=0;self.dash=0;self.facing=1;self.vx=0
        self.jump_buffer=0;self.previous_input={};self.aim_x=1;self.aim_y=0
        self.shot_speed=1350;self.shot_interval=1/20;self.shot_cooldown=0
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
        self.warning=None;self.breathing=False;self.transform=0
    def update(self,*a):pass
    def refresh_image(self,*a):pass
class Side(Boss):
    def __init__(self,boss):super().__init__({})
modulo('sprites',Player=Player,Boss=Boss,hitboxes_overlap=lambda a,b:a.rect.colliderect(b.rect))
modulo('attacks',update_attacks=lambda *a:None)
modulo('comilao',Comilao=Boss,update_comilao=lambda *a:None)
modulo('piramide',Piramide=Boss,PyramidSide=Side)
modulo('piramide_attacks',update_piramide=lambda *a:None)
from engine import GameModel
class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):pygame.init();pygame.display.set_mode((1280,720))
    @classmethod
    def tearDownClass(cls):pygame.quit()
    def model(self,stage):
        assets={'pepper':pygame.image.load(str(root/'assets/powerups/pimenta.png')).convert_alpha()}
        m=GameModel(assets);m.start(stage);return m
    def coletar(self,m):
        m.state='playing'
        while not m.pepper.coletavel:m.step(.05,{})
        m.player.x=m.pepper.retangulo.centerx
        m.step(.01,{})
        self.assertTrue(m.pepper.ativo)
    def test_tres_fases_coleta_tiro_expira_morte(self):
        for stage,interval,speed in ((0,1/12,1350),(1,1/20,1350),(2,1/20,1350)):
            with self.subTest(stage=stage):
                m=self.model(stage)
                self.assertEqual(m.player.shot_interval,interval);self.assertEqual(m.player.shot_speed,speed)
                before=m.pepper.tempo
                for _ in range(10):m.step(.05,{})
                self.assertEqual(m.pepper.tempo,before,'introdução consome tempo do bônus')
                count=sons.count('pimentinha');self.coletar(m)
                self.assertEqual(sons.count('pimentinha'),count+1)
                self.assertEqual(m.player.shot_interval,interval/1.5);self.assertEqual(m.player.shot_speed,speed*1.25)
                m.step(.01,{'shoot':True});hot=list(m.shots)[-1]
                self.assertTrue(hot.is_pepper);self.assertEqual(hot.vx,speed*1.25)
                self.assertEqual(hot.image.get_size(),(22,22),'integração alterou hitbox/sprite físico')
                remaining=m.pepper.restante;m.pause();m.step(10,{})
                self.assertEqual(m.pepper.restante,remaining)
                m.resume();m.state='transform';m.state_time=0
                for _ in range(10):m.step(.05,{})
                self.assertEqual(m.pepper.restante,remaining)
                m.state='playing'
                for _ in range(162):m.step(.05,{})
                self.assertFalse(m.pepper.ativo);self.assertEqual(m.player.shot_speed,speed)
                self.assertEqual(m.player.shot_interval,interval)
                self.assertTrue(hot.is_pepper,'tiro antigo perdeu a identidade')
                m.player.shot_cooldown=0;m.player_actions()  # shooting false, no extra shot
                m.step(.01,{'shoot':True});self.assertFalse(list(m.shots)[-1].is_pepper)
                # Coleta manual apenas para preparar a condição de dano fatal.
                m.pepper.restante=8;m.apply_pepper_profile();m.player.hp=1;m.player.invulnerable=0
                self.assertTrue(m.hurt_player());self.assertEqual(m.state,'dead')
                self.assertFalse(m.pepper.ativo);self.assertEqual(m.player.shot_speed,speed)
                m.start(stage);self.assertFalse(m.pepper.ativo);self.assertFalse(m.pepper.coletavel)
                self.assertEqual(m.player.hp,3)
    def test_dano_real_apenas_e_dash(self):
        m=self.model(0);m.state='playing';n=sons.count('hurt')
        self.assertTrue(m.hurt_player());self.assertEqual(m.player.hp,2)
        self.assertFalse(m.hurt_player());self.assertEqual(sons.count('hurt'),n+1)
        m.player.invulnerable=0;m.player.dash=.1
        self.assertFalse(m.hurt_player());self.assertEqual(m.player.hp,2)
    def test_visibilidade_e_arena_piramide(self):
        m=self.model(2);m.state='playing'
        while not m.pepper.coletavel:m.step(.05,{})
        for _ in range(101):m.step(.05,{})
        self.assertFalse(m.pepper.coletavel);self.assertFalse(m.pepper.ativo)
        for _ in range(401):m.step(.05,{})
        self.assertTrue(m.pepper.coletavel)
        t=m.pepper.visivel_restante;m.boss.phase=3;m.step(.01,{})
        self.assertGreaterEqual(m.pepper.retangulo.left,207)
        self.assertLessEqual(m.pepper.retangulo.right,1073)
        self.assertLessEqual(m.pepper.visivel_restante,t)
    def test_ordem_logica_e_reset_menu(self):
        m=self.model(2);m.state='victory'
        self.assertTrue(m.next_stage());self.assertEqual(m.stage_index,1)
        m.state='victory';self.assertTrue(m.next_stage());self.assertEqual(m.stage_index,0)
        m.state='victory';self.assertFalse(m.next_stage())
        m.start_story();self.assertEqual(m.stage_index,2);self.assertEqual(m.state,'story')
        m.reset();self.assertFalse(m.pepper.ativo);self.assertEqual(m.state,'title')
if __name__=='__main__':unittest.main(verbosity=2)
