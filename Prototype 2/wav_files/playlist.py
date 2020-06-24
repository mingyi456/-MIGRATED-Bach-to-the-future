import vlc, time

player1 = vlc.MediaPlayer('Pavane.wav')
player2 = vlc.MediaPlayer('Blue Danube Waltz.wav')
player3 = vlc.MediaPlayer('Piano Concerto, Adagio Sostenuto.wav')

player3.play()
time.sleep(1)
while player3.is_playing():
	time.sleep(1)