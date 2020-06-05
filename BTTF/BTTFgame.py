import pygame, os, sys
from pygame.locals import *
from statemanager import *

class PlayGameState(GameState):
    def __init__(self, game, gameOverState):
        super().__init__(game)