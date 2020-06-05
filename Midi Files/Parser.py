from mido import MidiFile

def play(mid):
    for i in mid.play():
        print(i)

if __name__ == '__main__':
    file = input('Enter filename:')
    if file:
        mid = MidiFile(file)
