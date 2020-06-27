from sys import exit
import pygame
import config
import rgb
from os import listdir
import time
from buttons import ActionManager, TextBox, TextLine
import csv
from config_parser import reset_config
from readJSON import data
import vlc
import string


class State_Manager():
	def __init__(self, TITLE=config.WINDOW_TITLE, SIZE=config.SIZE, FPS=config.FPS, TRACKS_DIR=config.TRACKS_DIR,
	             WAV_DIR=config.WAV_DIR):
		
		self.WAV_DIR = WAV_DIR
		self.wav_files = {}
		for i in listdir(self.WAV_DIR):
			self.wav_files[i.rsplit('.', 1)[0]] = vlc.MediaPlayer(f"{self.WAV_DIR}{i}")
		self.curr_state = None
		pygame.display.init()
		pygame.font.init()
		
		pygame.display.set_caption(TITLE)
		self.fps_clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(SIZE)
		self.SIZE = self.WIDTH, self.HEIGHT = SIZE
		self.FPS = FPS
		self.f_t = 1 / FPS
		self.time = 0
		self.lag = 0
		self.g_t = 0
		self.TRACKS_DIR = TRACKS_DIR
	
	def update(self):
		self.curr_state.update(self.g_t, self.lag)
		self.curr_state.draw()
		pygame.display.update()
		self.time, self.lag = self.chk_slp(time.time())
		self.g_t += self.time
	
	def ch_state(self, new_state, args={}):
		self.curr_state.exit()
		print("Entering new state")
		self.curr_state = None
		self.curr_state = new_state
		self.curr_state.enter(args)
		self.g_t = 0
	
	def chk_slp(self, st):
		del_t = self.fps_clock.tick_busy_loop(self.FPS) / 1000 - self.f_t
		if del_t > 0:
			print(f"Lag : {del_t}s")
			return time.time() - st, del_t
		else:
			return time.time() - st, 0


class BaseState:
	def __init__(self, fsm):
		self.fsm = fsm
		self.action_manager = ActionManager()
	
	def enter(self, args):
		print("Entering base state")
	
	def exit(self):
		self.fsm.screen.fill(rgb.WHITE)
		print("Exiting base state")
	
	def update(self, game_time, lag):
		print("Updating base state")
	
	def draw(self):
		self.fsm.screen.fill(rgb.WHITE)
		self.action_manager.draw_buttons(self.fsm.screen)


class MainMenuState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.action_manager.add_button("Start (Space)", (50, 50), (50, 50), ret="Start", key="space")
		self.action_manager.add_button("Options", (50, 150), (50, 50))
		self.action_manager.add_button("Achievements", (50, 250), (50, 50))
		self.action_manager.add_button("Editor", (50, 350), (50, 50))
		self.action_manager.add_button("Exit (Esc)", (50, self.fsm.HEIGHT - 100), (50, 50), ret="Exit", key="escape")
		
		self.font = pygame.font.SysFont('Comic Sans MS', 36)
		
		self.text_line = TextLine("Welcome and hello!", self.font, (300, 50))
	
	def update(self, game_time, lag):
		events = pygame.event.get()
		
		actions = self.action_manager.chk_actions(events)
		
		for action in actions:
			if action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
			
			elif action == "Start":
				self.fsm.ch_state(SelectTrackState(self.fsm))
			
			elif action == "Options":
				self.fsm.ch_state(SettingsState(self.fsm))
			
			elif action == "Achievements":
				self.fsm.ch_state(AchievementsState(self.fsm))
			
			elif action == "Editor":
				self.fsm.ch_state(EditTextState(self.fsm))
	
	def draw(self):
		super().draw()
		self.text_line.draw(self.fsm.screen)


class SelectTrackState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.tracks = listdir(self.fsm.TRACKS_DIR)
		for i, file in enumerate(self.tracks):
			self.action_manager.add_button(file, (375, i * 100 + 50), (50, 50), canScroll=True)
		
		self.action_manager.add_button("Exit (Esc)", (50, self.fsm.HEIGHT - 100), (50, 50), ret="Exit", key="escape")
		self.action_manager.add_button("Back (Backspace)", (50, 50), (50, 50), ret="Back", key="backspace")
	
	def update(self, game_time, lag):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.fsm.ch_state(ExitState(self.fsm))
		actions = self.action_manager.chk_actions(events)
		
		for action in actions:
			if action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
			elif action == "Back":
				self.fsm.ch_state(MainMenuState(self.fsm))
			elif action in self.tracks:
				print(f"Playing {action}")
				self.fsm.ch_state(PlayGameState(self.fsm), {"file_name": action})
	
	def draw(self):
		super().draw()


