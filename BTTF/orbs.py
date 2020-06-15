import pygame, os, sys
from pygame.locals import *
from MELODY_GENERATOR import *



class OrbModel:
    def __init__(self, x, y, duration, color=None):
        self.length = duration * 50  # pixels
        self.width = 100

        self.x = x
        self.y = y
        self.color = color


class OrbsController:
    def __init__(self, screen_width, no_of_lanes, initialframeticks):
        self.framecount = initialframeticks
        self.currentframecount = initialframeticks
        self.lanes = no_of_lanes
        self.orbs = []

        # will be using a 30 x 1000 PNG to represent an orb.
        self.positions = [i*35 for i in range(self.lanes)]

        #generating orbs
        reference_note = beat_map[0][1].note
        lane = 0

        y = 0
        for beat in beat_map:
            # (relativeTime, Note object)
            diff = beat[1].note - reference_note
            lane = (lane + diff) % self.lanes
            x = self.positions[lane]
            y -= beat[0] * 100
            duration = beat[1].duration
            orb = OrbModel(x, y, duration)
            self.orbs.append(orb)
            reference_note = beat[1].note

        # print(len(self.orbs))



    def update(self, gameTime):
        self.currentframecount -= gameTime
        if self.currentframecount < 0:
            self.currentframecount += self.framecount
            for i in self.orbs:
                i.y += 2
                if i.y > 650:
                    self.orbs.remove(i)

class OrbView:
    def __init__(self, OrbsController, imgpath):
        self.image = pygame.image.load(imgpath)
        self.map = OrbsController

    def render(self, surface):
        for i in self.map.orbs:
            surface.blit(self.image, (i.x, i.y), (0, 0, 30, i.length))




pygame.init()
fpsClock = pygame.time.Clock()
mainSurface = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Test')

black = pygame.Color(0, 0, 0)

orbsController = OrbsController(800, 10, 20)
orbView = OrbView(orbsController, 'longrectangle.png')

player.play()

while True:
    mainSurface.fill(black)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    orbView.render(mainSurface)
    orbsController.update(fpsClock.get_time())
    pygame.display.update()
    fpsClock.tick(60)
    # always keep refresh frequency below fps
