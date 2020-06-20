import mido
import time, concurrent.futures
import pygame

filename = '/Users/chence08/PycharmProjects/orbital/Twinkle Twinkle Little Star MIDI/Jesu-Joy-Of-Man-Desiring.midi'

mid = mido.MidiFile(filename)

'''
Goal:
TO CONVERT (ANY) MIDI FILES INTO THE FOLLOWING FORM
1. PRESERVE ACCURATE ABSOLUTE TIME FOR EVERY MIDI MESSAGE
2. ONLY FILTER OUT TOP NOTES (FOR NOW)
3. EVERY NOTE MUST HAVE BEGINNING AND END.
4. COMPILE IT INTO A LIST
5. BEGIN BY IMPLEMENTING A ONE-KEY PLAYABLE MAP
6. SCALE UPWARDS ACCORDING TO LANE NUMBERS
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

    # Filter out the TOP NOTE of every unique start_time
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

##########################
# FOR ONE KEY MODE
def melodyStreamline(lst):
    melody = []
    leftover = []
    cut_off = 0
    for start_time, note in lst:
        if start_time >= cut_off:
            melody.append(note)
            cut_off = note.end_time
        else:
            leftover.append(note)
    return melody, leftover

melody = melodyStreamline(time_map)[0]
leftover = melodyStreamline(time_map)[1]
print(len(melody), len(leftover))

def relativeTime2(lst):
    result = [(lst[0].start_time, lst[0])]
    for i in range(1, len(lst)):
        rel_time = lst[i].start_time - lst[i-1].start_time
        result.append((rel_time, lst[i]))
    return result

beat_map2 = relativeTime2(melody)

###########################


def relativeTime(lst):
    result = [(lst[0][0], lst[0][1])]
    for i in range(1, len(lst)):
        rel_time = lst[i][0] - lst[i-1][0]
        result.append((rel_time, lst[i][1]))
    return result

beat_map = relativeTime(time_map)
# for i in beat_map:
#     print(i[1].note)
# print(len(beat_map))

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTES_IN_OCTAVE = len(NOTES)
def number_to_note(number: int) -> tuple:
    assert number >= 0 and number <= 127, "number should be between 0 and 127"
    octave = number // NOTES_IN_OCTAVE - 1
    note = NOTES[number % NOTES_IN_OCTAVE]

    return note, octave

def play(lst):
    for i in lst:
        time.sleep(i[0])
        print(number_to_note(i[1].note))
    time.sleep(5)


pygame.mixer.init()
player = pygame.mixer.music
player.load(filename)


if __name__ == '__main__':
    player.play()
    play(beat_map2)


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



