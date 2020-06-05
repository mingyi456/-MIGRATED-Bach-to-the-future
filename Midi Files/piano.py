import time
import pygame
import mido
from time import sleep
from time import time as tk_time
from sys import exit
pygame.init()

SIZE= WIDTH, HEIGHT= 800,700
FPS= 30
screen= pygame.display.set_mode(SIZE)
pygame.display.set_caption("Prototype Piano 1")
f_t= 1/float(FPS)


notes= []
class note():
    def __init__(self, pos, size, time, colour= (0,0,0), group= notes):
        self.pos= list([pos[0], HEIGHT- pos[1]])
        self.size= list(size)
        self.time= time
        self.colour= colour
        self.rect= self.pos + self.size
        group.append(self)

def chk_exit(events):
    for event in events:
        if event.type == pygame.QUIT: exit()

def chk_slp(st, gt):
    c_t= tk_time()
    del_t= f_t - c_t + st
    if del_t < 0:
        print(f"Lag : {-del_t}s")
        return c_t, -del_t, gt + f_t - del_t
    else:
        sleep(del_t)
        return c_t, 0, gt + f_t

def draw_notes(group= notes):
    for note in notes:
        if note.time <= gt:
            pygame.draw.rect(screen, note.colour, note.rect)
            note.rect[1] +=5
        if note.rect[1] >= HEIGHT:
            notes.remove(note)

    if len(notes) == 0:
            exit()


file_name= "beethoven_furelise.mid"

pygame.mixer.music.load(file_name)
pygame.mixer.music.play()
mid= mido.MidiFile(file_name)
msgs= []
clean= list(filter(lambda x: x.type == "note_on" or x.type == "note_off", mid))
abs_time= 0
for msg in clean:
    abs_time += msg.time
    msgs.append([msg.type, msg.note, msg.time, abs_time])

n_on= []
n_off= []

for msg in msgs:
    if msg[0] == "note_on":
        n_on.append(msg[1:])
    else:
        n_off.append(msg[1:])

for i1 in n_on:
    for i2 in n_off:
        if i1[0] == i2[0] and i2[-1] > i1[-1]:
            i1.append(i2[-1])
            break
min_n= 999
max_n= 0

for i in n_on:
    pos=  int(round((i[0] - 41)/3.5)) * 100 + 25, HEIGHT
    size= 50, int(round ( i[-1] - i[-2] )) * 50
    time= i[-2]
    note(pos, size, time)


#note( (100, 200), (50, 50), 3)

st= tk_time()
gt= 0
lag= 0

while True:
    events= pygame.event.get()
    chk_exit(events)
    screen.fill((255, 255, 255))
    draw_notes(notes)
    pygame.display.flip()
    st, lag, gt= chk_slp(st, gt)
