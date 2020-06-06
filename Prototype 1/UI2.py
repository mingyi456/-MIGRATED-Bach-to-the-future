import pygame
from time import sleep
from time import time as tk_time
from sys import exit
import note_parser
import rgb
from os import listdir

pygame.init()
font= pygame.font.SysFont('Comic Sans MS', 30)
SIZE= WIDTH, HEIGHT= 800,600
FPS= 30
screen= pygame.display.set_mode(SIZE)
pygame.display.set_caption("Prototype 1")
f_t= 1/float(FPS)

files= listdir(".\\tracks")
print(files)


def chk_exit(events):
	for event in events:
		if event.type == pygame.QUIT: exit()

def chk_slp(st, gt):
	c_t= tk_time()
	del_t= f_t - c_t + st
	if del_t < 0:
		print(f"Lag : {-del_t}s")
		return c_t, -del_t, gt + f_t - del_t
	else:
		sleep(del_t)
		return c_t, 0, gt + f_t


def StartGame(file_name):
	notes= note_parser.parse(file_name)
	pygame.mixer.music.load(".\\tracks\\" + file_name)
	
	gt= 0
	lag= 0
	st= tk_time()
	pygame.mixer.music.play()
	
	while True:
		events= pygame.event.get()
		chk_exit(events)
		screen.fill((255, 255, 255))
		draw_notes(notes, gt)
		pygame.display.flip()
		st, lag, gt= chk_slp(st, gt)

def EndGame():
	end_buttons= []
	button( (225, 275), (50, 50), rgb.BLACK, name= "Choose Level", group= end_buttons)
	button( (525, 275), (50, 50), rgb.BLACK, name= "Quit", group= end_buttons)
	gt= 0
	lag= 0
	st= tk_time()
	pygame.mixer.music.stop()

	while True:
		events= pygame.event.get()

		chk_exit(events)

		screen.fill(rgb.WHITE)

		if chk_buttons(events, end_buttons) == "Quit":
			pygame.quit()
			exit()
		
		elif chk_buttons(events, end_buttons) == "Choose Level":
			SelectStage()

		draw_buttons(end_buttons)

		pygame.display.flip()

		st, lag, gt= chk_slp(st, gt)


def draw_notes(group, gt):
    for note in group:

        if note.rect[1] >= HEIGHT:
            group.remove(note)
            continue

        if note.time <= gt:
            pygame.draw.rect(screen, note.colour, note.rect)
            note.rect[1] += 5

        else:
            return

    if len(group) == 0:
        EndGame()

def is_within(point, rect):
	if point[0] > rect[0] and point[0] < (rect[0] + rect[2]):
		if point[1] > rect[1] and point[1] < (rect[1] + rect[3]):
			return True
	return False

buttons= []
class button():
	def __init__(self, pos, size, colour, hl_colour= rgb.YELLOW, name= "Untitled", group= buttons):
		self.name= name
		self.coords= list([pos[0], HEIGHT-pos[1]])
		self.size= list(size)
		self.rect= self.coords+self.size
		self.def_colour= self.colour= colour
		self.hl_colour= hl_colour
		group.append(self)

def draw_buttons(group= buttons):
	for button in group:
		text= font.render(button.name, 1, rgb.GREY)
		text_len= text.get_width()
		button.rect[2]= max( ( text_len, button.rect[2]))

		pygame.draw.rect(screen, button.colour, button.rect)
		screen.blit(text, button.rect)

def chk_buttons(events, group= buttons):
	curr_pos= pygame.mouse.get_pos()
	for event in events:

		if event.type == pygame.MOUSEBUTTONDOWN:

			if event.button == 1:

				for button in group:

					if is_within(curr_pos, button.rect):
						button.colour= button.hl_colour

						print(f"Button \"{button.name}\" clicked!")
						return button.name

				print("No buttons clicked!")
				return

		elif event.type == pygame.MOUSEBUTTONUP:

			for button in group:
				button.colour= button.def_colour

			return

	for button in group:
		if is_within(curr_pos, button.rect):
			button.colour= rgb.GREY
		else:
			button.colour= button.def_colour


def MainMenu(st= tk_time(), lag= 0, gt= 0):
	button( (375, 450), (50, 50), rgb.BLACK, name= "Choose Level")
	button( (375, 150), (50, 50), rgb.BLACK, name= "Quit")
	while True:
		events= pygame.event.get()

		chk_exit(events)

		screen.fill(rgb.WHITE)

		if chk_buttons(events, buttons) == "Quit":
			pygame.quit()
			exit()
		
		elif chk_buttons(events, buttons) == "Choose Level":
			SelectStage()

		draw_buttons(buttons)

		pygame.display.flip()

		st, lag, gt= chk_slp(st, gt)
		
def SelectStage(st= tk_time(), lag= 0, gt= 0):
	buttons_stages= []
	
	button( (50, HEIGHT-50), (50, 50), rgb.BLACK, name= "Back", group= buttons_stages)
	button( (50, HEIGHT-150), (50, 50), rgb.BLACK, name= "Quit", group= buttons_stages)
	for i,file in enumerate(files):
		button( (375, i*100 + 150), (50, 50), rgb.BLACK, name= file, group= buttons_stages)

	while True:
		events= pygame.event.get()

		chk_exit(events)

		screen.fill(rgb.WHITE)
		
		draw_buttons(group= buttons_stages)

		action= chk_buttons(events, group= buttons_stages)
		if action == None:
			pass
		elif action == "Back":
			MainMenu()
		elif action == "Quit":
			pygame.quit()
			exit()
		elif action in files:
			print(f"Playing {action}!")
			StartGame(action)

		pygame.display.flip()

		st, lag, gt= chk_slp(st, gt)



MainMenu()

