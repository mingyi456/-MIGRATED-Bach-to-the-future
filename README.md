#orbital2020 #LastMinuteWonders
# Bach to the Future
A classical music game that is played directly from a computer keyboard.

#### Proposed Level of Achievement: Apollo 11

## Motivation
To increase engagement with classical music works through the medium of a classical music rhythm game. Instead of passive listening, players can "tap along" to the melodies on their keyboard.\
\
*J.S. Bach, the super-musician, time travels across history and is met with the surprise of seeing music modernise over the eras. He is keen on "keeping up with the time", and he wishes to learn all of music through this great adventure!*

## Aim
To convert the wealth of classical [MIDI files](https://en.scratch-wiki.info/wiki/MIDI_Notes) present today into a fun and educational game that people can interact with using Python 3.

## Features

| No | Feature | Function |
|:--|:--|:--|
| 1 | User Interface (UI) | The entire premise of the game. Synchronising audio, visual elements with keystroke registration. Along with the ability to toggle between screens: Menu, Settings, View Achievements, Highscore and more.|
| 2 | Difficulty Levels | To ensure the game is entertaining and progressive for all players of all skill levels. |
| 3 | Scoring System | A meaningful way to quantify the player's performance that rewards combo streaks and accuracy. |
| 4 | Achievements | To encourage players to strive for excellence or even seek out easter eggs. |
| 5 | Pausing and Resuming | To prevent untimely interruptions from causing players to lose progress and possibly to accommodate music tracks that are too long to realistically play in a single short session (about 10 minutes) |
| 6 | Saving | Provision of multiple user profiles |
| 7 | Tutorial/Practice Mode | To orientate new players around the game |
| 8 | Options Page | To toggle relevant settings related to the game, even to rebind the keys for different keyboard layouts/ controllers. |
| 9 | Possible option to upload own MIDI files | To improve replayability for those who played all available stages |

## Implementation
#### Modules used: Mido, Pygame, concurrent.futures, time
### Extracting the melody information
Applying `mido.MidiFile(filename)`, we are able to parse the MIDI message bytes into messages of the following form:\

> **note_on** channel=0 **note**=43 velocity=64 **time**=0\
> note_on channel=0 note=50 velocity=69 time=0.1875\
> **note_off** channel=0 note=43 velocity=0 time=0.003125\
> note_on channel=0 note=59 velocity=88 time=0.184375\
> note_off channel=0 note=50 velocity=0 time=0.003125\

From here, we are able to derive the changes in note **pitch** and **duration**, in order to construct the visual map of the melody spread out among the lanes.

### Orbs Generator
The **melody orbs** will flow down the lanes in a **non-random** logical fashion that will emphasise on the following:\
1. Consecutive notes should not cluster on one single lane.\
2. Notes that are close in pitch should appear close visually, that clearly indicate *a sense of direction* or *recurring patterns*.\
3. If the lane pattern (musical structure) is highly repetitive, <insert bonus feature here>\
4. Some notes can give you **extra features** when you click on it (for especially difficult scenarios), to reward you with **score multipliers**, for example.

We aim to design an algorithm that is as robust as possible that would work with most cases of MIDI files, so as to realise *Feature 9*.

### Synchronising audio, visual and keystrokes
***------NOT ENTIRELY SURE AS OF NOW------***\
\
We are currently looking at using the `concurrent.futures.ProcessPoolExecutor()` to execute the different functionalities in parallel.\
If there are better ways to handle lag and ensure synchrony, please let us know!

## User Stories

| Priority | As a ... | I want to ... | So that I can |
|:--|:--|:--|:--|
| *** | new player | To face an appropriate level of difficulty | Feel drawn into the game and play the game more |
| *** | returning player | To have different features and different levels | Not feel bored replaying the game |
| * | experienced player/ tinkerer | To be able to input my own MIDI files into the game to play | Play a wider range of possible music tracks |

## Program Flow
<img width="838" alt="programflow" src="https://user-images.githubusercontent.com/65040076/83293191-fe27e480-a21d-11ea-8e67-398cc8cc2b75.png">

![](./Program Flow.svg)

## [Project Log](https://docs.google.com/spreadsheets/d/1cvhibKC6C2piTqb6wom9Ge8BIiDPPLDGw0afi3QZ9Ro/edit?usp=sharing)

## Authors
<table>
  <tr>
    <td align="center"><img src="https://avatars.githubusercontent.com/chence08" width="100px;" alt=""/><br /><sub><b>Chen YiJia</b></sub><br /></td>
    <td align="center"><img src="https://avatars.githubusercontent.com/mingyi456" width="100px;" alt=""/><br /><sub><b>Chen Mingyi</b></sub><br /></td>
  </tr>
<table>

