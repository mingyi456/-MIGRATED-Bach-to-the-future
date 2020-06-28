#orbital2020 #LastMinuteWonders #MILESTONE2

# Bach to the Future

A music rhythm game that is played directly from the computer keyboard.

#### Proposed Level of Achievement: Apollo 11

## Motivation

Tap Tap Revenge was one of the original hits in music rhythm gaming, the premise of this arcade game was simple. There were orbs that flowed down from the top of the screen to give time for the player to anticipate the beats in the music. When the orbs reach the "line of action", the players were supposed to tap and hold the orb, the goal was to hit the orb **on time** and **hold on** to continue earning points. The "beatmaps" of Tap Tap Revenge were normally manually programmed by a human who would then share their map on the platform for others to play.

Our team has set out to automate this process of beatmap generation using an algorithm that works over MIDI files. We know that the classical music genre is one that is highly structured, which would be ideal for the application of our low-level algorithm. Coincidentally, it is also a highly neglected genre with a wealth of interesting information, we thought we would take this chance to make a classical-music-themed Tap Tap Revenge to fill in this gap.

#### If you are interested to try out our prototype, please ensure:

1. Python 3.6 or above
2. Dependencies installed in virtualenv: pygame, time, csv, json
3. Download the Prototype 2 folder and **run state_manager.py**

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

$$
\frac{750000}{10^6} \times \frac{3840}{960} = 3\text{ seconds}
$$

This 3 seconds refer to the **relative time** from the the previous message before the `note_on` happens. Note that we also have obtained the note **pitch** of 74.

We then pass these data through our algorithm and generate our desired map into a static csv format for fast retrieval for the Game Engine.

## 

## [Project Log](https://docs.google.com/spreadsheets/d/1cvhibKC6C2piTqb6wom9Ge8BIiDPPLDGw0afi3QZ9Ro/edit?usp=sharing)

