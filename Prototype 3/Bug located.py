from os import listdir
import vlc
from sys import exit
from time import sleep
import pygame


if __name__ == "__main__":
	
	pygame.display.init()
	pygame.mixer.init()
	pygame.display.set_mode((600, 400))
	
	player= vlc.MediaPlayer("./wav_files/pavane.wav")
	player.play()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
