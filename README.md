

#orbital2020 #LastMinuteWonders #MILESTONE3

# Bach to the Future

A music rhythm game for computers!

1. [Poster](#Poster)
2. [Motivation](#Motivation)
3. [Installation](#Installation)
4. [Full Features](#Full Features)

## Poster

#### Proposed Level of Achievement: Apollo 11

## Motivation

Tap Tap Revenge was one of the original hits in music rhythm gaming, the premise of this arcade game was simple. There were orbs that flowed down from the top of the screen to give time for the player to anticipate the beats in the music. When the orbs reach the "line of action", the players were supposed to tap and hold the orb, the goal was to hit the orb **on time** and **hold on** to continue earning points. The "beatmaps" of Tap Tap Revenge were normally manually programmed by a human who would then share their map on the platform for others to play.

Our team has set out to automate this process of beatmap generation using an algorithm that works over MIDI files. We know that the classical music genre is one that is highly structured, which would be ideal for the application of our low-level algorithm. Coincidentally, it is also a highly neglected genre with a wealth of interesting information, we thought we would take this chance to make a classical-music-themed Tap Tap Revenge to fill in this gap.

## Installation

### For MacOS

1. Download the release file into your **Downloads** folder and unzip the file.

2. Make sure you have a **modern Python** version installed. As of 27 July 2020, this is [version 3.8.5](https://www.python.org/downloads/mac-osx/). Follow the link to download the required installer and follow through with the installation process with the default settings.

3. Make sure you have **[VLC player](https://get.videolan.org/vlc/3.0.11/macosx/vlc-3.0.11.dmg)** on your system.

4. Launch your **Terminal** from Applications and **paste** in the following lines. **After pasting each line, press *return* and wait for it complete.**

   1. ```bash
      xcode-select --install
      ```

   2. ```bash
      /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
      ```

   3. ```bash
      curl https://bootstrap.pypa.io/get-pip.py | sudo python3
      ```

   4. ```bash
      pip3 install pretty_midi python-vlc midi2audio
      ```

   5. ```bash
      python3 -m pip install pygame==2.0.0.dev10
      ```

   6. ```bash
      brew install fluidsynth
      ```

   7. ```bash
      cd ~/Downloads/BTTF
      ```
      
   8. ```bash
      python3 main.py
      ```
      

### For Windows

#### Source code distribution

1. Download the release (source code) file and unzip the file.

2. Make sure you have a **modern Python** version installed. As of 27 July 2020, this is [version 3.8.5](https://www.python.org/downloads/mac-osx/). Follow the link to download the required installer and follow through with the installation process with the default settings. Ensure python.exe and pip.exe are both added to the system PATH 

3. Make sure you have **[VLC player](https://get.videolan.org/vlc/3.0.11/macosx/vlc-3.0.11.dmg)** on your system.

4. Launch Command Prompt  in the directory of the downloaded file and paste the following lines. (Use the right click to paste text into the window)

	1. ```batch
		pip install pretty_midi python-vlc midi2audio psutil pygame
		```
	

	2. ```batch
		python main.py
		```

#### Compiled binary distribution

1. Download the release (binary file) and unzip the file.
2. Ensure you have the latest Microsoft Visual C++ redistributables installed.
3. Open the folder in explorer and click on the main.exe file (it helps if you sort by file type to locate it)

## Full Features

- Menu selection for Campaign, Chapter Select, Arcade Mode, Sandbox mode, Achievements, and Options with scrollable and clickable components
- A basic but functional and programmable VN engine for the campaign mode
- A campaign mode with scrolling text, fading backgrounds, moving sprites, and an advance feature to fast forward animations
- A scoring system that records streaks and represents the current score both as a number and as a meter bar
- A pause system and volume control using the up and down arrow keys during a game
- A high score and achievements recording system for each user
- A text input (restricted to lowercase letters, numbers and whitespace) system for new users to key in their name. (The numpad cannot be used to input numbers currently)
- A Users menu to switch between users
- A highly customisable sandbox mode for users to upload their own midi files, with a directory explorer implemented natively in Pygame to preserve theming, avoid extra dependencies or even potential clashes between Pygame and GUI frameworks (e.g. on MacOS launching Tkinter's file dialog prompt with an active Pygame window causes a crash)
- Various options in the sandbox configuration mode for users to select the level of note quantization, volume, tempo, or even instrument tracks using pretty-midi, midi2audio and FluidSynth as a backend
- A included FluidSynth distribution for Windows users in the source code as it is difficult to install it.
- A parser in the Arcade Mode that provides song information and current highscore of the user
- A options menu allowing users to change FPS, toggle fullscreen mode, change default game volume (values above 100 are allowed) and background volume, and even number of lanes and keybindings (any key from a-z) for different lanes in the game mode. The change applies immediately in the current game session without the need to restart. Between 1 to 6 lanes are allowed and when fewer than 6 lanes are chosen, only the first few key bindings are active. Binding the same key to multiple lanes is allowed (at your own loss of points when playing). (Unfortunately, we removed the option to change screen resolution as a design choice)

