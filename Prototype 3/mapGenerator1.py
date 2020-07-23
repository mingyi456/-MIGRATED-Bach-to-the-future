from pretty_midi import PrettyMIDI
import pretty_midi, csv, itertools, time
from midi2audio import FluidSynth

fs = FluidSynth('soundfont.sf3')

midi_path = 'master tracks/Pavane.midi'

def midiFunnel(midi_path, quantize=False, slowDown=False, onekey=False):
	directory, name = midi_path.rsplit('/', 1)
	name = name.rsplit('.', 1)[0]
	
	mid = PrettyMIDI(midi_path)
	mid.remove_invalid_notes()
	average_tempo = mid.estimate_tempo()
	crotchet = 60 / average_tempo
	unit_time = 'NOT QUANTIZED'
	########################################################################
	if quantize:
		print(mid.time_signature_changes)
		print(average_tempo)
		subdivision = int(input('Note to quantize to: '))
	while quantize:
		if subdivision > 1:
			average_tempo = int(round(mid.estimate_tempo(), 3))
			crotchet = 60 / average_tempo
			unit_time = 60 / (average_tempo * subdivision)
			for instrument in mid.instruments:
				for note in instrument.notes:
					note.start = note.start // unit_time * unit_time
					duration = note.get_duration() // unit_time * unit_time
					note.end = note.start + duration
					note.velocity += 10
			
			new_midi_path = 'tracks/' + name + '.mid'
			mid.write(new_midi_path)
			mid = PrettyMIDI(new_midi_path)
			break
		subdivision = int(input('Please enter number above 1.\n'
		                        'Recommended 4, 8, 16, 32 for straight tempo \n'
		                        '12 for triple meter: '))
	#########################################################################
	
	songLength = time.strftime("%M:%S", time.gmtime(mid.get_end_time()))
	
	totalInstruments = len(mid.instruments)
	initial_instruments = mid.instruments[0].name
	for i in range(1, totalInstruments):
		if i == totalInstruments - 1:
			initial_instruments += ' and ' + mid.instruments[i].name
		else:
			initial_instruments += ', ' + mid.instruments[i].name

	selected_tracks = ()
	for number, instrument in enumerate(mid.instruments):
		print(number, instrument)
		selected_tracks += (number,)
	
	entry1 = input('Which instrument would you like? ')
	entry1 = set(int(x) for x in entry1.split(','))
	while True:
		if entry1.issubset(set(range(totalInstruments))):
			selected_tracks = entry1
			break
		entry1 = input(f'Please enter number between 0 and {totalInstruments-1}: ')
		entry1 = set(int(x) for x in entry1.split(','))
	
	for number, instrument in enumerate(mid.instruments.copy()):
		if number not in selected_tracks:
			mid.instruments.remove(instrument)
	remainingInstruments = len(mid.instruments)
	selected_instruments = mid.instruments[0].name
	for i in range(1, remainingInstruments):
		if i == remainingInstruments - 1:
			selected_instruments += ' and ' + mid.instruments[i].name
		else:
			selected_instruments += ', ' + mid.instruments[i].name
	
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
	totalNotes = len(csv_rows)
	sustainedNotes = 0
	totalSustainDuration = 0
	for row in csv_rows:
		if row[4]:
			sustainedNotes += 1
			totalSustainDuration += row[2]

	info_header = ['totalNotes', 'sustainedNotes', 'totalSustainDuration', \
	        'songLength', 'selected_instruments', 'initial_instruments', 'average_tempo', 'unit_time', 'crotchet']
	info = [totalNotes, sustainedNotes, totalSustainDuration, \
	        songLength, selected_instruments, initial_instruments, average_tempo, unit_time, crotchet]
	
	csv_path = 'beatmaps/' + name + '.csv'
	with open(csv_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(info_header)
		writer.writerow(info)
		writer.writerow(['End Time', 'Start Time', 'Duration', 'Pitch', 'Sustained'])
		writer.writerows(csv_rows)
	print('CSV COMPLETE!')
	
	audio_path = 'wav_files/' + name + '.flac'
	print('STARTING WAV GENERATION, PLEASE WAIT...')
	fs.midi_to_audio(midi_path, audio_path)

midiFunnel(midi_path, True)