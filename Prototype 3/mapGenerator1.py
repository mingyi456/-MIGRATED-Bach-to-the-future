from pretty_midi import PrettyMIDI
import pretty_midi, csv, itertools
from midi2audio import FluidSynth

fs = FluidSynth('/Users/chence08/PycharmProjects/Bach-to-the-future/Prototype 3/TimGM6mb.sf2')

midi_path = '../Prototype 3/tracks/Pavane.midi'

def midiFunnel(midi_path, quantize=0, onekey=False):
	directory, name = midi_path.rsplit('/', 1)
	name = name.rsplit('.', 1)[0]
	directory = directory.rsplit('/', 1)[0]
	print(directory, name)
	
	mid = PrettyMIDI(midi_path)
	mid.remove_invalid_notes()
	average_tempo = mid.estimate_tempo()
	crotchet = 60 / average_tempo
	unit_time = 'NOT QUANTIZED'
	########################################################################
	if quantize:
		average_tempo = int(round(mid.estimate_tempo(), 3))
		crotchet = 60 / average_tempo
		unit_time = 60 / (average_tempo * quantize)
		for instrument in mid.instruments:
			for note in instrument.notes:
				note.start = note.start // unit_time * unit_time
				duration = note.get_duration() // unit_time * unit_time
				note.end = note.start + duration
	mid.write(midi_path)
	mid = PrettyMIDI(midi_path)
	#########################################################################
	
	selected_tracks = ()
	for number, instrument in enumerate(mid.instruments):
		print(number, instrument)
		selected_tracks += (number,)
	
	entry1 = input('Which instrument would you like? ')
	if entry1:
		selected_tracks = tuple(int(x) for x in entry1.split(','))
	
	for number, instrument in enumerate(mid.instruments.copy()):
		if number not in selected_tracks:
			mid.instruments.remove(instrument)
	instrument_info = mid.instruments
	
	notes = [x.notes for x in mid.instruments]
	flatten = list(itertools.chain(*notes))
		
	melody = {}
	for note in flatten:
		if note.start not in melody:
			melody[note.start] = note
		elif note.pitch > melody[note.start].pitch:
			melody[note.start] = note
	melody = list(melody.values())
	print(f'\nNo chords: {len(melody)}\nWith chords: {len(flatten)}')
	
	if onekey:
		cut_off = 0  # end time of previous note
		for note in melody.copy():
			if note.start < cut_off:
				melody.remove(note)
			else:
				cut_off = note.end
		print(f'Onekey: {len(melody)}')
	
	csv_rows = [[x.end, x.start, x.get_duration(), x.pitch, x.get_duration()>crotchet] for x in melody]
		
	
	csv_path = directory + '/beatmaps/' + name + '.csv'
	with open(csv_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(['End Time', 'Start Time', 'Duration', 'Pitch', 'Sustained', \
		                 f'{instrument_info}, Average Tempo={average_tempo}, Unit Time={unit_time}, Crotchet={crotchet}'])
		writer.writerows(csv_rows)
	print('CSV COMPLETE!')
	
	# audio_path = directory + '/wav_files/' + name + '.wav'
	# print('STARTING WAV GENERATION, PLEASE WAIT...')
	# fs.midi_to_audio(midi_path, audio_path)

midiFunnel(midi_path, 8)
