

#orbital2020 #LastMinuteWonders #MILESTONE3

# Bach to the Future

A music rhythm game for computers!

1. [Poster](#Poster)
2. [Motivation](#Motivation)
3. [Installation](#Installation)
4. [Full Features](#Full Features)
5. [pretty_midi switch](#pretty_midi switch)
6. [Compatibility Issues](#Compatibility Issues)

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
      cd ~/Downloads/
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
2. Ensure you have the latest [Microsoft Visual C++ redistributables](https://support.microsoft.com/en-sg/help/2977003/the-latest-supported-visual-c-downloads) installed.
3. Open the folder in explorer and click on the main.exe file (it helps if you sort by file type to locate it)

## Full Features

| S/N  | Feature                       | Description                                                  | Achieved |
| ---- | ----------------------------- | ------------------------------------------------------------ | -------- |
| 1    | Menu Selection                | Selection for Campaign, Chapter Select, Arcade Mode, Sandbox mode, Achievements, and Options with scrollable and clickable components. | ✅        |
| 2    | **Visual Novel Engine**       | To handle various audiovisual assets; scriptable.            | ✅        |
| 3    | Campaign Mode                 | Scrolling text, fading backgrounds, moving sprites, and an advance feature to fast forward animations. An immersive experience to guide the player through the history of music and leads them straight into the games. | ✅        |
| 4    | Pause and volume control      | Using `P` to pause and the `up` and `down` arrow keys during a game. | ✅        |
| 5    | Highscore and Achievments log | For every unique user.                                       | ✅        |
| 6    | Text Input                    | For new users to key in their name.<br />(restricted to lowercase letters, numbers and whitespace)<br />(The numpad cannot be used to input numbers currently) | ✅        |
| 7    | User Profiles                 | Create new user profiles and toggle between them swiftly.    | ✅        |
| 8    | **Sandbox Mode**              | A highly customisable sandbox mode for users to upload their own midi files, with a directory explorer implemented natively in Pygame to preserve theming, avoid extra dependencies or even potential clashes between Pygame and GUI frameworks (e.g. on MacOS launching Tkinter's file dialog prompt with an active Pygame window causes a crash) | ✅        |
| 9    | Sandbox Options               | Various options in the sandbox configuration mode for users to select the level of note quantization, volume, tempo, or even instrument tracks using *pretty-midi*, *midi2audio* and *FluidSynth* as a backend | ✅        |
| 10   | (Windows) Fluidsynth          | A included FluidSynth distribution for Windows users in the source code as it is difficult to install it. | ✅        |
| 11   | Arcade Mode                   | Robust system that lists all available songs (including sandbox) and provides song information and current highscore of the user. | ✅        |
| 12   | Options                       | An options menu allowing users to change FPS, toggle fullscreen mode, change default game volume (values above 100 are allowed) and background volume, and even number of lanes. The change applies immediately in the current game session without the need to restart.<br />*Unfortunately, we removed the option to change screen resolution as a design choice* | ✅        |
| 13   | Key Bindings                  | Any key from a-z for different lanes in the game mode.  Between 1 to 6 lanes are allowed and when fewer than 6 lanes are chosen, only the first few key bindings are active. Binding the same key to multiple lanes is allowed (at your own loss of points when playing). | ✅        |

## pretty_midi switch



## Compatibility Issues

Due to [pygame](https://www.pygame.org/news) being a less popular open source library than other game engines such as Unity, the library has not been keeping up on time with Python upgrades and OS upgrades over time. The last stable release was on 25 April 2019 and this version has various compability problems that affects our development.

### Phantom Orbs

For reasons unknown, among songs of longer durations (which would normally imply a greater number of orbs), the visuals of the orbs would break down - orbs that aren't meant to appear would appear on top of other orbs. **Fortunately, this does not happen when pygame 2.0.0.dev10 is being used.** **The stable release is essential when one wishes to deploy the scripts as executables for various OSes. The following issues are only pertinent to users who are running the executable version.**

### Audio Issues with certain Windows devices

On orbitee mingyi456's computer,

