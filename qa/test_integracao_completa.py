"""Integração real dos arquivos recebidos; só sprites/chefes ausentes são dublês.
Artes de terceiros são miniaturas coloridas temporárias, não substituem assets do jogo.
"""
import os,sys,tempfile,json
from pathlib import Path
os.environ['SDL_VIDEODRIVER']='dummy';os.environ['SDL_AUDIODRIVER']='dummy'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import pygame
import dependencias_teste
import assets,config,audio,main

def frame_fixture(pasta):
    manifest={'player':{'actions':{}},'dragon':{},'background':{'day':'assets/day.png','night':'assets/night.png'},'bread':{'url':'assets/bread.png'}}
    for nome in ('01_parado','02_corrida','03_pulo','04_atirar_frente','05_atirar_cima','06_dash','07_correr_atirar','08_pular_atirar','09_atirar_diagonal'):
        manifest['player']['actions'][nome]={'url':f'assets/{nome}.png','cols':4,'rows':2,'count':8}
    for nome in ('base','head'):manifest['dragon'][nome]={'url':f'assets/{nome}.png','cols':4,'rows':2,'count':8}
    arquivos=set([s['url'] for s in manifest['player']['actions'].values()]+[s['url'] for s in manifest['dragon'].values()])
    arquivos.update(['assets/day.png','assets/night.png','assets/bread.png','assets/vale-comilao.png','assets/piramide-cenario.png'])
    arquivos.update('assets/'+x+'.png' for x in ('comilao-corpo-animado','comilao-boca-animada','piramide-base','piramide-olho-esquerdo','piramide-olho-direito','servo-serpente','servo-morcego'))
    for nome in arquivos:
        arquivo=pasta/nome;arquivo.parent.mkdir(parents=True,exist_ok=True)
        imagem=pygame.Surface((120,120),pygame.SRCALPHA);imagem.fill('#647b87');pygame.image.save(imagem,str(arquivo))
    (pasta/'assets/manifest.json').write_text(json.dumps(manifest))
    (pasta/'assets/powerups').mkdir();import shutil
    shutil.copy(ROOT/'assets/powerups/pimenta.png',pasta/'assets/powerups/pimenta.png')

def key(ui,k):main.handle_event(ui,pygame.event.Event(pygame.KEYDOWN,key=k))
def click(ui,p):
    w,h=ui['window'].get_size();scale=min(w/config.WIDTH,h/config.HEIGHT)
    pos=((w-config.WIDTH*scale)/2+p[0]*scale,(h-config.HEIGHT*scale)/2+p[1]*scale)
    main.handle_event(ui,pygame.event.Event(pygame.MOUSEBUTTONDOWN,button=1,pos=pos))

def playing(ui):
    if ui['game'].state=='story':key(ui,pygame.K_RETURN)
    while ui['game'].state=='intro':main.update_game(ui,.05,{})
    assert ui['game'].state=='playing'

