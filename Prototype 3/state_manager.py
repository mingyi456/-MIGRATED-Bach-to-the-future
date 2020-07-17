from sys import exit
import rgb
from os import listdir, path, environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
import pygame
from UIManager import ActionManager, TextLine
import csv
import vlc
from data_parser import get_config, ch_config, get_user_data, update_user_data, get_sys_config, get_achievements, reset_config


class State_Manager():
	def __init__(self, config= get_config()):
		
		raw_paths= get_sys_config()
		self.ASSETS_DIR= path.join(*raw_paths["Assets"])
		self.WAV_DIR = path.join(*raw_paths["WAV Directory"])
		self.wav_files = {}
		for i in listdir(self.WAV_DIR):
			self.wav_files[i.rsplit('.', 1)[0]] = vlc.MediaPlayer(f"{self.WAV_DIR}{i}")
		self.curr_state = None
		pygame.display.init()
		pygame.font.init()
		
		self.SYSFONT= f"{self.ASSETS_DIR}ARCADE_R.TTF"
		
		pygame.display.set_caption("Prototype 3")
		self.icon= pygame.image.load(f"{self.ASSETS_DIR}quaver.png")
		pygame.display.set_icon(self.icon)
		self.fps_clock = pygame.time.Clock()
		
		self.SIZE = self.WIDTH, self.HEIGHT = eval(config["Resolution"]["Value"])
		self.isFullScreen= eval(config["Fullscreen"]["Value"])
		if self.isFullScreen:
			self.screen = pygame.display.set_mode(self.SIZE, pygame.FULLSCREEN)
		else:
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
		self.background = pygame.image.load(f"{self.fsm.ASSETS_DIR}background.jpg").convert()
	
	def enter(self, args):
		pass
	
	def exit(self):
		self.fsm.screen.blit(self.background, (0,0))
	
	def update(self, game_time, lag):
		print("Updating base state")
	
	def draw(self):
		self.fsm.screen.fill(rgb.BLACK)
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
				self.fsm.ch_state(StoryState(self.fsm), {"file" : "storyline1.json"})
			
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
		self.settings= get_config()
		self.text= []
		self.text_lines= []
		
		for i, setting in enumerate(self.settings):
			val = self.settings[setting]["Value"]
			self.text_lines.append(TextLine(f"{setting} : {val}", self.font, (300, i * 50 + 30, 10, 10)))
			self.action_manager.add_button("Change", (200, i * 50 + 25), (30, 30), ret=setting)
	
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
				reset_config()
				self.fsm.__init__()
				self.fsm.curr_state = MainMenuState(self.fsm)
				self.fsm.ch_state(SettingsState(self.fsm))
	
	def draw(self):
		super().draw()
		
		for text_line in self.text_lines:
			text_line.draw(self.fsm.screen)
		

class ChSettingState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.font = pygame.font.Font(self.fsm.SYSFONT, 20)
		self.action_manager.add_button("Back", (50, 50), (50, 30))
	
	def enter(self, args):
		self.args= args
		self.setting = args["setting"]
		self.setting_text_line= TextLine(self.setting, self.font, (250, 50))
		self.val = args["value"]["Value"]
		self.val_text_line= TextLine(f"Current value : {self.val}", self.font, (250, 100))
		
		self.choices= args["value"]["Choices"]
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
		self.setting_text_line.draw(self.fsm.screen)
		self.val_text_line.draw(self.fsm.screen)



