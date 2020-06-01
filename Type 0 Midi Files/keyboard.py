from time import sleep, time
from sys import exit
import pygame
from pygame.locals import *
from pygame import mixer
import rgb
pygame.init()

SIZE= WIDTH, HEIGHT= 400, 250
BLACK= 0, 0, 0
WHITE= 255, 255, 255
GREY= 127, 127, 127
YELLOW= 255, 255, 0
FPS= 90

def chk_exit(events):
    for event in events:
        if event.type == pygame.QUIT: exit()

def chk_slp(st):
    del_t= f_t - time() + st
    if del_t < 0:
        print(f"Lag : {-del_t}s")
        return time(), -del_t
    else:
        sleep(del_t)
        return time(), 0

def is_within(point, rect):
    if point[0] > rect[0] and point[0] < (rect[0] + rect[2]):
        if point[1] > rect[1] and point[1] < (rect[1] + rect[3]):
            return True
    return False

buttons= []

class button():
    def __init__(self, pos, size, colour, hl_colour= rgb.YELLOW, name= "Untitled", group= buttons):
        self.name= name
        self.coords= list([pos[0], HEIGHT-pos[1]])
        self.size= list(size)
        self.rect= self.coords+self.size
        self.def_colour= self.colour= colour
        self.hl_colour= hl_colour
        group.append(self)

def draw_buttons(group= buttons):
    for button in group:
        pygame.draw.rect(screen, button.colour, button.rect)

def chk_buttons(events, group= buttons):
    curr_pos= pygame.mouse.get_pos()
    for event in events:

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 1:

                for button in group:

                    if is_within(curr_pos, button.rect):
                        button.colour= button.hl_colour

                        print(f"Button \"{button.name}\" clicked!")
                        return

                print("No buttons clicked!")
                return

        elif event.type == pygame.MOUSEBUTTONUP:
            
            for button in group:
                button.colour= button.def_colour

            return

    for button in group:
        if is_within(curr_pos, button.rect):
            button.colour= rgb.GREY
        else:
            button.colour= button.def_colour

    keys= pygame.key.get_pressed()

    for i in range(322):
        if keys[i]:
            print(pygame.key.name(i))



screen= pygame.display.set_mode(SIZE)
pygame.display.set_caption("Buttons")
f_t= 1/float(FPS)

st= time()
lag= 0

while pygame.mouse.get_pressed() != (1, 0, 0):
    chk_exit(pygame.event.get())

print("Start!")

b1= button( (50, 150), (50, 50), BLACK, name= "A")

b2= button( (150, 150), (50, 50), BLACK, name= "B")

b3= button( (250, 150), (50, 50), BLACK, name= "C")

while True:
    events= pygame.event.get()

    chk_exit(events)

    screen.fill(WHITE)

    chk_buttons(events, buttons)

    draw_buttons(buttons)

    pygame.display.flip()

    st, lag= chk_slp(st)
