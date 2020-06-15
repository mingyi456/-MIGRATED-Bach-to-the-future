import pygame, os, sys
from pygame.locals import *
from statemanager import *

class PlayGameState(GameState):
    def __init__(self, game, gameOverState):
        super().__init__(game)

    def draw(self, surface):
        
        pygame.draw.rect(surface, (255, 0, 0), (50, 50, 50, 50))