class AchievementsState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.action_manager.add_button("Back", (50, 50), (50, 30))
		self.name_font = pygame.font.Font(self.fsm.SYSFONT, 20)
		self.des_font = pygame.font.Font(self.fsm.SYSFONT, 14)

		self.text_lines= []
		hasAchieved= get_user_data()["Achievements"]
		print(hasAchieved)
		achievements= get_achievements()
		for i, achievement in enumerate(achievements):
			
			font_col= rgb.GREEN if hasAchieved[achievement["name"]] else rgb.WHITE
			self.text_lines.append(TextLine(achievement["name"], self.name_font, (200, i * 80 + 50), font_colour= font_col))
			self.text_lines.append(TextLine(achievement["description"], self.des_font, (200, i * 80 + 85), font_colour= font_col))

	
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

		for line in self.text_lines:
			line.draw(self.fsm.screen)


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
		self.action_manager.add_button("Back", (self.fsm.WIDTH-100, 50), (50, 30), ret="Back", key="backspace")
		self.action_manager.add_keystroke("Pause", 'p')
		self.action_manager.add_keystroke("Vol+", "up")
		self.action_manager.add_keystroke("Vol-", "down")
		self.isPlaying = True
		self.beatmap = None
		self.orbs = []
		self.image = pygame.image.load(f"{self.fsm.ASSETS_DIR}longrectangle.png").convert()
		
		self.score = 0
		self.score_font = pygame.font.Font(self.fsm.SYSFONT, 24)
		self.score_line = TextLine(str(self.score), self.score_font, (750, 50))
		
		self.orb_spd= 450
		self.countdown = self.fsm.FPS * 5
	
	def enter(self, args):
		self.file = args["file_name"]
		print(f"File name = {self.file}")
		if "Story" in args.keys():
			self.story= True
			self.story_line= args["Story"]
		else:
			self.story= False
		file_path = f"{self.fsm.TRACKS_DIR}{self.file}"
		with open(file_path, 'r') as file:
			reader = csv.reader(file)
			next(reader)
			self.beatmap = [row for row in reader]
		lanes = 4
		self.positions = [i * 100 for i in range(1, lanes + 1)]
		
		############################################################################
		
		self.lane1 = pygame.image.load(f"{self.fsm.ASSETS_DIR}red.png").convert()
		self.lane2 = pygame.image.load(f"{self.fsm.ASSETS_DIR}green.png").convert()
		self.lane3 = pygame.image.load(f"{self.fsm.ASSETS_DIR}yellow.png").convert()
		self.lane4 = pygame.image.load(f"{self.fsm.ASSETS_DIR}purple.png").convert()
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
		self.volume= int(get_config()["Default Volume"]["Value"])
		print(self.volume)
		self.player.audio_set_volume(self.volume)
		self.player.play()
	
	def update(self, game_time, lag):
		
		orbsONSCREEN = [orb for orb in self.orbs if orb.getTail() > 0]
		
		actions = self.action_manager.chk_actions(pygame.event.get())
		for action in actions:
			
			if action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
			
			elif action == "Back":
				self.fsm.ch_state(MainMenuState(self.fsm))
			
			elif action == "Pause":
				self.isPlaying = not self.isPlaying
				self.player.pause()
			
			elif action == "Vol+":
				self.volume += 1
				self.player.audio_set_volume(self.volume)
				print(f"Volume : {self.player.audio_get_volume()}")
			
			elif action == "Vol-":
				self.volume= max(0, self.volume-1)
				self.player.audio_set_volume(self.volume)
				print(f"Volume : {self.player.audio_get_volume()}")
			
			elif action == "f (down)":
				pass

			elif action == "f (up)":
				pass

			elif action == "g (down)":
				for orb in orbsONSCREEN:
					if abs(orb.getTail() - 500) < 10 and orb.lane == 1:
						self.score += 1
						print("Score += 1")
				self.laneIcons[1][1] = True
			
			elif action == "g (up)":
				for orb in orbsONSCREEN:
					if orb.lane == 1:
						penalty = round(0.1*max(orb.y - 500, 0))
						self.score -= penalty
						print(f"Penalty to score : -{penalty}")				
				self.laneIcons[1][1] = False
			
			elif action == "h (down)":
				for orb in orbsONSCREEN:
					if abs(orb.getTail() - 500) < 10 and orb.lane == 2:
						self.score += 1
						print("Score += 1")
				self.laneIcons[2][1] = True
			
			elif action == "h (up)":
				for orb in orbsONSCREEN:
					if orb.lane == 2:
						penalty = round(0.1*max(orb.y - 500, 0))
						self.score -= penalty
						print(f"Penalty to score : -{penalty}")		
				self.laneIcons[2][1] = False
			
			elif action == "j (down)":
				for orb in orbsONSCREEN:
					if abs(orb.getTail() - 500) < 10 and orb.lane == 3:
						self.score += 1
						print("Score += 1")
				self.laneIcons[3][1] = True
			
			elif action == "j (up)":
				for orb in orbsONSCREEN:
					if orb.lane == 3:
						penalty = round(0.1*max(orb.y - 500, 0))
						self.score -= penalty
						print(f"Penalty to score : -{penalty}")		
				self.laneIcons[3][1] = False
		
		keys= pygame.key.get_pressed()
		
		if keys[pygame.K_f]:
			for orb in orbsONSCREEN:
				if orb.lane == 0 and orb.getTail() > 500 and orb.y < 500:
					self.score += 1
					print("Score += 1")
					break
			self.score -= 1
			self.laneIcons[0][1] = True
		
		if keys[pygame.K_g]:
			pass
		
		

		
		if self.isPlaying:  # pause handling
			for i in self.orbs:
				i.y += self.orb_spd * (self.fsm.fps_clock.get_time() / 1000)
				if i.y > self.fsm.HEIGHT:
					self.orbs.remove(i)
		
		if len(self.orbs) == 0:
			self.countdown -= 1
			if self.countdown <= 0:
				print("Track Completed!")
				if self.story:
					self.fsm.ch_state(GameOverState(self.fsm), {"file_name": self.file, "score": self.score, "Story": self.story_line})
				else:
					self.fsm.ch_state(GameOverState(self.fsm), {"file_name": self.file, "score": self.score})
		
		self.score_line = TextLine(str(self.score), self.score_font, (550, 50))
	
	def exit(self):
		self.player.stop()

	
	def draw(self):
		super().draw()
		self.score_line.draw(self.fsm.screen)
		pygame.draw.line(self.fsm.screen, rgb.GREY, (0,500), (800,500), 5)
		
		for pos in self.positions:
			x = pos - 35
			pygame.draw.line(self.fsm.screen, rgb.GREEN, (x, 0), (x, self.fsm.HEIGHT), 5)
		pygame.draw.line(self.fsm.screen, rgb.GREEN, (self.positions[-1] + 60, 0), (self.positions[-1] + 60, self.fsm.HEIGHT), 5)
		
		for i in self.orbs:
			self.fsm.screen.blit(self.image, (i.x, round(i.y + i.length * 0.1)), (0, 0, 30, round(i.length * 0.9)))
			
		for args, boolean in self.laneIcons:
			if boolean:
				self.fsm.screen.blit(*args)

