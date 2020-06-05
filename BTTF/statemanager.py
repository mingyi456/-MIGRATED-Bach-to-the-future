import pygame, os, sys
from pygame.locals import *

# Basic state class and State Machine Manager

class GameState:
    def __init__(self, game):
        self.game = game

    def onEnter(self, previousState):
        '''
        The base class 'GameState' does not contain any code for onEnter().
        Classes that extend 'GameState' are expected to provide their own definition.
        This method is called by the game when entering the state for the first time.
        '''
        pass

    def onExit(self):
        '''
        Same as onEnter().
        This method is called when leaving the state.
        '''
        pass

    def update(self, gameTime):
        '''
        This method is called by the game allowing the state to update itself.
        The 'gameTime' (in milliseconds) is the time since the last call to this method.
        '''
        pass

class Game:
    def __init__(self, gameName, width, height):
        pygame.init()
        pygame.display.set_caption(gameName)
        self.fpsClock = pygame.time.Clock()
        self.mainwindow = pygame.display.set_mode((width, height))
        self.background = pygame.Color(0, 0, 0)  # Pygame object for color representations
        self.currentState = None

    def changeState(self, newState):
        if self.currentState != None:
            self.currentState.onExit()  # exit currentState
        if newState == None:
            pygame.quit()
            sys.exit()

        oldState = self.currentState
        self.currentState = newState
        newState.onEnter(oldState)  # Transition to newState

    def run(self, initialState):
        self.changeState(initialState)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            gameTime = self.fpsClock.get_time()

            if self.currentState != None:
                self.currentState.update(gameTime)

            self.mainwindow.fill(self.background)  # fill mainwindow with background color
            if self.currentState != None:
                self.currentState.draw(self.mainwindow)

            pygame.display.update()
            self.fpsClock.tick(30)  # frame rate
