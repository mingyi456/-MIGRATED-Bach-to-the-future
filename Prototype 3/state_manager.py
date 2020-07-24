from sys import exit
import rgb
from os import listdir, path, environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
import pygame
from UIManager import ActionManager, TextLine
import csv
import vlc
from data_parser import get_config, ch_config, get_user_data, update_user_data, get_sys_config, get_achievements, reset_config

class State_Manager:
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
	
# SUSTAINS HAVE AREA, SO LENGTH == 3, HEADS ONLY LENGTH == 2

class Orbs:
	def __init__(self, x, end_time, start_time, duration, lane, sustained, speed, offset, sustainTrim):
		self.x = x + 10
		self.tail_y = -end_time * speed + offset  # ensure sound always before visual, 0.1 reaction time
		self.head_y = -start_time * speed + offset
		self.length = duration * speed
		self.lane = lane
		self.sustained = sustained
		self.sustainTrim = sustainTrim
		
		# ASSETS
		raw_paths= get_sys_config()
		ASSETS_DIR = path.join(*raw_paths["Assets"])
		self.heads = [pygame.image.load(f"{ASSETS_DIR}lane1_orb.png").convert_alpha(), \
					  pygame.image.load(f"{ASSETS_DIR}lane2_orb.png").convert_alpha(), \
					  pygame.image.load(f"{ASSETS_DIR}lane3_orb.png").convert_alpha(), \
					  pygame.image.load(f"{ASSETS_DIR}lane4_orb.png").convert_alpha()]
		self.sustains = [pygame.image.load(f"{ASSETS_DIR}lane1_sustain.png").convert_alpha(), \
						 pygame.image.load(f"{ASSETS_DIR}lane2_sustain.png").convert_alpha(), \
						 pygame.image.load(f"{ASSETS_DIR}lane3_sustain.png").convert_alpha(), \
						 pygame.image.load(f"{ASSETS_DIR}lane4_sustain.png").convert_alpha()]
		
	def blits(self):
		result = []
		if self.sustained:
			result.append([self.sustains[self.lane], \
			               [self.x+12, self.tail_y + 30 + self.length * (1-self.sustainTrim)], \
			               (0, 0, 36, self.length * self.sustainTrim)])
		result.append([self.heads[self.lane], [self.x, self.head_y]])
		return result

