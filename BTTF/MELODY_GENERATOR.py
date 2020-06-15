import mido
import time, concurrent.futures
import pygame

filename = '/Users/chence08/PycharmProjects/work/BTTF/twinkle-twinkle-little-star.midi'

mid = mido.MidiFile(filename)

'''
Goal:
TO CONVERT (ANY) MIDI FILES INTO THE FOLLOWING FORM
1. PRESERVE ACCURATE ABSOLUTE TIME FOR EVERY MIDI MESSAGE
2. ONLY FILTER OUT TOP NOTES (FOR NOW)
3. EVERY NOTE MUST HAVE BEGINNING AND END.
4. COMPILE IT INTO A LIST
'''


class Note:  # Specific for mido
    def __init__(self, start_time, end_time, note):
        """
        :param start_time: absolute time
        :param end_time: absolute time
        :param note: 0-127
        """
        self.start_time = start_time
        self.end_time = end_time
        self.note = note
        self.duration = self.end_time - self.start_time

def viewfile(mid):
    # filter1 = list(filter(lambda x: x.time > 0 or x.type == 'note_on' or x.type == 'note_off', mid))
    filter1 = list(mid)
    abs_time = 0
    for msg in filter1:
        abs_time += msg.time
        msg.time = abs_time  # write over
    filter2 = list(filter(lambda x: x.type == 'note_on' or x.type == 'note_off', filter1))

    for i in range(50):
        print(filter2[i])

    # for i in mid:
    #     print(i)

# print(viewfile(mid))

def notesFilter(mid):
    # filter1 = list(filter(lambda x: x.time > 0 or x.type == 'note_on' or x.type == 'note_off', mid))
    filter1 = list(mid)
    abs_time = 0
    for msg in filter1:
        abs_time += msg.time
        msg.time = abs_time  # write over
    filter2 = list(filter(lambda x: x.type == 'note_on' or x.type == 'note_off', filter1))

    note_on = list(filter(lambda x: x.type == 'note_on' and x.velocity > 0, filter2))
    note_off = list(filter(lambda x: x.type == 'note_off' or x.velocity == 0, filter2))
    zipped = []
    for i in note_on:
        for j in note_off:
            if j.time >= i.time and i.note == j.note:
                zipped.append((i, j))
                break  # break out of inner loop as pairing is unique.

    # Repackaging for OOP
    result = []
    for _ in zipped:
        start_time = _[0].time
        end_time = _[1].time
        note = _[0].note
        result.append(Note(start_time, end_time, note))

    # Filter out the MELODY (TOP NOTE)
    melody = {}
    for note in result:
        if note.start_time not in melody:
            melody[note.start_time] = note
        elif note.note > melody[note.start_time].note:
            melody[note.start_time] = note
    return list(melody.items())

time_map = notesFilter(mid)
# for i in time_map:
#     print(i)
# print(mid.length)
# print(len(time_map))

def relativeTime(lst):
    result = [(lst[0][0], lst[0][1])]
    for i in range(1, len(lst)):
        rel_time = lst[i][0] - lst[i-1][0]
        result.append((rel_time, lst[i][1]))
    return result

beat_map = relativeTime(time_map)
# for i in beat_map:
#     print(i)
# print(len(beat_map))

def play(lst):
    beat = 0
    for i in lst:
        beat += 1
        time.sleep(i[0])
        print(beat)
    time.sleep(5)


pygame.mixer.init()
player = pygame.mixer.music
player.load(filename)


# if __name__ == '__main__':
#     player.play()
#     play(beat_map)


# Suddenly not working so well...
# if __name__ == '__main__':
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         executor.submit(play, beat_map)
#         executor.submit(player.play())

# for i in notesFilter(mid).items():
#     print(i)
#     # print(i[0].note == i[1].note, i)
#
# print(mid.length)



