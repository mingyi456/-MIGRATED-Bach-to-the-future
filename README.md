

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



## Full Features



