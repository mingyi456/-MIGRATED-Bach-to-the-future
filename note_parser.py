import mido
import rgb
from os import listdir
from sys import exit

SIZE= WIDTH, HEIGHT= 800, 600
FPS= 30
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

files= listdir(".\\tracks")


file_name= files[2]

print(f"Track : {file_name}")

mid= mido.MidiFile(".\\tracks\\"+file_name)
msgs= []
clean= list(filter(lambda x: x.time > 0 or x.type == 'note_on' or x.type == 'note_off', mid))
abs_time= 0

for msg in clean:
	abs_time += msg.time
	if msg.type == "note_on" or msg.type == "note_off":
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
    if min_n > i[0]:
        min_n= i[0]
    if max_n < i[0]:
        max_n= i[0]
print(f"Min Note = {min_n}\nMax Note = {max_n}")

note_cols= rgb.RED, rgb.GREEN, rgb.YELLOW, rgb.BLUE

div=  (max_n - min_n)/3

for i in n_on:
	x_pos=   round(( (i[0] - min_n) / div )) * 100 + 25
	pos= x_pos, HEIGHT
	size= 50, int(round ( (i[-1] - i[-2])*20 ))
	time= i[-2]
	print(time)
	col= note_cols[x_pos // 100]
	note(pos, size, time, col)





