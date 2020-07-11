from os import listdir
import vlc
from sys import exit

import pygame

class Foo:
	def __init__(self):
		self.wav_files= []
		for i in listdir(".\\wav_files\\"):
			self.wav_files.append(vlc.MediaPlayer(f".\\wav_files\\{i}"))

def playall():
	for i in Foo().wav_files:
		i.play()


if __name__ == "__main__":
	
	playall() # Here there is no error

	pygame.mixer.init()
	pygame.display.init()

	screen = pygame.display.set_mode((600, 400))
	
	# playall() # Here there is an error
		
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()


