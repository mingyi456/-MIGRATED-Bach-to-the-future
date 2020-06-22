from sys import exit
import pygame
import config
import rgb
from os import listdir
import time
from buttons import Button_Manager
from mapGenerator import beatmapGenerator
from config_parser import reset_config


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
		self.lag= 0
		self.TRACKS_DIR= TRACKS_DIR

	def update(self):
		self.curr_state.update(self.time, self.lag)
		self.curr_state.draw()
		pygame.display.update()
		self.time, self.lag= self.chk_slp(time.time())

	def ch_state(self, new_state, args= {}):
		self.curr_state.exit()
		print("Entering new state")
		self.curr_state= None
		self.curr_state= new_state
		self.curr_state.enter(args)

	def chk_slp(self, st):
		del_t= self.fps_clock.tick_busy_loop(self.FPS)/1000 -self.f_t
		if del_t > 0:
			print(f"Lag : {del_t}s")
			return time.time() - st, del_t	
		else:
			return time.time() - st, 0

class BaseState:
	def __init__(self, fsm):
		self.fsm= fsm
		self.button_manager= Button_Manager()
	def enter(self, args):
		print("Entering base state")
	def exit(self):
		print("Exiting base state")
	def update(self, game_time, lag):
		print("Updating base state")
	def draw(self):
		self.fsm.screen.fill(rgb.WHITE)
	
class MainMenuState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.button_manager.add_button("Start (Space)", (50, 50), (50, 50), ret= "Start", key= "space")
		self.button_manager.add_button("Options", (50, 150), (50, 50))		
		self.button_manager.add_button("Exit (Esc)", (50, self.fsm.HEIGHT -100), (50, 50), ret= "Exit", key= "escape")
		
	def update(self, game_time, lag):
		events= pygame.event.get()
		for event in events:
			if event.type== pygame.QUIT:
				self.fsm.ch_state(ExitState(self.fsm))
		action= self.button_manager.chk_buttons(events)
		
		if action == "Exit":
			self.fsm.ch_state(ExitState(self.fsm))
			
		elif action == "Start":
			self.fsm.ch_state(SelectTrackState(self.fsm))
		
		elif action == "Options":
			self.fsm.ch_state(SettingsState(self.fsm))
				
	def draw(self):
		self.fsm.screen.fill(rgb.WHITE)
		self.button_manager.draw_buttons(self.fsm.screen)

class SelectTrackState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.tracks= listdir(self.fsm.TRACKS_DIR)
		for i,file in enumerate(self.tracks):
			self.button_manager.add_button(file, (375, i*100 + 50), (50, 50))
		self.button_manager.add_button("Exit (Esc)", (50, self.fsm.HEIGHT -100), (50, 50), ret= "Exit", key= "escape")
		self.button_manager.add_button("Back (Backspace)", (50, 50), (50, 50), ret="Back", key= "backspace")
		
	def update(self, game_time, lag):
		events= pygame.event.get()
		for event in events:
			if event.type== pygame.QUIT:
				self.fsm.ch_state(ExitState(self.fsm))
		action= self.button_manager.chk_buttons(events)
		
		if action == "Exit":
			self.fsm.ch_state(ExitState(self.fsm))
		elif action == "Back":
			self.fsm.ch_state(MainMenuState(self.fsm))
		elif action in self.tracks:
			print(f"Playing {action}")
			self.fsm.ch_state(PlayGameState(self.fsm), {"file_name" : action})


	def draw(self):
		self.fsm.screen.fill(rgb.WHITE)
		self.button_manager.draw_buttons(self.fsm.screen)

class SettingsState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.button_manager.add_button("Back", (50, 50), (50, 50))
		self.button_manager.add_button("Exit (Esc)", (50, self.fsm.HEIGHT -100), (50, 50), ret= "Exit", key= "escape")
		self.button_manager.add_button("Restore", (50, 150), (50, 50), ret= "Restore defaults")
		self.button_manager.add_button("defaults", (50, 200), (50, 50), ret= "Restore defaults")
		self.font= pygame.font.SysFont('Comic Sans MS', 24)

	
	def enter(self, args):
		self.settings= dir(config)[:7]
		self.text= []

		for i, setting in enumerate(self.settings):
			val= eval(f"config.{setting}")
			self.text.append((self.font.render(f"{setting} : {val}", 1, rgb.BLACK), (300, i*50 + 25, 10, 10)))
			self.button_manager.add_button("Change", (200, i*50 + 25), (30, 40),ret= setting, font= self.font)

	def update(self, game_time, lag):
		events= pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.fsm.ch_state(ExitState(self.fsm))
		action= self.button_manager.chk_buttons(events)

		if action == "Exit":
			self.fsm.ch_state(ExitState(self.fsm))
		elif action == "Back":
			self.fsm.ch_state(MainMenuState(self.fsm))	
		elif action in self.settings:		
			self.fsm.ch_state(ChSettingState(self.fsm), {"setting" : action, "value" : eval(f"config.{action}")} )
			
		elif action == "Restore defaults":
			reset_config()
			self.fsm.__init__()
			self.fsm.curr_state= MainMenuState(self.fsm)
			self.fsm.ch_state(SettingsState(self.fsm))

	def draw(self):
		self.fsm.screen.fill(rgb.WHITE)
		self.button_manager.draw_buttons(self.fsm.screen)
		
		for line in self.text:
			self.fsm.screen.blit(line[0], line[1])
			
class ChSettingState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.font= pygame.font.SysFont('Comic Sans MS', 30)
		self.button_manager.add_button("Back", (50, 50), (50, 50))
		
	def enter(self, args):
		self.setting= args["setting"]
		self.setting_text= self.font.render(self.setting, 1, rgb.BLACK), (250, 50, 50, 50)
		self.val= args["value"]
		self.val_text= self.font.render(f"Current value : {self.val}", 1, rgb.BLACK), (250, 100, 50, 50)
		
		
	def update(self, game_time, lag):
		events= pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.fsm.ch_state(ExitState(self.fsm))
		action= self.button_manager.chk_buttons(events)
		if action == "Back":
			self.fsm.ch_state(SettingsState(self.fsm))
	
	def draw(self):
		self.fsm.screen.fill(rgb.WHITE)
		self.button_manager.draw_buttons(self.fsm.screen)
		self.fsm.screen.blit(self.setting_text[0], self.setting_text[1])
		self.fsm.screen.blit(self.val_text[0], self.val_text[1])


class AchivementsState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
	
class PlayGameState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.button_manager.add_button("Back", (50, 50), (50, 50), ret= "Back", key= "backspace")
		self.button_manager.add_keystroke("Pause", 'p')
		self.isPaused= False
	
	def enter(self, args):
		file= args["file_name"]
		print(f"File name = {file}")
		
	def update(self, game_time, lag):
		events= pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.fsm.ch_state(ExitState(self.fsm))
				
		action= self.button_manager.chk_buttons(events)
		
		if action == "Exit":
			self.fsm.ch_state(ExitState(self.fsm))
		
		elif action == "Back":
			self.fsm.ch_state(MainMenuState(self.fsm))
		
		elif action == "Pause":
			print("Pause!")
			self.isPaused= True
		

		

	def draw(self):
		self.fsm.screen.fill(rgb.WHITE)
		self.button_manager.draw_buttons(self.fsm.screen)
		

		

class ExitState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
	
	def enter(self, args):
		print("Exiting program")
		pygame.quit()
		exit()

if __name__ == "__main__":	
	fsm= State_Manager()
	fsm.curr_state= MainMenuState(fsm)
	while True:
		fsm.update()
