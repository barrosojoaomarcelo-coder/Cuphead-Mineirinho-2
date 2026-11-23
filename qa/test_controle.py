"""Pygame real, dispositivos físicos simulados; nenhum joystick real conectado."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import sys
from pathlib import Path
import unittest
from unittest.mock import patch
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pygame
import controle

class FakeJoystick:
    def __init__(self,identifier,name='USB Gamepad'):
        self.identifier=identifier;self.name=name;self.axes=[0.0,0.0];self.buttons=[False]*16;self.hat=(0,0);self.closed=False
    def init(self):self.closed=False
    def quit(self):self.closed=True
    def get_instance_id(self):return self.identifier
    def get_name(self):return self.name
    def get_numbuttons(self):return len(self.buttons)
    def get_numaxes(self):return len(self.axes)
    def get_numhats(self):return 1
    def get_button(self,n):return self.buttons[n]
    def get_axis(self,n):return self.axes[n]
    def get_hat(self,n):return self.hat

class FakeController:
    def __init__(self,joy):self.joy=joy;self.axes=[0]*6;self.buttons=[False]*21
    def quit(self):pass
    def get_button(self,n):return self.buttons[n]
    def get_axis(self,n):return self.axes[n]

class ControleTests(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.devices=[];self.normalized={}
        def get_joy(i):return self.devices[i]
        self.patches=[patch.object(pygame.joystick,'get_count',side_effect=lambda:len(self.devices)),
                      patch.object(pygame.joystick,'Joystick',side_effect=get_joy)]
        api=SimpleNamespace(init=lambda:None,set_eventstate=lambda enabled:None,
            is_controller=lambda index:self.devices[index].identifier in self.normalized,
            Controller=SimpleNamespace(from_joystick=lambda joy:self.normalized[joy.identifier]))
        self.patches.append(patch.object(controle,'controller_api',api))
        for p in self.patches:p.start()
    def tearDown(self):
        for p in reversed(self.patches):p.stop()
        pygame.quit()
    def add(self,id=10,normalized=False):
        joy=FakeJoystick(id);self.devices.append(joy)
        if normalized:self.normalized[id]=FakeController(joy)
        return joy
    def event(self,pad,kind,menu=False,paused=False,**kwargs):
        return pad.handle_event(pygame.event.Event(kind,instance_id=pad.instance_id,**kwargs),menu,paused)
    def test_no_hardware_then_hotplug_and_remove(self):
        pad=controle.ControleJoystick();self.assertFalse(pad.conectado)
        self.assertFalse(any(pad.read_controls().values()))
        joy=self.add()
        self.assertEqual(pad.handle_event(pygame.event.Event(pygame.JOYDEVICEADDED,device_index=0)),[])
        self.assertTrue(pad.conectado);self.assertEqual(pad.instance_id,10)
        self.devices.clear()
        pad.handle_event(pygame.event.Event(pygame.JOYDEVICEREMOVED,instance_id=10))
        self.assertFalse(pad.conectado);self.assertTrue(pad.desconectou)
        self.assertFalse(any(pad.read_controls().values()));self.assertTrue(joy.closed)
    def test_generic_movement_actions_and_deadzone(self):
        joy=self.add();pad=controle.ControleJoystick()
        joy.axes=[.2,-.21];self.assertFalse(any(pad.read_controls().values()))
        joy.axes=[-.8,.7];joy.buttons[0]=joy.buttons[1]=joy.buttons[2]=True
        got=pad.read_controls();self.assertTrue(all(got[k] for k in ('left','down','jump','shoot','dash')))
        joy.axes=[0,0];joy.hat=(1,1);joy.buttons[3]=True
        got=pad.read_controls();self.assertTrue(got['right'] and got['up'])
    def test_normalized_xbox_playstation_mapping_and_duplicate_events(self):
        self.add(normalized=True);pad=controle.ControleJoystick();c=self.normalized[10]
        c.axes[0]=-24000;c.axes[1]=18000
        c.buttons[pygame.CONTROLLER_BUTTON_A]=True
        c.buttons[pygame.CONTROLLER_BUTTON_X]=True
        c.buttons[pygame.CONTROLLER_BUTTON_B]=True
        got=pad.read_controls();self.assertTrue(all(got[k] for k in ('left','down','jump','shoot','dash')))
        self.assertEqual(self.event(pad,pygame.JOYBUTTONDOWN,menu=True,button=0),[])
        self.assertEqual(self.event(pad,pygame.CONTROLLERBUTTONDOWN,menu=True,button=pygame.CONTROLLER_BUTTON_A),[pygame.K_RETURN])
        self.assertEqual(self.event(pad,pygame.CONTROLLERBUTTONDOWN,button=pygame.CONTROLLER_BUTTON_A),[])
    def test_start_back_and_menu_only_confirmation(self):
        self.add();pad=controle.ControleJoystick()
        self.assertEqual(self.event(pad,pygame.JOYBUTTONDOWN,button=0),[])
        self.assertEqual(self.event(pad,pygame.JOYBUTTONDOWN,button=7),[pygame.K_p])
        self.assertEqual(self.event(pad,pygame.JOYBUTTONDOWN,menu=True,button=7),[pygame.K_RETURN])
        self.assertEqual(self.event(pad,pygame.JOYBUTTONDOWN,menu=True,paused=True,button=7),[pygame.K_p])
        self.assertEqual(self.event(pad,pygame.JOYBUTTONDOWN,button=6),[pygame.K_ESCAPE])
    def test_analog_navigation_edges_hysteresis_and_menu_reentry(self):
        self.add();pad=controle.ControleJoystick()
        def axis(v,menu=True):return self.event(pad,pygame.JOYAXISMOTION,menu=menu,axis=0,value=v)
        self.assertEqual(axis(-.8),[pygame.K_LEFT]);self.assertEqual(axis(-.7),[])
        self.assertEqual(axis(-.19),[]);self.assertEqual(axis(-.3),[])
        self.assertEqual(axis(0),[]);self.assertEqual(axis(.7),[pygame.K_RIGHT])
        axis(0,menu=False)
        self.assertEqual(axis(.7),[pygame.K_RIGHT])
    def test_hat_and_other_devices_ignored(self):
        self.add();pad=controle.ControleJoystick()
        self.assertEqual(self.event(pad,pygame.JOYHATMOTION,menu=True,hat=0,value=(0,1)),[pygame.K_UP])
        self.assertEqual(self.event(pad,pygame.JOYHATMOTION,menu=True,hat=0,value=(0,1)),[])
        other=pygame.event.Event(pygame.JOYBUTTONDOWN,instance_id=777,button=0)
        self.assertEqual(pad.handle_event(other,menu=True),[])
    def test_menu_confirm_does_not_accidentally_jump_or_dash_after_resume(self):
        joy=self.add();pad=controle.ControleJoystick();joy.buttons[0]=True
        self.event(pad,pygame.JOYBUTTONDOWN,menu=True,button=0)
        self.assertFalse(pad.read_controls()['jump'])
        joy.buttons[0]=False;pad.read_controls();joy.buttons[0]=True
        self.assertTrue(pad.read_controls()['jump'])
        joy.buttons[1]=True;self.event(pad,pygame.JOYBUTTONDOWN,menu=True,button=1)
        self.assertFalse(pad.read_controls()['dash'])
    def test_unplug_before_event_returns_safe_controls(self):
        joy=self.add();pad=controle.ControleJoystick()
        joy.get_axis=lambda n:(_ for _ in ()).throw(pygame.error('detached'))
        self.assertFalse(any(pad.read_controls().values()))
        self.assertTrue(pad.desconectou);self.assertFalse(pad.conectado)
    def test_remove_active_selects_another_and_requests_pause(self):
        self.add(10);self.add(20);pad=controle.ControleJoystick()
        self.devices.pop(0)
        pad.handle_event(pygame.event.Event(pygame.JOYDEVICEREMOVED,instance_id=10))
        self.assertTrue(pad.desconectou);self.assertEqual(pad.instance_id,20)

if __name__=='__main__':unittest.main(verbosity=2)
