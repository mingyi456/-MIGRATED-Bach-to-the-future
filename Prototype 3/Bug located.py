# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 02:15:34 2020

@author: user
"""
import config
from os import listdir, getcwd
import vlc
from time import sleep

import pygame






class Foo:
	def __init__(self):
		self.wav_files= []
		for i in listdir(".\\wav_files\\"):
			self.wav_files.append(vlc.MediaPlayer(f".\\wav_files\\{i}"))



if __name__ == "__main__":

	files= Foo()
		
	for i in files.wav_files:
		i.play()
	
	pygame.display.init()
	pygame.font.init()
	fps_clock = pygame.time.Clock()
	screen = pygame.display.set_mode((600, 400))
	pygame.mixer.quit()


sleep(30)
