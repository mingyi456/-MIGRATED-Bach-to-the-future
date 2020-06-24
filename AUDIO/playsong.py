import pygame
from pygame.locals import *

class Print:
    def __init__(self):
        self.font = pygame.font.Font(None, 32)

    def draw(self, surface, msg, position):
        obj = self.font.render(msg, True, (255,255,255))
        surface.blit(obj, position)

pygame.init()
pygame.mixer.init()

fpsClock = pygame.time.Clock()
surface = pygame.display.set_mode((640, 480))
out = Print()

'''
When playing audio using pygame, NEVER USE THE MIDI FILES DIRECTLY. Load them up as .mp3, .wav, or .ogg
Pause and unpause does not currently work with MIDI files.

CONSIDER USING OTHER LIBRARIES TO HANDLE THE PLAYING.

Notes: there exists a module midi2audio that can be used to synthesis and play midi. KIV.
'''

pygame.mixer.music.load('Fate Symphony.wav')
song = pygame.mixer.music
song.play(-1)

# Refer to textbook for alternate implementation using pygame.mixer.Sound(filename)
# However, it is highly restrictive on file types. Currently work on playershoot.wav

running = True  # To keep the program running while the music is playing
paused = False  # Is the music paused
fading = False  # Is the music fading out
volume = 1  # Music volume

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.mixer.fadeout(1000)  # FADEOUT THE MUSIC FOR 1000 MILLISECONDS
        elif event.type == KEYDOWN:  # CHECK IF A KEY IS PRESSED
            if event.key == pygame.K_SPACE:  # PAUSE/UNPAUSE
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif event.key == pygame.K_ESCAPE and not fading:  # FADEOUT
                fading = True
                pygame.mixer.music.fadeout(1000)
            elif event.key == pygame.K_LEFTBRACKET:  # VOLUME DOWN
                volume -= 0.1
                volume = max(0, volume)
                song.set_volume(volume)
            elif event.key == pygame.K_RIGHTBRACKET:  # VOLUME UP
                volume += 0.1
                volume = min(1, volume)
                song.set_volume(volume)

    if not pygame.mixer.music.get_busy():  # IF AUDIO HAS STOPPED PLAYING
        running = False  # GAME QUITS

    surface.fill((0,0,0))
    out.draw(surface, 'Press <SPACE> to pause / unpause the music', (4,4))
    out.draw(surface, 'Press <ESC> to fade out and close the program', (4, 36))
    out.draw(surface, "Press [ and ] to alter the volume", (4, 68))
    out.draw(surface, f'Current volume: {volume}', (4, 100))

    pygame.display.update()
    fpsClock.tick(30)

pygame.mixer.quit()
pygame.quit()