class GameOverState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.action_manager.add_button("Retry", (200, 400), (50, 30))

		self.action_manager.add_keystroke("Exit", "escape")
		self.high_scores= get_user_data()["Highscores"]
		self.score_font = pygame.font.Font(self.fsm.SYSFONT, 24)
		self.high_score_text= TextLine("High Score achieved!", self.score_font, (250, 300))
	
	def enter(self, args):
		self.args = args
		
		self.score = args["score"]
		self.track= args["file_name"].rsplit('.', 1)[0]
		
		if "Story" in args.keys():
			self.story= True
			self.story_line= args["Story"]
			self.action_manager.add_button("Continue", (550, 400), (50, 30))
		
		else:
			self.action_manager.add_button("Back to Main Menu", (500, 400), (50, 30), ret="Main Menu")
			self.action_manager.add_button("Back to Start", (300, 400), (50, 30), ret="Start")			
		
		ctr= self.fsm.WIDTH // 2

		self.score_line = TextLine(f"Score : {self.score}", self.score_font, (ctr, 150)).align_ctr()

		self.track_line= TextLine(self.track, self.score_font, (ctr, 50)).align_ctr()
		
		if self.track in self.high_scores.keys():

			if self.high_scores[self.track] < self.score:
				print("High Score achieved!")
				self.isHighScore= True
				update_user_data(("Highscores", args["file_name"].rsplit('.', 1)[0]), args["score"])
			else:
				print("High Score not achieved")
				self.isHighScore= False
		else:
			print("No previous high score found")
			self.isHighScore= True
			update_user_data(("Highscores", args["file_name"].rsplit('.', 1)[0]), args["score"])
	
	
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
			
			elif action == "Continue":
				from Storyline import StoryState
				self.fsm.ch_state(StoryState(self.fsm), {"file" : "storyline1.json", "curr_line": self.story_line})
	
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
