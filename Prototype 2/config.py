'''
Configuration file for global game settings such as screen dimensions, frame rate, directory to search for music tracks etc. 
Also performs a configuration test when as main.
All of these parameters will be available to edit via the "options" screen as well.
Default config will be stored as a comment at the bottom of the file.
KIV: Consider using the JSON file format and using the included JSON parser in the standard library in future.
'''

from os.path import sep

SIZE= WIDTH, HEIGHT= 800, 600

FPS= 30

NUM_LANES= 4

WINDOW_TITLE= "Prototype 2"

DEF_FONT= "Comic Sans MS"

DEF_FONT_SIZE= 30

TRACKS_DIR= f".{sep}tracks"


if __name__ == "__main__":
    try:
        from os import listdir
        listdir(TRACKS_DIR)
        from pygame import font
        font.init()
        font.SysFont(DEF_FONT, DEF_FONT_SIZE)
        print("Configuration passed")
    except:
        print("Something failed!")

# Backup config

'''
from os.path import sep

SIZE= WIDTH, HEIGHT= 800, 600

FPS= 30

NUM_LANES= 4

WINDOW_TITLE= "Prototype 2"

DEF_FONT= "Comic Sans MS"

DEF_FONT_SIZE= 30

TRACKS_DIR= f".{sep}tracks"


if __name__ == "__main__":
    try:
        from os import listdir
        listdir(TRACKS_DIR)
        from pygame import font
        font.init()
        font.SysFont(DEF_FONT, DEF_FONT_SIZE)
    except:
        print("Failed!")


'''
