import vlc, time

player1 = vlc.MediaPlayer('/Users/chence08/PycharmProjects/Bach-to-the-future/Prototype 2/wav_files/Pavane.wav')
player2 = vlc.MediaPlayer('/Users/chence08/PycharmProjects/Bach-to-the-future/Prototype 2/wav_files/Blue Danube Waltz.wav')
player3 = vlc.MediaPlayer('/Users/chence08/PycharmProjects/Bach-to-the-future/Prototype 2/wav_files/Piano Concerto, Adagio Sostenuto.wav')

player3.play()
time.sleep(1)
while player3.is_playing():
	time.sleep(1)