with tempfile.TemporaryDirectory() as tmp:
    pasta=Path(tmp);pygame.init();pygame.display.set_mode((1152,648))
    frame_fixture(pasta);assets.ROOT=pasta
    ui=main.initialize(save_dir=pasta/'saves')
    assert ui['title_menu_active'];main.draw_screen(ui);pygame.time.wait(270)
    assert pygame.mixer.Channel(0).get_volume()>.5
    # All stage menu buttons -> actual engine -> actual render and actual audio.
    for numero,fisico in ((1,2),(2,1),(3,0)):
        menu=ui['title_menu'];click(ui,menu.nivel_rects[numero-1].center);click(ui,menu.iniciar_rect.center)
        pygame.time.wait(150)
        game=ui['game'];assert game.stage_index==fisico and not ui['title_menu_active']
        assert pygame.mixer.Channel(0).get_sound()==ui['assets']['sounds']['music']
        assert abs(pygame.mixer.Channel(0).get_volume()-.20)<.02
        playing(ui);main.draw_screen(ui)
        assert ui['buttons']=={}
        # First pepper after six seconds, collect -> voice -> shot metadata.
        while not game.pepper.coletavel:main.update_game(ui,.05,{})
        game.player.x=game.pepper.retangulo.centerx;main.update_game(ui,.01,{'shoot':True})
        assert game.pepper.ativo
        assert pygame.mixer.Channel(1).get_sound()==ui['assets']['sounds']['pimentinha']
        main.update_game(ui,.05,{'shoot':True});assert any(s.is_pepper for s in game.shots)
        main.draw_screen(ui)
        # Pause -> Help -> Back -> Resume keeps timers frozen and restores fight.
        restante=game.pepper.restante;key(ui,pygame.K_p);main.draw_screen(ui)
        assert set(ui['buttons'])=={'retornar','reiniciar','como_jogar','menu'}
        main.update_game(ui,1,{});assert game.pepper.restante==restante
        click(ui,ui['buttons']['como_jogar'].center);assert ui['instructions'] and game.state=='paused'
        main.draw_screen(ui);key(ui,pygame.K_ESCAPE);assert not ui['instructions'] and game.state=='paused'
        main.draw_screen(ui);click(ui,ui['buttons']['retornar'].center);assert game.state=='playing'
        # Real damage triggers original supplied voice; invulnerability doesn't repeat.
        audio.stop_voices(ui['assets']);game.player.invulnerable=0;game.player.dash=0
        assert game.hurt_player() and game.player.hp==2
        sound=pygame.mixer.Channel(1).get_sound();assert sound==ui['assets']['sounds']['hurt']
        assert not game.hurt_player() and pygame.mixer.Channel(1).get_sound()==sound
        # Restart from pause restores 3 HP and clears pepper in this same physical stage.
        key(ui,pygame.K_p);main.draw_screen(ui);click(ui,ui['buttons']['reiniciar'].center)
        assert game.state=='intro' and game.player.hp==3 and not game.pepper.ativo and game.stage_index==fisico
        playing(ui);key(ui,pygame.K_p);main.draw_screen(ui);click(ui,ui['buttons']['menu'].center)
        assert game.state=='title' and ui['title_menu_active']
    # Campaign and last-boss labels remain consistent.
    main.start_selected_stage(ui,1)
    for atual,seguinte in ((2,1),(1,0)):
        assert ui['game'].stage_index==atual;ui['game'].state='victory';main.button_action(ui,'play')
        assert ui['game'].stage_index==seguinte
    ui['game'].state='victory';main.button_action(ui,'play');assert ui['game'].state=='title'
    # Resize + mute transition from menu to phase and back.
    main.handle_event(ui,pygame.event.Event(pygame.VIDEORESIZE,w=900,h=800));main.draw_screen(ui)
    key(ui,pygame.K_m);assert ui['assets']['muted']
    main.start_selected_stage(ui,1);playing(ui);assert pygame.mixer.Channel(0).get_volume()==0
    key(ui,pygame.K_m);assert not ui['assets']['muted']
    assert abs(pygame.mixer.Channel(0).get_volume()-.20)<.02
    main.button_action(ui,'menu');main.update_game(ui,.02,{});pygame.time.wait(270);assert pygame.mixer.Channel(0).get_volume()>.5
    # Main routes controller keys in the correct context and merges actions.
    real=ui['joystick'];real.fechar()
    class ControleDeTeste:
        desconectou=False
        def __init__(self):self.contextos=[]
        def handle_event(self,e,menu=False,paused=False):
            self.contextos.append((menu,paused))
            return getattr(e,'teclas',[])
        def read_controls(self):return {'shoot':True,'left':False}
    controle=ControleDeTeste();ui['joystick']=controle
    def pad(*teclas):main.handle_event(ui,pygame.event.Event(pygame.USEREVENT,teclas=list(teclas)))
    main.start_selected_stage(ui,1);playing(ui)
    assert main.read_controls(ui)['shoot']
    pad(pygame.K_p);assert ui['game'].state=='paused' and controle.contextos[-1]==(False,False)
    main.draw_screen(ui);pad(pygame.K_RETURN);assert ui['game'].state=='playing'
    assert controle.contextos[-1]==(True,True)
    pad(pygame.K_p);main.button_action(ui,'como_jogar');pad(pygame.K_RETURN)
    assert not ui['instructions'] and ui['game'].state=='paused'
    assert controle.contextos[-1]==(True,False)
    pad(pygame.K_p);assert ui['game'].state=='playing'
    controle.desconectou=True;pad();assert ui['game'].state=='paused'
    controle.desconectou=False;main.button_action(ui,'menu');pad(pygame.K_RIGHT)
    assert ui['title_menu'].selecionado==1
    class PerdeuDuranteLeitura(ControleDeTeste):
        def read_controls(self):
            self.desconectou=True
            return {}
    main.start_selected_stage(ui,1);playing(ui)
    ui['joystick']=PerdeuDuranteLeitura()
    main.game_screen(ui,max_frames=1)
    assert ui['game'].state=='paused'
    ui['joystick']=real;main.button_action(ui,'menu')
    key(ui,pygame.K_ESCAPE);assert not ui['running']
    pygame.quit()
print('PASS main/engine/scene/assets/audio/config reais:3 fases,menu->luta,coleta,vozes,tiros,pausa/ajuda/reinício/menu,ordem,resize,mute. Sprites/chefes ausentes: dublês.')
