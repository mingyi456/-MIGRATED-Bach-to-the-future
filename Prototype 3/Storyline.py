import pygame
import rgb
from UIManager import TextLine, TextBox
from state_manager import State_Manager, BaseState, ExitState, MainMenuState
import json

class StoryState(BaseState):
	def __init__(self, fsm):
		super().__init__(fsm)
		#self.action_manager.add_button("Back", (50, 50), (50, 30))
		self.action_manager.add_keystroke("space", "space", ret= "Advance")
		self.action_manager.add_keystroke("enter", "return", ret= "Advance")
		self.font1= pygame.font.Font(self.fsm.SYSFONT, 22)
		self.font2= pygame.font.Font(self.fsm.SYSFONT, 14)
		self.title= TextLine("StoryState", self.font1, (400, 50)).align_ctr()
		self.curr_text= ""
		self.text_len= 0
		self.curr_text_box= TextBox(self.curr_text , self.font2, (50, 350), (700, 250))
		self.curr_frame= 0
		self.max_frame= 0
		self.scripts= []
		self.isDone= True
	
	def enter(self, args):
		with open(args["file"]) as file:
			self.script= json.load(file)
		self.curr_line= 0
		self.max_line= len(self.script)

	def update(self, game_time, lag):
		actions= self.action_manager.chk_actions(pygame.event.get())
		for action in actions:
			if action == "Exit":
				self.fsm.ch_state(ExitState(self.fsm))
			elif action == "Back":
				self.fsm.ch_state(MainMenuState(self.fsm))
			
			elif action == "Advance":
				if self.isDone:
					self.advance(self.script[self.curr_line])
					self.curr_line += 1
					if self.curr_line > self.max_line:
						print("Scene completed!")
						self.fsm.ch_state(MainMenuState(self.fsm))
				else:
					self.curr_frame= len(self.curr_text)
		
		self.curr_text_pos= min(self.curr_frame, self.text_len)
		self.curr_text_box= TextBox(self.curr_text[:self.curr_text_pos] , self.font2, (50, 350), (700, 250))
		self.curr_frame += 1
		if self.curr_frame >= self.max_frame:
			self.isDone= True
		for file, time in self.scripts:
			if self.curr_frame <= time:
				exec(open(file).read())
		
	def advance(self, commands):
		self.curr_frame= 0
		self.isDone= False
		self.scripts= []
		self.curr_text= ""
		for command in commands:
			print(command)
			if command["Type"] == "Title":
				self.title= TextLine(command["Text"], self.font1, (400, 50)).align_ctr()
			elif command["Type"] == "Speech":
				self.curr_text= command["Text"]
				self.text_len= len(self.curr_text)
			elif command["Type"] == "Script":
				self.scripts.append((command["File"], 60))
			elif command["Type"] == "Background":
				self.background = pygame.image.load('background.jpg').convert_alpha()
				

		
		self.max_frame= len(self.curr_text)
	
	def draw(self):
		super().draw()
		self.title.draw(self.fsm.screen)
		self.curr_text_box.draw(self.fsm.screen)

if __name__ == "__main__":
	
	fsm = State_Manager()
	fsm.curr_state = MainMenuState(fsm)
	fsm.ch_state(StoryState(fsm), {"file" : "storyline.json"})
	while True:
		fsm.update()