class SettingsState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.action_manager.add_button("Back", (50, 50), (50, 50))
		self.action_manager.add_button("Exit (Esc)", (50, self.fsm.HEIGHT - 100), (50, 50), ret="Exit", key="escape")
		self.action_manager.add_button("Restore", (50, 150), (50, 50), ret="Restore defaults")
		self.action_manager.add_button("defaults", (50, 200), (50, 50), ret="Restore defaults")
		self.font = pygame.font.SysFont('Comic Sans MS', 24)
	
	def enter(self, args):
		self.settings = dir(config)[:7]
		self.text = []
		
		for i, setting in enumerate(self.settings):
			val = eval(f"config.{setting}")
			self.text.append((self.font.render(f"{setting} : {val}", 1, rgb.BLACK), (300, i * 50 + 25, 10, 10)))
			self.action_manager.add_button("Change", (200, i * 50 + 25), (30, 40), ret=setting, font=self.font)
	
	def update(self, game_time, lag):
		events = pygame.event.get()
		
		actions = self.action_manager.chk_actions(events)
		
		for action in actions:
			
			if action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
			elif action == "Back":
				self.fsm.ch_state(MainMenuState(self.fsm))
			elif action in self.settings:
				self.fsm.ch_state(ChSettingState(self.fsm), {"setting": action, "value": eval(f"config.{action}")})
			
			elif action == "Restore defaults":
				reset_config()
				self.fsm.__init__()
				self.fsm.curr_state = MainMenuState(self.fsm)
				self.fsm.ch_state(SettingsState(self.fsm))
	
	def draw(self):
		super().draw()
		
		for line in self.text:
			self.fsm.screen.blit(line[0], line[1])


class ChSettingState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.font = pygame.font.SysFont('Comic Sans MS', 30)
		self.action_manager.add_button("Back", (50, 50), (50, 50))
	
	def enter(self, args):
		self.setting = args["setting"]
		self.setting_text = self.font.render(self.setting, 1, rgb.BLACK), (250, 50, 50, 50)
		self.val = args["value"]
		self.val_text = self.font.render(f"Current value : {self.val}", 1, rgb.BLACK), (250, 100, 50, 50)
	
	def update(self, game_time, lag):
		events = pygame.event.get()
		
		actions = self.action_manager.chk_actions(events)
		
		for action in actions:
			if action == "Back":
				self.fsm.ch_state(SettingsState(self.fsm))
			elif action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
	
	def draw(self):
		super().draw()
		self.fsm.screen.blit(self.setting_text[0], self.setting_text[1])
		self.fsm.screen.blit(self.val_text[0], self.val_text[1])


class AchievementsState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.action_manager.add_button("Back", (50, 50), (50, 50))
		print(data)
		self.name_font = pygame.font.SysFont('Comic Sans MS', 24)
		self.des_font = pygame.font.SysFont('Comic Sans MS', 18)
		self.text = []
		for i, achievement in enumerate(data):
			font_col = rgb.RED
			self.text.append((self.name_font.render(achievement["name"], 1, font_col), (200, i * 80 + 50, 50, 50)))
			self.text.append(
				(self.des_font.render(achievement["description"], 1, font_col), (200, i * 80 + 85, 50, 50)))
	
	def update(self, game_time, lag):
		events = pygame.event.get()
		
		actions = self.action_manager.chk_actions(events)
		
		for action in actions:
			if action == "Back":
				self.fsm.ch_state(MainMenuState(self.fsm))
	
	def draw(self):
		super().draw()
		for line in self.text:
			self.fsm.screen.blit(line[0], line[1])


class OrbModel:
	def __init__(self, x, y, duration, lane, start_time, end_time):
		self.length = duration * 450  # pixels
		
		self.x = x
		self.y = y
		self.lane = lane
		self.start_time = start_time
		self.end_time = end_time


