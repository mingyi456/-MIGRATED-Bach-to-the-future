#orbital2020 #LastMinuteWonders #MILESTONE2

# Bach to the Future

A music rhythm game that is played directly from the computer keyboard.

## Poster
<img alt="Poster" src="./Milestone 2 poster Last Minute Wonders.png">

#### Proposed Level of Achievement: Apollo 11

## Motivation

Tap Tap Revenge was one of the original hits in music rhythm gaming, the premise of this arcade game was simple. There were orbs that flowed down from the top of the screen to give time for the player to anticipate the beats in the music. When the orbs reach the "line of action", the players were supposed to tap and hold the orb, the goal was to hit the orb **on time** and **hold on** to continue earning points. The "beatmaps" of Tap Tap Revenge were normally manually programmed by a human who would then share their map on the platform for others to play.

Our team has set out to automate this process of beatmap generation using an algorithm that works over MIDI files. We know that the classical music genre is one that is highly structured, which would be ideal for the application of our low-level algorithm. Coincidentally, it is also a highly neglected genre with a wealth of interesting information, we thought we would take this chance to make a classical-music-themed Tap Tap Revenge to fill in this gap.

#### If you are interested to try out our prototype, please ensure:

1. Python 3.6 or above

2. Dependencies installed in virtualenv: pygame, python-vlc

3. Download the Prototype 2 folder and **run state_manager.py**

#### After launching:

1. Click on buttons to navigate the UI.

2. During the game, the key map consists of the f, g, h, j keys. They correspond to the 1st to 4th lanes. Press p to pause and unpause.

3. When the song finishes (after a short delay), there will be a screen showing the score reached. Click on the buttons to retry, or return to previous menus.

## Features

| S/N  | Feature                       | Function                                                     | Achieved |
| ---- | ----------------------------- | ------------------------------------------------------------ | -------- |
| 1    | Toggling between screens      | Main Menu, Achievements, Song Selection, Settings, Entering game.<br />Framework for more screens in the future. | ✅        |
| 2    | Game Engine                   | 1. Visual and audio synchronisation<br />2. Score updating<br />3. Pausing and Resuming | ✅        |
| 3    | User Profiles                 | Multiple game profiles can be created and deleted if required. | ✅        |
| 4    | Saving game progress          | Keeping track of achievements and highscores for every profile. | ✅        |
| 5    | Settings update               | Changing and preserving settings changes.<br />Factory reset of settings or entire game. | ✅        |
| 6    | Varied difficulties           | Songs have been curated to offer different difficulties for a progressive experience | ✅*       |
| 7    | Storyline                     | An engaging visual novel campaign style that leads you into different songs | ❌        |
| 8    | Visual Refinement             | Implementation of a coherent pixel art theme to all parts of the game to make it look better. | ❌        |
| 9    | Uploading your own MIDI Files | Proof of concept of a general purpose beatmap generator      | ❌        |

✅* - not very well done

## Implementation

### Beatmap Generation

Using the [mido](https://mido.readthedocs.io/en/latest/) module, we parse a MIDI file into useful attributes like:

```python
import mido
mid = mido.MidiFile('Pavane.midi')

for track in mid.tracks:  # TRACKS
	print(track)

for msg in mid.tracks[1]:  # MESSAGES IN 'Flute' TRACK
	print(msg)
```
**Tracks**

```python
<midi track 'Pavane' 24 messages>
<midi track 'Flute' 516 messages>
<midi track 'Oboe' 340 messages>
<midi track 'Clarinet in Bb' 404 messages>
<midi track 'Bassoon' 216 messages>
```

**Note Data**

```python
program_change channel=0 program=73 time=0
control_change channel=0 control=121 value=0 time=0
control_change channel=0 control=64 value=0 time=0
control_change channel=0 control=91 value=52 time=0
control_change channel=0 control=10 value=70 time=0
control_change channel=0 control=7 value=95 time=0
<meta message track_name name='Flute' time=0>
note_on channel=0 note=74 velocity=42 time=3840  # in ticks
note_on channel=0 note=76 velocity=42 time=1680
note_off channel=0 note=74 velocity=0 time=30
note_off channel=0 note=76 velocity=0 time=195
note_on channel=0 note=77 velocity=50 time=15
note_on channel=0 note=79 velocity=53 time=1680
```

Here, in order to resolve time=3840 (ticks) in to seconds, a formula is applied. This song has a tempo of 750000 and a ticks_per_beat of 960

<center>Time in seconds = (750000 / 10^6) * (3840 / 960) = 3</center>
This 3 seconds refer to the **relative time** from the the previous message before the `note_on` happens. Note that we also have obtained the note **pitch** of 74.

We then pass these data through our algorithm and generate our desired map into a **static csv format** for fast retrieval for the Game Engine.

### Game Engine Philosophy

Pygame is a simple Python wrapper around Simple DirectMedia Layer (SDL), which allows us to utilise the power of SDL in a simple to use language, Python at the cost of performance. Nevertheless, many of Python's speed limitations can be skirted through careful use of list comprehension, or other techniques rather than using brute force iteration for everything as in C. SDL has quite a few limitations in rendering, (limited functionality when using hardware accelerated rendering), so a relatively modern / high-end CPU (tested and developed on i7 8750H and i7 9750H) is necessary to run this game smoothly. 

We are aware of the limitation of pygame's Clock.tick_busy_loop() in that it only serves as an upper bound to frame rate and cannot. We aimed for a constant FPS of 30 to ensure the orbs would move at a constant speed. Thus, using this function alone would mean that momentary dips in FPS will cause the orbs to lag behind permanently. 

To workaround this, we wrapped this function in our own function which takes the return value of Clock.tick_busy_loop() and compares it to 1/30 (the actual amount of time a frame is supposed to take). If there is any lag detected, the Game Engine passes the magnitude of the lag to the state's update method so that it scales the velocity accordingly in the next frame. This can be verified by repositioning the window in the middle of a game (simulating a large lag spike). It can be seen that the orbs suddenly make a large jump to their supposed location instead of lagging behind. While this does not reduce the visual choppiness caused by the lower frame rate, it ensures that momentary dips in frame rate have no long term implications.





## Program Flow

<img alt="State Diagram" src="./State Diagram.svg">

## Goals for Milestone 3

* Implementation of an interactive directory explorer in the SelectTracksState to allow for categorisation of music tracks (basically sub levels within levels), and a more robust organisation of the .csv and .wav files.

* Implementation of a more robust and flexible settings page that allows saving, undoing and reverting to default for individual users without needing to restart the game. Also, more settings will be made available to the user, such as custom keybindings, screen size, colour scheme, etc. To accommodate this, the settings page will have sub-directories which group related settings together.

* A multi-user system with login (non-secure) so different users can have their own configurations, achievement progress and high scores.

* A more polished UI (less hard-coding of positions) so that it scales properly regardless of screen size and font. Scrolling rate currently fixed regardless of mouse wheel speed, and a workaround to allow variable rate scrolling is planned.

* A proper storyline is planned, with art assets and simple animations, to increase the sense of immersion for players. A tutorial mode will help orient new players, while a practice mode with easier song tracks and more visual hints helps players hone their skills. 

* A sandbox mode allows players to bypass the storyline if they wish to and just play any track available. They can also upload their own MIDI tracks in this mode to play.



## [Video](https://www.youtube.com/watch?v=9Qv3JzVdR2c&t=1s)

## [Project Log](https://docs.google.com/spreadsheets/d/1cvhibKC6C2piTqb6wom9Ge8BIiDPPLDGw0afi3QZ9Ro/edit?usp=sharing)

