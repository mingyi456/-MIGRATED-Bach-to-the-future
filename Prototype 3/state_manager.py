from sys import exit
import pygame

import rgb
from os import listdir, path
from UIManager import ActionManager, TextLine
import csv
import vlc
from data_parser import get_config, ch_config, get_user_data, update_user_data, get_sys_config, get_achievements



class State_Manager():
	def __init__(self, config= get_config()):
		
		raw_paths= get_sys_config()
		
		self.WAV_DIR = path.join(*raw_paths["WAV Directory"])
		self.wav_files = {}
		for i in listdir(self.WAV_DIR):
			self.wav_files[i.rsplit('.', 1)[0]] = vlc.MediaPlayer(f"{self.WAV_DIR}{i}")
		self.curr_state = None
		pygame.display.init()
		pygame.font.init()
		
		self.SYSFONT= "ARCADE_R.TTF"
		
		pygame.display.set_caption("Prototype 2")
		self.icon= pygame.image.load("quaver.png")
		pygame.display.set_icon(self.icon)
		self.fps_clock = pygame.time.Clock()
		
		self.SIZE = self.WIDTH, self.HEIGHT = eval(config["Resolution"]["Value"])
		self.screen = pygame.display.set_mode(self.SIZE)
		self.FPS = int(config["FPS"]["Value"])
		self.f_t = 1 / self.FPS
		self.time = 0
		self.lag = 0
		self.g_t = 0
		self.TRACKS_DIR = path.join(*raw_paths["CSV Directory"])
	
	def update(self):
		self.curr_state.update(self.g_t, self.lag)
		self.curr_state.draw()
		pygame.display.update()
		self.time, self.lag = self.chk_slp()
		self.g_t += self.time
	
	def ch_state(self, new_state, args={}):
		self.curr_state.exit()
		print("Entering new state")
		self.curr_state = None
		self.curr_state = new_state
		self.curr_state.enter(args)
		self.g_t = 0
	
	def chk_slp(self):
		del_t = self.fps_clock.tick_busy_loop(self.FPS) / 1000 - self.f_t
		if del_t > 0:
			print(f"Lag : {del_t}s")
				
			return self.fps_clock.get_time()/1000, del_t
		else:
			return self.fps_clock.get_time()/1000, 0

class BaseState:
	def __init__(self, fsm):
		self.fsm = fsm
		self.action_manager = ActionManager()
		self.background = pygame.image.load('background.jpg').convert_alpha()
	
	def enter(self, args):
		pass
	
	def exit(self):
		self.fsm.screen.blit(self.background, (0,0))
	
	def update(self, game_time, lag):
		print("Updating base state")
	
	def draw(self):
		self.fsm.screen.blit(self.background, (0,0))
		self.action_manager.draw_buttons(self.fsm.screen)

class MainMenuState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.action_manager.add_button("Start (Space)", (50, 50), (50, 30), ret="Start", key="space")
		self.action_manager.add_button("Options", (50, 100), (50, 30))
		self.action_manager.add_button("Achievements", (50, 150), (50, 30))
		self.action_manager.add_button("Storyline", (50, 200), (50, 30))
		self.action_manager.add_button("About", (50, self.fsm.HEIGHT - 100), (50, 30))
		self.action_manager.add_button("Exit (Esc)", (50, self.fsm.HEIGHT - 50), (50, 30), ret="Exit", key="escape")
		
		self.font = pygame.font.Font(self.fsm.SYSFONT, 24)
		
		self.text_line = TextLine("~BACH TO THE FUTURE~", self.font, (300, 50))
		
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
				
			elif action == "About":
				self.fsm.ch_state(AboutState(self.fsm))
			
			elif action == "Storyline":
				from Storyline import StoryState
				self.fsm.ch_state(StoryState(self.fsm), {"file" : "storyline.json"})
			
	def draw(self):
		super().draw()
		self.text_line.draw(self.fsm.screen)

