from sys import exit
import pygame
import config
import rgb
from os import listdir
import time
from buttons import Button_Manager

from config_parser import ch_config

fsm= None

class State_Manager():
	def __init__(self, TITLE= config.WINDOW_TITLE,SIZE= config.SIZE, FPS= config.FPS, TRACKS_DIR= config.TRACKS_DIR):
		self.curr_state= None
		pygame.init()
		pygame.display.set_caption(TITLE)
		self.fps_clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(SIZE)
		self.SIZE= self.WIDTH, self.HEIGHT= SIZE
		self.FPS= FPS
		self.f_t= 1/FPS
		self.time= 0
		self.TRACKS_DIR= TRACKS_DIR

	def update(self):
		self.curr_state.update()
		self.curr_state.draw()
		pygame.display.update()
		self.time, lag= self.chk_slp(time.time())

	def ch_state(self, new_state, args= {}):
		self.curr_state.exit()
		print("Entering new state")
		self.curr_state= None
		self.curr_state= new_state
		self.curr_state.enter()

	def chk_slp(self, st):
		del_t= self.fps_clock.tick_busy_loop(self.FPS)/1000 -self.f_t
		if del_t > 0:
			print(f"Lag : {del_t}s")
			return time.time() - st, del_t	
		else:
			return time.time() - st, 0

class Base_State:
	def __init__(self, fsm):
		self.fsm= fsm
		self.button_manager= Button_Manager()
	def enter(self, args= {}):
		print("Entering base state")
	def exit(self):
		print("Exiting base state")
	def update(self):
		print("Updating base state")
	def draw(self):
		self.fsm.screen.fill(rgb.RED)
	
class Main_Menu_State(Base_State):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.button_manager.add_button("Start", (50, 50), (50, 50))
		self.button_manager.add_button("Options", (50, 150), (50, 50))		
		self.button_manager.add_button("Exit", (50, self.fsm.HEIGHT -100), (50, 50))
		
	def enter(self):
		pass

	def update(self):
		events= pygame.event.get()
		for event in events:
			if event.type== pygame.QUIT:
				self.fsm.ch_state(Exit_State())
		action= self.button_manager.chk_buttons(events)
		
		if action == "Exit":
			self.fsm.ch_state(Exit_State())
			
		elif action == "Start":
			self.fsm.ch_state(Select_Track_State(self.fsm))
		
		elif action == "Options":
			self.fsm.ch_state(Settings_State(self.fsm))
				
	def draw(self):
		self.fsm.screen.fill(rgb.WHITE)
		self.button_manager.draw_buttons(self.fsm.screen)

class Select_Track_State(Base_State):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.tracks= listdir(self.fsm.TRACKS_DIR)
		for i,file in enumerate(self.tracks):
			self.button_manager.add_button(file, (375, i*100 + 50), (50, 50))
		self.button_manager.add_button("Exit", (50, self.fsm.HEIGHT -100), (50, 50))
		self.button_manager.add_button("Back", (50, 50), (50, 50))
		
	def update(self):
		events= pygame.event.get()
		for event in events:
			if event.type== pygame.QUIT:
				self.fsm.ch_state(Exit_State())
		action= self.button_manager.chk_buttons(events)
		
		if action == "Exit":
			self.fsm.ch_state(Exit_State())
		elif action == "Back":
			self.fsm.ch_state(Main_Menu_State(self.fsm))
		elif action in self.tracks:
			print(f"Playing {action}")


	def draw(self):
		self.fsm.screen.fill(rgb.WHITE)
		self.button_manager.draw_buttons(self.fsm.screen)

class Settings_State(Base_State):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.button_manager.add_button("Back", (50, 50), (50, 50))
		self.button_manager.add_button("Exit", (50, self.fsm.HEIGHT -100), (50, 50))
		self.button_manager.add_button("Apply", (50, 150), (50, 50))
		self.font= pygame.font.SysFont('Comic Sans MS', 24)
	
	def enter(self):
		import config
		self.settings= dir(config)[:7]
		self.text= []

		for i, setting in enumerate(self.settings):
			val= eval(f"config.{setting}")
			self.text.append((self.font.render(f"{setting} = {val}", 1, rgb.BLACK), (300, i*50 + 25, 10, 10)))
			self.button_manager.add_button("Change", (200, i*50 + 25), (30, 40), font= self.font)

	def update(self):
		events= pygame.event.get()
		for event in events:
			if event.type== pygame.QUIT:
				self.fsm.ch_state(Exit_State())
		action= self.button_manager.chk_buttons(events)
		
		if action == "Exit":
			self.fsm.ch_state(Exit_State())
		elif action == "Back":
			self.fsm.ch_state(Main_Menu_State(self.fsm))	
		elif action == "Change":

			if config.FPS == 30:
				new= 60
			else:
				new= 30
			ch_config("FPS", new)
			self.fsm.__init__()
			self.fsm.curr_state= Main_Menu_State(self.fsm)
			self.fsm.ch_state(Settings_State(self.fsm))
				
	def draw(self):
		self.fsm.screen.fill(rgb.WHITE)
		self.button_manager.draw_buttons(self.fsm.screen)
		
		for line in self.text:
			self.fsm.screen.blit(line[0], line[1])

class Achivements(Base_State):
	def __init__(self, fsm):
		super().__init__(fsm)
	


class Exit_State(Base_State):
	def __init__(self, fsm=fsm):
		super().__init__(fsm)
	
	def enter(self):
		print("Exiting program")
		pygame.quit()
		exit()

if __name__ == "__main__":	
	fsm= State_Manager()
	fsm.curr_state= Main_Menu_State(fsm)
	while True:
		fsm.update()
