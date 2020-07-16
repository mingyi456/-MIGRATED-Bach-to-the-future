import pygame, os, sys
from pygame.locals import *

pygame.mixer.init()
shootSound = pygame.mixer.Sound('Sheep may safely graze.ogg')
shootSound.play()
while pygame.mixer.get_busy():
    pass
pygame.mixer.quit()