class AboutState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.font = pygame.font.Font(self.fsm.SYSFONT, 24)
		
		self.text_lines= []
		self.text_lines.append(TextLine("Bach to the Future", self.font, (200, 100)))
		self.text_lines.append(TextLine("Icon made by Freepik from www.flaticon.com", pygame.font.Font(self.fsm.SYSFONT, 14), (150, 300)))
		
		self.action_manager.add_button("Back", (50, 50), (50, 30))
		
		self.action_manager.add_button("Exit", (50, self.fsm.HEIGHT- 100), (50, 30))
		
	def update(self, game_time, lag):
		
		actions= self.action_manager.chk_actions(pygame.event.get())
		
		for action in actions:
			if action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
			elif action == "Back":
				self.fsm.ch_state(MainMenuState(self.fsm))
		
	def draw(self):
		super().draw()
		for line in self.text_lines:
			line.draw(self.fsm.screen)

		
class SelectTrackState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.tracks = listdir(self.fsm.TRACKS_DIR)
		
		for i, file in enumerate(self.tracks):
			self.action_manager.add_button(file.rsplit('.',1)[0], (375, i * 50 + 50), (50, 30), canScroll=True, ret=file)
		
		self.action_manager.scroll_max = self.action_manager.scroll_buttons[-1].rect[1] - (self.fsm.HEIGHT//4)*3
		
		self.action_manager.add_button("Exit (Esc)", (50, self.fsm.HEIGHT - 100), (50, 30), ret="Exit", key="escape")
		self.action_manager.add_button("Back (Backspace)", (50, 50), (50, 30), ret="Back", key="backspace")
	
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
		self.action_manager.add_button("Back", (50, 50), (50, 30))
		self.action_manager.add_button("Exit (Esc)", (50, self.fsm.HEIGHT - 100), (50, 30), ret="Exit", key="escape")
		self.action_manager.add_button("Restore", (50, 150), (110, 30), ret="Restore defaults")
		self.action_manager.add_button("defaults", (50, 180), (110, 30), ret="Restore defaults")
		self.font = pygame.font.Font(self.fsm.SYSFONT, 15)
	
	def enter(self, args):
		self.settings = get_config()
		self.text = []
		
		for i, setting in enumerate(self.settings):
			val = self.settings[setting]["Value"]
			self.text.append((self.font.render(f"{setting} : {val}", 1, rgb.WHITE), (300, i * 50 + 30, 10, 10)))
			self.action_manager.add_button("Change", (200, i * 50 + 25), (30, 40), ret=setting)
	
	def update(self, game_time, lag):
		events = pygame.event.get()
		
		actions = self.action_manager.chk_actions(events)
		
		for action in actions:
			
			if action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
			elif action == "Back":
				self.fsm.ch_state(MainMenuState(self.fsm))
			elif action in self.settings:
				self.fsm.ch_state(ChSettingState(self.fsm), {"setting": action, "value": self.settings[action]})
			
			elif action == "Restore defaults":
				
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
		self.font = pygame.font.Font(self.fsm.SYSFONT, 20)
		self.action_manager.add_button("Back", (50, 50), (50, 30))
	
	def enter(self, args):
		self.args= args
		self.setting = args["setting"]
		self.setting_text = self.font.render(self.setting, 1, rgb.WHITE), (250, 50, 50, 50)
		self.val = args["value"]["Value"]
		self.val_text = self.font.render(f"Current value : {self.val}", 1, rgb.WHITE), (250, 100, 50, 50)
		self.choices= args["value"]["Choices"]
		print(self.choices)

		for e, i in enumerate(args["value"]["Choices"]):		
 			self.action_manager.add_button(str(i), (250, e*50+150), (50, 30))
	
	def update(self, game_time, lag):
		events = pygame.event.get()
		
		actions = self.action_manager.chk_actions(events)
		
		for action in actions:
			if action == "Back":
				self.fsm.ch_state(SettingsState(self.fsm))
			elif action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
					
			elif action in self.choices or eval(action) in self.choices:
				print(f"Choice clicked : {eval(action)}")
				ch_config(self.setting, action)
				config2= get_config()
				self.fsm.__init__(config2)
				self.fsm.curr_state= MainMenuState(self.fsm)
				self.fsm.ch_state(SettingsState(self.fsm))

	def draw(self):
		super().draw()
		self.fsm.screen.blit(self.setting_text[0], self.setting_text[1])
		self.fsm.screen.blit(self.val_text[0], self.val_text[1])


class AchievementsState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.action_manager.add_button("Back", (50, 50), (50, 30))
		self.name_font = pygame.font.Font(self.fsm.SYSFONT, 20)
		self.des_font = pygame.font.Font(self.fsm.SYSFONT, 14)
		self.text = []
		hasAchieved= get_user_data()["Achievements"]
		print(hasAchieved)
		achievements= get_achievements()
		for i, achievement in enumerate(achievements):
			if hasAchieved[achievement["name"]]:
				font_col = rgb.WHITE
			else:
				font_col= rgb.RED				
			
			self.text.append((self.name_font.render(achievement["name"], 1, font_col), (200, i * 80 + 50, 50, 50)))
			self.text.append(
				(self.des_font.render(achievement["description"], 1, font_col), (200, i * 80 + 85, 50, 50)))
	
	def update(self, game_time, lag):
		events = pygame.event.get()
		
		actions = self.action_manager.chk_actions(events)
		
		for action in actions:
			if action == "Back":
				self.fsm.ch_state(MainMenuState(self.fsm))
			elif action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
	
	def draw(self):
		super().draw()
		for line in self.text:
			self.fsm.screen.blit(line[0], line[1])


class OrbModel:
	def __init__(self, x, y, duration, lane, end_time):
		self.length = duration * 450  # pixels
		
		self.x = x
		self.y = y
		self.lane = lane

		self.end_time = end_time
	
	def getTail(self):
		return self.y + self.length

class PlayGameState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		pygame.key.set_repeat(1)
		self.action_manager.add_button("Back", (700, 50), (50, 30), ret="Back", key="backspace")
		self.action_manager.add_keystroke("Pause", 'p')
		self.isPlaying = True
		self.beatmap = None
		self.orbs = []
		self.image = pygame.image.load('longrectangle.png').convert()
		
		self.score = 0
		self.score_font = pygame.font.Font(self.fsm.SYSFONT, 24)
		self.score_line = TextLine(str(self.score), self.score_font, (750, 50))
		
		self.orb_spd= 450
		
		self.countdown = 30 * 5
	
	def enter(self, args):
		
		self.file = args["file_name"]
		print(f"File name = {self.file}")
		file_path = f"{self.fsm.TRACKS_DIR}{self.file}"
		with open(file_path, 'r') as file:
			reader = csv.reader(file)
			next(reader)
			self.beatmap = [row for row in reader]
		lanes = 4
		self.positions = [i * 100 for i in range(1, lanes + 1)]
		
		############################################################################
		
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
		
		reference_note = int(self.beatmap[0][2])
		lane = 0
		
		for beat in self.beatmap:
			diff = int(beat[2]) - reference_note
			lane = (lane + diff) % lanes
			x = self.positions[lane]
			
			end_time = float(beat[0])
			duration = float(beat[1])
			y = -(end_time) * self.orb_spd + 498 - self.orb_spd * 0.1
			orb = OrbModel(x, y, duration, lane, end_time)
			self.orbs.append(orb)
			reference_note = int(beat[2])
		
		wav_file = self.file.rsplit('.', 1)[0]
		self.player = self.fsm.wav_files[wav_file]
		self.player.play()
	
	def update(self, game_time, lag):
		actions = self.action_manager.chk_actions(pygame.event.get())
		
		orbsONSCREEN = [orb for orb in self.orbs if orb.getTail() > 0]
		
		for action in actions:
			
			if action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
			
			elif action == "Back":
				self.fsm.ch_state(MainMenuState(self.fsm))
			
			elif action == "Pause":
				self.isPlaying = not self.isPlaying
				self.player.pause()
				if pygame.key.get_repeat() == 0:
					pygame.key.set_repeat(1)
				else:
					pygame.key.set_repeat(0)
			
			if action == "f (down)":
				for orb in orbsONSCREEN:
					if abs(orb.getTail() - 500) < 10 and orb.lane == 0:
						self.score += 1
						print("Score += 1")
				self.laneIcons[0][1] = True
			
			if action == "f (up)":
				for orb in orbsONSCREEN:
					if orb.lane == 0:
						penalty = round(0.1*max(orb.y - 500, 0))
						self.score -= penalty
						print(f"Penalty to score : -{penalty}")		
				self.laneIcons[0][1] = False
			
			if action == "g (down)":
				for orb in orbsONSCREEN:
					if abs(orb.getTail() - 500) < 10 and orb.lane == 1:
						self.score += 1
						print("Score += 1")
				self.laneIcons[1][1] = True
			
			if action == "g (up)":
				for orb in orbsONSCREEN:
					if orb.lane == 1:
						penalty = round(0.1*max(orb.y - 500, 0))
						self.score -= penalty
						print(f"Penalty to score : -{penalty}")				
				self.laneIcons[1][1] = False
			
			if action == "h (down)":
				for orb in orbsONSCREEN:
					if abs(orb.getTail() - 500) < 10 and orb.lane == 2:
						self.score += 1
						print("Score += 1")
				self.laneIcons[2][1] = True
			
			if action == "h (up)":
				for orb in orbsONSCREEN:
					if orb.lane == 2:
						penalty = round(0.1*max(orb.y - 500, 0))
						self.score -= penalty
						print(f"Penalty to score : -{penalty}")		
				self.laneIcons[2][1] = False
			
			if action == "j (down)":
				for orb in orbsONSCREEN:
					if abs(orb.getTail() - 500) < 10 and orb.lane == 3:
						self.score += 1
						print("Score += 1")
				self.laneIcons[3][1] = True
			
			if action == "j (up)":
				for orb in orbsONSCREEN:
					if orb.lane == 3:
						penalty = round(0.1*max(orb.y - 500, 0))
						self.score -= penalty
						print(f"Penalty to score : -{penalty}")		
				self.laneIcons[3][1] = False

		
		if self.isPlaying:  # pause handling
			for i in self.orbs:
				i.y += self.orb_spd * (self.fsm.fps_clock.get_time() / 1000)
				if i.y > self.fsm.HEIGHT:
					self.orbs.remove(i)
		
		if len(self.orbs) == 0:
			self.countdown -= 1
			if self.countdown <= 0:
				print("Track Completed!")
				self.fsm.ch_state(GameOverState(self.fsm), {"file_name": self.file, "score": self.score})
		
		self.score_line = TextLine(str(self.score), self.score_font, (550, 50))
	
		

		
	def exit(self):
		self.player.stop()
		pygame.key.set_repeat(0)
	
	def draw(self):
		super().draw()
		self.score_line.draw(self.fsm.screen)
		pygame.draw.line(self.fsm.screen, rgb.GREY, (0,500), (800,500), 5)
		
		for pos in self.positions:
			x = pos - 35
			pygame.draw.line(self.fsm.screen, rgb.GREEN, (x, 0), (x, 600), 5)
		pygame.draw.line(self.fsm.screen, rgb.GREEN, (self.positions[-1] + 60, 0), (self.positions[-1] + 60, 600), 5)
		
		for i in self.orbs:
			self.fsm.screen.blit(self.image, (i.x, round(i.y + i.length * 0.1)), (0, 0, 30, round(i.length * 0.9)))
			
		for args, boolean in self.laneIcons:
			if boolean:
				self.fsm.screen.blit(*args)

class GameOverState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.action_manager.add_button("Retry", (200, 400), (50, 30))
		self.action_manager.add_button("Back to Main Menu", (500, 400), (50, 30), ret="Main Menu")
		self.action_manager.add_button("Back to Start", (300, 400), (50, 30), ret="Start")
		self.action_manager.add_keystroke("Exit", "escape")
		self.high_scores= get_user_data()["Highscores"]
		self.score_font = pygame.font.Font(self.fsm.SYSFONT, 24)
		self.high_score_text= TextLine("High Score achieved!", self.score_font, (250, 300))
	
	def enter(self, args):
		self.args = args
		
		self.score = args["score"]
		self.track= args["file_name"].rsplit('.', 1)[0]
		
		center= self.fsm.WIDTH // 2

		self.score_line = TextLine(f"Score : {self.score}", self.score_font, (center, 150)).align_ctr()

		self.track_line= TextLine(self.track, self.score_font, (center, 50)).align_ctr()

		if self.high_scores[self.track] < self.score:
			print("High Score achieved!")
			self.isHighScore= True
			update_user_data(("Highscores", args["file_name"].rsplit('.', 1)[0]), args["score"])
		else:
			print("High Score not achieved")
			self.isHighScore= False			
	
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
		self.track_line.draw(self.fsm.screen)
		if self.isHighScore:
			self.high_score_text.draw(self.fsm.screen)



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