class PlayGameState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.action_manager.add_button("Back", (50, 50), (50, 50), ret="Back", key="backspace")
		self.action_manager.add_keystroke("Pause", 'p')
		self.isPlaying = True
		self.beatmap = None
		self.orbs = []
		self.image = pygame.image.load('longrectangle.png').convert()
		
		self.score = 0
		self.score_font = pygame.font.SysFont('Comic Sans MS', 36)
		self.score_line = TextLine(str(self.score), self.score_font, (750, 50))
	
	def enter(self, args):
		self.fsm.screen.fill(rgb.WHITE)
		font = pygame.font.SysFont('Comic Sans MS', 30)
		TextLine("Loading...", font, (300, 100)).draw(self.fsm.screen)
		
		self.file = args["file_name"]
		print(f"File name = {self.file}")
		file_path = f"{self.fsm.TRACKS_DIR}{self.file}"
		with open(file_path, 'r') as file:
			reader = csv.reader(file)
			header = next(reader)
			self.beatmap = [row for row in reader]
		lanes = 4
		self.positions = [i * 35 for i in range(5, lanes + 5)]
		
		############################################################################
		
		self.laneLock = {1: False, 2: False, 3: False, 4: False}
		self.lane1 = pygame.image.load('red.png').convert()
		self.lane2 = pygame.image.load('green.png').convert()
		self.lane3 = pygame.image.load('yellow.png').convert()
		self.lane4 = pygame.image.load('purple.png').convert()
		self.laneIcons = [[(self.lane1, (self.positions[0], 490)), False], \
		                  [(self.lane2, (self.positions[1], 490)), False], \
		                  [(self.lane3, (self.positions[2], 490)), False], \
		                  [(self.lane4, (self.positions[3], 490)), False]]
		
		self.action_manager.add_sp_keystroke('f', 'f')
		self.action_manager.add_sp_keystroke('g', 'g')
		self.action_manager.add_sp_keystroke('h', 'h')
		self.action_manager.add_sp_keystroke('j', 'j')
		
		############################################################################
		
		# generating orbs
		reference_note = int(self.beatmap[0][1])
		lane = 1
		
		for beat in self.beatmap:
			diff = int(beat[1]) - reference_note
			lane = (lane + diff) % lanes
			x = self.positions[lane]
			
			end_time = float(beat[4])
			duration = float(beat[2])
			y = -end_time * 450 + 500
			start_time = float(beat[3])
			orb = OrbModel(x, y, duration, lane, start_time, end_time)
			self.orbs.append(orb)
			reference_note = int(beat[1])
		
		wav_file = self.file.rsplit('.', 1)[0]
		self.player = self.fsm.wav_files[wav_file]
		self.player.play()
	
	def update(self, game_time, lag):
		actions = self.action_manager.chk_actions(pygame.event.get())
		
		for action in actions:
			
			if action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
			
			elif action == "Back":
				self.fsm.ch_state(MainMenuState(self.fsm))
			
			elif action == "Pause":
				self.isPlaying = not self.isPlaying
				self.player.pause()
			
			if action == "f (down)":
				
				self.laneIcons[0][1] = True
			
			if action == "f (up)":
				self.laneIcons[0][1] = False
			
			if action == "g (down)":
				self.laneIcons[1][1] = True
			
			if action == "g (up)":
				self.laneIcons[1][1] = False
			
			if action == "h (down)":
				self.laneIcons[2][1] = True
			
			if action == "h (up)":
				self.laneIcons[2][1] = False
			
			if action == "j (down)":
				self.laneIcons[3][1] = True
			
			if action == "j (up)":
				self.laneIcons[3][1] = False
		
		if self.isPlaying or self.player.is_playing():
			for i in self.orbs:
				i.y += 15 * (self.fsm.f_t + lag) / self.fsm.f_t
				if i.y > 650:
					self.orbs.remove(i)
		
		if len(self.orbs) <= 0:
			print("Completed!")
			self.fsm.ch_state(GameOverState(self.fsm), {"file_name": self.file, "score": self.score})
		
		# print(game_time)
	
	def exit(self):
		pygame.mixer.music.stop()
		self.player.stop()
	
	def draw(self):
		super().draw()
		self.score_line.draw(self.fsm.screen)
		pygame.draw.line(self.fsm.screen, rgb.GREY, (0,500), (800,500), 5)
		
		for i in self.orbs:
			self.fsm.screen.blit(self.image, (round(i.x), round(i.y)), (0, 0, 30, round(i.length * 0.9)))
			
		for args, boolean in self.laneIcons:
			if boolean:
				self.fsm.screen.blit(*args)

