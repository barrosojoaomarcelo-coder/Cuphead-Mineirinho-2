"""Renderer real; módulos de chefes ausentes recebem só avisos de desenho vazios."""
import os, sys, types, importlib.util
from pathlib import Path
os.environ['SDL_VIDEODRIVER']='dummy';os.environ['SDL_AUDIODRIVER']='dummy'
import pygame
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
def stub(name,**attrs):
    m=types.ModuleType(name);m.__dict__.update(attrs);sys.modules[name]=m
stub('config',WIDTH=1280,HEIGHT=720,FLOOR=622,STAGE_ORDER=(2,1,0))
stub('engine',STAGES=('Dragão Vermelho','Chefe Comilão','Olho da Pirâmide'))
stub('comilao',draw_comilao_warning=lambda *a:None)
stub('piramide_attacks',draw_piramide_warning=lambda *a:None)
spec=importlib.util.spec_from_file_location('scene_em_teste',ROOT/'scene.py')
scene=importlib.util.module_from_spec(spec);spec.loader.exec_module(scene)
pygame.init();tela=pygame.display.set_mode((1280,720))
def solid(c):
    s=pygame.Surface((1280,720));s.fill(c);return s
assets={'day':solid('#42617b'),'night':solid('#202d43'),'valley':solid('#704539'),'pyramid':solid('#542c70')}
r=scene.Renderer(assets)
class Pepper:
    def desenhe_coletavel(self,tela):pass
    def sprite_projetil(self,direction):
        s=pygame.Surface((12,6),pygame.SRCALPHA);s.fill('#ff3100');return s
p=types.SimpleNamespace(x=200,y=622,dash=0,dash_cooldown=.4,hp=3,facing=1)
b=types.SimpleNamespace(warning=None,horizontal=None,transform=0)
model=types.SimpleNamespace(stage_index=0,state='playing',night=0,boss=b,player=p,
    boss_group=pygame.sprite.Group(),player_group=pygame.sprite.Group(),shots=pygame.sprite.Group(),
    beams=pygame.sprite.Group(),fire=pygame.sprite.Group(),minions=pygame.sprite.Group(),
    warnings=[],stats={'shots':0,'hits':0},pepper=Pepper(),elapsed=22)
texts=[]
orig_text=r.text
def capture(target,message,*args,**kwargs):
    texts.append(str(message));return orig_text(target,message,*args,**kwargs)
r.text=capture
for idx,cor in ((0,'#42617b'),(1,'#704539'),(2,'#542c70')):
    model.stage_index=idx;model.state='playing';texts.clear()
    buttons=r.draw(tela,model)
    assert buttons=={} and texts==[]
    assert tela.get_at((20,20))[:3]==pygame.Color(cor)[:3], 'HUD superior deve sumir, sem cobrir cenário'
    assert tela.get_at((1270,700))[:3]==pygame.Color(cor)[:3], 'Faixa inferior deve sumir'
    assert tela.get_at((37,690))[:3]!=pygame.Color(cor)[:3], 'vidas inferiores devem existir'
# Imagem de pimenta é render-only, mesma posição física e retângulo original.
shot=pygame.sprite.Sprite();shot.image=pygame.Surface((8,8));shot.image.fill('#24ff00')
shot.rect=shot.image.get_rect(center=(450,400));shot.is_pepper=True;shot.pepper_direction=(1,0)
image=shot.image;rect=shot.rect.copy();model.shots.add(shot)
r.draw(tela,model)
assert shot.image is image and shot.rect==rect and shot.image.get_at((0,0))[:3]==(36,255,0)
assert tela.get_at((450,400))[:3]==(255,49,0)
shot.is_pepper=False;r.draw(tela,model);assert tela.get_at((450,400))[:3]==(36,255,0)
# Novo cartão; nenhum overlay antigo pode ser chamado.
old_overlay=r._overlay
r._overlay=lambda *a:(_ for _ in ()).throw(AssertionError('pausa antiga não deve ser usada'))
model.state='paused';buttons=r.draw(tela,model)
assert tuple(buttons)==('retornar','reiniciar','como_jogar','menu')
for action,rect in buttons.items():
    assert r.pause_menu.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN,button=1,pos=rect.center))==action
assert r.draw(tela,model,instructions=True).keys()=={'back'}
r._overlay=old_overlay
# Números e conclusão acompanham ordem de apresentação 2,1,0.
for idx,logical in ((2,1),(1,2),(0,3)):
    model.stage_index=idx;model.state='intro';texts.clear();r.draw(tela,model)
    assert any(t.startswith(f'FASE {logical} — ') for t in texts)
    model.state='victory';texts.clear();r.draw(tela,model)
    assert ('AVENTURA CONCLUÍDA!' in texts)==(idx==0)
    expected='VOLTAR AO MENU' if idx==0 else f'IR PARA A FASE {logical+1}'
    assert expected in texts
    assert not any('TEMPO ' in t or 'PRECISÃO ' in t or 'RECORDE' in t for t in texts)
pygame.quit()
print('PASS Renderer real: sem faixas/timer em três cenários, só HP inferior, pausa/ajuda, projétil pimenta sem mudar hitbox, intro/vitória na nova ordem.')
