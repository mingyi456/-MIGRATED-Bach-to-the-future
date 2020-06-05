import pygame, os, sys
from pygame.locals import *

class BitmapFont:
    def __init__(self, fontFile, width, height):
        """
        :param fontFile:
        :param width: of the individual characters
        :param height: of the individual characters
        """
        self.image = pygame.image.load(fontFile)
        self.cellWidth = width
        self.cellHeight = height
        width = self.image.get_rect().width
        height = self.image.get_rect().height
        self.cols = width / self.cellWidth  # no. of cols in grid
        self.rows = height / self.cellHeight  # no. of rows in grid

    def draw(self, surface, msg, x, y):
        for c in msg:
            ch = self.toIndex(c)
            ox = (ch % self.cols) * self.cellWidth  # x-offset
            oy = (ch / self.cols) * self.cellHeight  # y-offset
            cw = self.cellWidth
            ch = self.cellHeight
            sourceRect = (ox, oy, cw, ch)
            surface.blit(self.image, (x, y, cw, ch), sourceRect)
            x += self.cellWidth

    def centre(self, surface, msg, y):
        width = len(msg) * self.cellWidth  # pixel length of message
        halfWidth = surface.get_rect().width
        x = (halfWidth - width) / 2
        self.draw(surface, msg, x, y)

    def toIndex(self, char):
        return ord(char) - ord(' ')  # index value into the bitmap font