class PlayGameState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		self.action_manager.add_button("Back", (self.fsm.WIDTH-100, 50), (50, 30), ret="Back", key="backspace")
		self.action_manager.add_keystroke("Pause", 'p')
		self.action_manager.add_keystroke("Vol+", "up")
		self.action_manager.add_keystroke("Vol-", "down")
		self.lineOfGoal = 510
		self.orb_spd = 450
		self.errorMargin = 6
		self.rangeOfGoal = (self.lineOfGoal - self.orb_spd/self.fsm.FPS * self.errorMargin, self.lineOfGoal + self.orb_spd/self.fsm.FPS * self.errorMargin)
		self.sustainTrim = 0.8  # 1 for no Trim
		self.baseScore = 50
		self.meter_bar = pygame.image.load(f"{self.fsm.ASSETS_DIR}meter_bar.png").convert_alpha()
		
		self.isPlaying = True
		self.orbs = []
		
		self.laneNo = 4
		self.positions = [480/self.laneNo + 80 * i for i in range(6)]
		self.grids = (pygame.image.load(f"{self.fsm.ASSETS_DIR}lane_topblack.png").convert_alpha(), \
					  pygame.image.load(f"{self.fsm.ASSETS_DIR}lane_bottomblack.png").convert_alpha())
		self.gridBlits = [(pygame.image.load(f"{self.fsm.ASSETS_DIR}meter.png").convert_alpha(), (0, 0))]
		for i in range(self.laneNo):
			self.gridBlits.append((self.grids[i%2], (self.positions[i], 0)))
		
		self.lanes = [(pygame.image.load(f"{self.fsm.ASSETS_DIR}lane1.png").convert_alpha(), (self.positions[0], 490)), \
					  (pygame.image.load(f"{self.fsm.ASSETS_DIR}lane2.png").convert_alpha(), (self.positions[1], 490)), \
					  (pygame.image.load(f"{self.fsm.ASSETS_DIR}lane3.png").convert_alpha(), (self.positions[2], 490)), \
					  (pygame.image.load(f"{self.fsm.ASSETS_DIR}lane4.png").convert_alpha(), (self.positions[3], 490)), \
					  (pygame.image.load(f"{self.fsm.ASSETS_DIR}lane5.png").convert_alpha(), (self.positions[4], 490)), \
					  (pygame.image.load(f"{self.fsm.ASSETS_DIR}lane6.png").convert_alpha(), (self.positions[5], 490))]
		self.laneBlits = self.lanes[:self.laneNo]
		
		self.key_bindings= ['f', 'g', 'h', 'j', 'k', 'l'][:self.laneNo]
		self.key_binds = [eval(f"pygame.K_{x}") for x in self.key_bindings]
		print(self.key_binds)  # [('f', int)]
		
		for key in self.key_bindings:
			self.action_manager.add_sp_keystroke(key, key)
		
		self.score = 0
		self.score_font = pygame.font.Font(self.fsm.SYSFONT, 24)
		self.score_line = TextLine(str(self.score), self.score_font, (550, 50))
		
		self.countdown = self.fsm.FPS * 5
		self.start_timer= self.fsm.FPS * 3
		self.hasStarted= False
		self.start_timer_text= TextLine("", pygame.font.Font(self.fsm.SYSFONT, 48), (400, 300)).align_ctr()
		
	
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
			info = next(reader)
			next(reader)
			self.beatmap = [row for row in reader]
		
		self.sustainSnapshot = [False for _ in range(self.laneNo)]
		self.sustainValid = [False for _ in range(self.laneNo)]
		############################################################################
		
		self.lane_responses = [[[False, pygame.image.load(f"{self.fsm.ASSETS_DIR}lane1_press.png").convert_alpha()], \
								[False, pygame.image.load(f"{self.fsm.ASSETS_DIR}lane1_correct.png").convert_alpha()], \
								(self.positions[0], 490)], \
							   [[False, pygame.image.load(f"{self.fsm.ASSETS_DIR}lane2_press.png").convert_alpha()], \
								[False, pygame.image.load(f"{self.fsm.ASSETS_DIR}lane2_correct.png").convert_alpha()], \
								(self.positions[1], 490)], \
							   [[False, pygame.image.load(f"{self.fsm.ASSETS_DIR}lane3_press.png").convert_alpha()], \
								[False, pygame.image.load(f"{self.fsm.ASSETS_DIR}lane3_correct.png").convert_alpha()], \
								(self.positions[2], 490)], \
							   [[False, pygame.image.load(f"{self.fsm.ASSETS_DIR}lane4_press.png").convert_alpha()], \
								[False, pygame.image.load(f"{self.fsm.ASSETS_DIR}lane4_correct.png").convert_alpha()], \
								(self.positions[3], 490)]]
		self.lane_input = [False for _ in range(self.laneNo)]
		
		############################################################################

		reference_note = int(self.beatmap[0][3])
		lane = 0

		for end_time, start_time, duration, pitch, sustained in self.beatmap:
			end_time = float(end_time)
			start_time = float(start_time)
			duration = float(duration)
			pitch = int(pitch)
			sustained = sustained == 'True'
			
			diff = pitch - reference_note
			lane = (lane + diff) % self.laneNo
			x = self.positions[lane]

			orb = Orbs(x, end_time, start_time, duration, lane, sustained, self.orb_spd, self.lineOfGoal, self.sustainTrim)
			self.orbs.extend(orb.blits())
			reference_note = pitch
		
		# FULL SCORE CALCULATION
		totalNotes = int(info[0])
		sustainedNotes = int(info[1])
		totalSustainDuration = float(info[2]) * self.sustainTrim
		crotchet = float(info[8])
		self.fullScore = (totalNotes * self.baseScore) \
		                 + (totalSustainDuration / crotchet - sustainedNotes * crotchet) * self.baseScore/2
		self.scorePercentage = 0
		
		wav_file = self.file.rsplit('.', 1)[0]
		self.player = self.fsm.wav_files[wav_file]
		self.volume= int(get_config()["Default Volume"]["Value"])
		self.player.audio_set_volume(self.volume)
		
	
	def update(self, game_time, lag):
		
		deltaTime = self.fsm.fps_clock.get_time()/1000
		
		if self.start_timer < 0:
			if not self.hasStarted:
				self.hasStarted= True
				self.player.play()
				
		else:
			self.start_timer_text= TextLine(str(self.start_timer//self.fsm.FPS+1), pygame.font.Font(self.fsm.SYSFONT, 48), (400, 300)).align_ctr()
			self.start_timer -= 1
			

		if self.isPlaying and self.player.is_playing() and self.hasStarted:
			increaseY = self.orb_spd * deltaTime
			for orb in self.orbs.copy():
				orb[1][1] += increaseY
				if orb[1][1] > self.fsm.HEIGHT:
					self.orbs.remove(orb)
		
		# USE BOOLEAN FOR KEY UP AND DOWN, PUT SCORE UPDATE AT THE END OF UPDATE LOOP.
		tapSnapshot = [False for _ in range(self.laneNo)]
		for orb in self.orbs:
			# orb = source, dest, area
			if len(orb) == 3 and (orb[1][1] - 30 + orb[2][3]) > self.lineOfGoal:
				# Check for the tail of a sustained note
				lane = self.positions.index(orb[1][0] - 22)
				self.sustainSnapshot[lane] = True
			if self.rangeOfGoal[0] < orb[1][1] < self.rangeOfGoal[1] and len(orb) == 2:
				# Check for a tap
				lane = self.positions.index(orb[1][0]-10)
				tapSnapshot[lane] = True
			if len(orb) == 3 and (orb[1][1] - 30) > self.lineOfGoal:
				# Check for the head of a sustained note and terminate all boolean
				lane = self.positions.index(orb[1][0] - 22)
				self.sustainSnapshot[lane] = False
				self.sustainValid[lane] = False
		# print(self.sustainSnapshot)
		# print(tapSnapshot)
		
		actions = self.action_manager.chk_actions(pygame.event.get())
		for action in actions:
			for i in range(self.laneNo):
				if action == f"{self.key_bindings[i]} (down)":
					self.lane_responses[i][0][0] = True
					self.lane_input[i] = True
				elif action == f"{self.key_bindings[i]} (up)":
					self.lane_responses[i][0][0] = False
					self.lane_responses[i][1][0] = False
					self.lane_input[i] = False
			
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
		
		
		for i in range(self.laneNo):
			if tapSnapshot[i] and self.lane_input[i]:
				self.sustainValid[i] = True
				self.score += self.baseScore
				self.lane_responses[i][1][0] = True
			self.lane_input[i] = False
			if self.lane_responses[i][1][0]:
				self.lane_responses[i][1][0] = bool(tapSnapshot[i])  # remove fire art once note has passed.
			if self.sustainSnapshot[i] and self.sustainValid[i] and self.lane_responses[i][0][0]:
				self.score += deltaTime * self.baseScore/2
				self.lane_responses[i][1][0] = True
			
		self.score_line = TextLine(str(int(self.score)), self.score_font, (550, 50))
		self.scorePercentage = self.score/self.fullScore

		# if self.isPlaying:  # pause handling
		#     current_time = self.fsm.fps_clock.get_time()/1000
		#     increaseY = self.orb_spd * current_time
		#     for source, dest, area in self.orbblits:
		#         dest[1] += increaseY
		#         if dest[1] > self.fsm.HEIGHT:
		#             self.orbblits.remove([source, dest, area])
		
		if len(self.orbs) == 0:
			self.countdown -= 1
			if self.countdown <= 0:
				print("Track Completed!")
				if self.story:
					self.fsm.ch_state(GameOverState(self.fsm), {"file_name": self.file, "score": int(self.score), "Story": self.story_line})
				else:
					self.fsm.ch_state(GameOverState(self.fsm), {"file_name": self.file, "score": int(self.score)})
	
	def exit(self):
		self.player.stop()

	
	def draw(self):
		super().draw()
		self.fsm.screen.blits(self.gridBlits)
		self.score_line.draw(self.fsm.screen)
		
		# for pos in self.positions:
		# 	x = pos - 35
		# 	pygame.draw.line(self.fsm.screen, rgb.GREEN, (x, 0), (x, self.fsm.HEIGHT), 5)
		# pygame.draw.line(self.fsm.screen, rgb.GREEN, (self.positions[-1] + 60, 0), (self.positions[-1] + 60, self.fsm.HEIGHT), 5)
		
		# for i in self.orbs:
		# 	self.fsm.screen.blit(self.image, (i.x, round(i.y + i.length * 0.2)), (0, 0, 30, round(i.length * 0.8)))
		# 	# self.fsm.screen.blit(self.image, (i.x, round(i.y + i.length)), (0, 0, 30, round(i.length)))
		self.fsm.screen.blits(self.orbs)
		self.fsm.screen.blits(self.laneBlits)
		
		for press, correct, position in self.lane_responses:
			if press[0]:
				self.fsm.screen.blit(press[1], position)
			if correct[0]:
				self.fsm.screen.blit(correct[1], position)
		self.fsm.screen.blit(self.meter_bar, (11, 499 - self.scorePercentage * 398), (0, 0, 28, self.scorePercentage * 398))
		
		if not self.hasStarted:
			self.start_timer_text.draw(self.fsm.screen)

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
