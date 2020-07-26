from pretty_midi import PrettyMIDI
import pretty_midi, csv, itertools, time
from sys import platform as SYS_PLATFORM

if SYS_PLATFORM == "win32":
	from os import environ
	environ["PATH"] += ".\\FluidSynth_Windows"

from midi2audio import FluidSynth
from os import path
fs = FluidSynth('soundfont.sf3')

midi_path = 'master tracks\\Pavane.midi'  # path is inputted

def midiState(midi_path):
	mid = PrettyMIDI(midi_path)
	mid.remove_invalid_notes()
	average_tempo = mid.estimate_tempo()
	pass
	


def midiFunnel(midi_path, quantize=True, onekey=True, changeTempo=True, changeVolume=True):
	directory, name = path.split(midi_path)
	name = name.rsplit('.', 1)[0]
	new_midi_path = 'tracks/' + name + '.mid'
	
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
			print('QUANTIZE COMPLETE')
			break
		subdivision = int(input('Please enter number above 1.\n'
		                        'Recommended 4, 8, 16, 32 for straight tempo \n'
		                        '12 for triple meter: '))
	#########################################################################
	if changeVolume:
		for instrument in mid.instruments:
			volume_messages = [msg.value for msg in instrument.control_changes if msg.number == 7]
			print(f'Max Min Volume: {max(volume_messages), min(volume_messages)}', \
			      f'Room to full volume = {127 - max(volume_messages)}', \
			      pretty_midi.program_to_instrument_name(instrument.program))
		volume_change = int(input('Positive number to increase volume, negative to decrease volume: '))
		for instrument in mid.instruments:
			for msg in instrument.control_changes:
				if msg.number == 7 and msg.value > 0:
					msg.value = max(min(127, msg.value + volume_change), 0)
		print('====== UPDATED VOLUME SETTINGS ======')
		for instrument in mid.instruments:
			volume_messages = [msg.value for msg in instrument.control_changes if msg.number == 7]
			print(f'Max Min Volume: {max(volume_messages), min(volume_messages)}', \
			      f'Room to full volume = {127 - max(volume_messages)}', \
			      pretty_midi.program_to_instrument_name(instrument.program))
	#########################################################################
	if changeTempo:
		time_multiple = float(input('Multiple to slow down or speed up music\n'
		                          'Enter number between 0 and 1 to speed up, above 1 to slow down: '))
	while changeTempo:
		if time_multiple > 0:
			for instrument in mid.instruments:
				for note in instrument.notes:
					note.start *= time_multiple
					note.end *= time_multiple
			if time_multiple < 1:
				print(f'Music sped up by {1/time_multiple} times')
			elif time_multiple > 1:
				print(f'Music slowed down by {time_multiple} times')
			break
		time_multiple = float(input('Multiple to slow down or speed up music\n'
		                            'Enter number between 0 and 1 to speed up, above 1 to slow down: '))
	#########################################################################
	mid.write(new_midi_path)
	mid = PrettyMIDI(new_midi_path)
	
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
		print(number, pretty_midi.program_to_instrument_name(instrument.program), instrument.name)
		selected_tracks += (number,)
	
	entry1 = input('Which instrument would you like? ')
	entry1 = set(int(x) for x in entry1.split(','))
	while True:
		if entry1.issubset(set(range(totalInstruments))):
			selected_tracks = entry1
			break
		entry1 = input(f'Please enter number between 0 and {totalInstruments - 1}: ')
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
	
	csv_rows = [[x.end, x.start, x.get_duration(), x.pitch, x.get_duration() > crotchet] for x in melody]
	totalNotes = len(csv_rows)
	sustainedNotes = 0
	totalSustainDuration = 0
	for row in csv_rows:
		if row[4]:
			sustainedNotes += 1
			totalSustainDuration += row[2]
	
	info_header = ['totalNotes', 'sustainedNotes', 'totalSustainDuration', \
	               'songLength', 'selected_instruments', 'initial_instruments', 'average_tempo', 'unit_time',
	               'crotchet']
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
	print('STARTING FLAC GENERATION, PLEASE WAIT...')
	fs.midi_to_audio(new_midi_path, audio_path)


midiFunnel(midi_path, False, False, False, False)

