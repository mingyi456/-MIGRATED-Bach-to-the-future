from vlc import MediaPlayer
import mido
import time
import concurrent.futures

song = 'bach_cellosuite.mid'


def player():
    MediaPlayer(song).play()


def parse(filename):
    return mido.MidiFile(filename)


def play(lst, all=True):
    sleep = time.sleep
    abs_time = 0
    for msg in lst:
        abs_time = round(abs_time + msg.time, 10)
        if all:
            sleep(msg.time)
        print(msg)
        # if msg.type == 'note_on':  # ONLY SEE THE NOTE BEING STRIKED DOWN
        #     print(msg.type, msg.note, msg.time, abs_time)


def clean(mid):
    # filter only for note_on, note_off messages.
    # together with time.
    filter1 = list(filter(lambda x: x.time > 0 \
                                    or x.type == 'note_on' or x.type == 'note_off', mid))
    # clean bach_minuet
    # filter2 = list(filter(lambda x: x.note >= 66, filter1))
    return filter1


# def tt(mid):
#     for i in mid.play():
#         print(i)




def set_tempo(filename, tpb):
    midee = mido.MidiFile(filename)
    midee.ticks_per_beat = tpb
    midee.save(filename)

mid = parse(song)


# if __name__ == '__main__':
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         executor.submit(player)
#         executor.submit(play, clean(mid), True)
