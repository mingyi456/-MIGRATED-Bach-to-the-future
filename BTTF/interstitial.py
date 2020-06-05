import pygame, os, sys
from pygame.locals import *
from bitmapfont import *
from statemanager import *

class InterstitialState(GameState):
    def __init__(self, game, msg, waitTimeMs, nextState):
        super().__init__(game)
        self.nextState = nextState
        self.font = BitmapFont('fasttracker2-style_12x12.png', 12, 12)
        self.message = msg
        self.waitTimer = waitTimeMs

    def update(self, gameTime):
        self.waitTimer -= gameTime
        if self.waitTimer < 0:
            self.game.changeState(self.nextState)

    def draw(self, surface):
        self.font.centre(surface, self.message, surface.get_rect().height / 2)