class GameOverState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.action_manager.add_button("Retry", (200, 400), (50, 50))
		self.action_manager.add_button("Back to Main Menu", (500, 400), (50, 50), ret="Main Menu")
		self.action_manager.add_button("Back to Start", (300, 400), (50, 50), ret="Start")
		self.action_manager.add_keystroke("Exit", "escape")
	
	def enter(self, args):
		self.args = args
		
		self.score = args["score"]
		self.score_font = pygame.font.SysFont('Comic Sans MS', 36)
		self.score_line = TextLine(f"Score : {self.score}", self.score_font, (350, 100))
	
	def update(self, game_time, lag):
		events = pygame.event.get()
		
		actions = self.action_manager.chk_actions(events)
		
		for action in actions:
			if action == "Retry":
				self.fsm.ch_state(PlayGameState(self.fsm), self.args)
			
			elif action == "Main Menu":
				self.fsm.ch_state(MainMenuState(self.fsm))
			
			elif action == "Start":
				self.fsm.ch_state(SelectTrackState(self.fsm))
			
			elif action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
	
	def draw(self):
		super().draw()
		self.score_line.draw(self.fsm.screen)


class EditTextState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.action_manager.add_button("Back", (50, 50), (50, 50))
		self.alphabet = list(string.printable)
		self.action_manager.add_keystroke("backspace", "backspace")
		self.action_manager.add_keystroke("space", "space")
		self.action_manager.add_keystroke("enter", "return")
		self.action_manager.add_keystroke("caps lock", "caps lock")
		self.action_manager.add_keystroke("shift", "left shift")
		self.action_manager.add_keystroke("shift", "right shift")
		
		for i in self.alphabet:
			self.action_manager.add_keystroke(i, i)
		
		self.font = pygame.font.SysFont('Comic Sans MS', 30)
		self.title = TextLine("Text entered:", self.font, (300, 50))
		self.text_pos = (200, 250)
		self.text_size = (400, 400)
		self.text = TextBox("", self.font, self.text_pos, self.text_size)
		self.confirmed_text = TextBox("", self.font, self.text_pos, self.text_size)
		self.string = ""
		self.confirmed_str = ""
		self.isUppercase = False
		self.isCaps_lock = False
	
	def update(self, game_time, lag):
		actions = self.action_manager.chk_actions(pygame.event.get())
		for action in actions:
			if action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
			
			elif action == "Back":
				self.fsm.ch_state(MainMenuState(self.fsm))
			
			elif action == "backspace":
				self.string = self.string[:-1]
			
			elif action == "space":
				self.string += ' '
			
			elif action == "enter":
				self.confirmed_str = self.string
				self.confirmed_text = TextBox(self.confirmed_str, self.font, (200, 100), self.text_size)
			
			elif action == "shift":
				self.isUppercase = not self.isCaps_lock
			
			elif action == "caps lock":
				self.isCaps_lock = not self.isCaps_lock
			
			elif action in self.alphabet:
				if self.isUppercase:
					self.string += action.upper()
				else:
					self.string += action
		
		self.isUppercase = self.isCaps_lock
		
		self.text = TextBox(self.string, self.font, self.text_pos, self.text_size)
	
	def draw(self):
		super().draw()
		self.title.draw(self.fsm.screen)
		self.text.draw(self.fsm.screen)
		self.confirmed_text.draw(self.fsm.screen)


class ExitState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
	
	def enter(self, args):
		print("Exiting program")
		pygame.quit()
		exit()


if __name__ == "__main__":
	
	fsm = State_Manager()
	fsm.curr_state = MainMenuState(fsm)
	while True:
		fsm.update()
