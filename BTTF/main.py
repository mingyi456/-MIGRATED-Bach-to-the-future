import pygame, os, sys
from pygame.locals import *

# Our imports
from statemanager import Game
from interstitial import InterstitialState
from menu import MainMenuState
from BTTFgame import PlayGameState

BTTF = Game("BACH TO THE FUTURE", 800, 800)
mainMenuState = MainMenuState(BTTF)
gameOverState = InterstitialState(BTTF, 'G A M E  O V E R !', 5000, mainMenuState)
playGameState = PlayGameState(BTTF, gameOverState)
getReadyState = InterstitialState(BTTF, 'Get Ready!', 2000, playGameState)
mainMenuState.setPlayState(getReadyState)

BTTF.run(mainMenuState)  # initial state of the game when launched
