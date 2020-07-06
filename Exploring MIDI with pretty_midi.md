# Exploring MIDI with `pretty_midi`

## Information extraction

For our purposes, only useful attributes and methods will be discussed.

```python
import pretty_midi
mid = pretty_midi.PrettyMIDI('Blue Danube Waltz.midi')

for instrument in mid.instruments:
  print(instrument)
for key_signature in mid.key_signature_changes:
  print(key_signature)
for time_signature in mid.time_signature_changes:
  print(time_signature)
```

### Attributes

#### Instruments

List of `pretty_midi.Instrument` objects.

```python
Instrument(program=73, is_drum=False, name="Flute I")
Instrument(program=73, is_drum=False, name="Flute II (Piccolo)")
Instrument(program=68, is_drum=False, name="Oboe 1&2")
Instrument(program=71, is_drum=False, name="Clarinet I in C")
Instrument(program=71, is_drum=False, name="Clarinet II in C")
Instrument(program=70, is_drum=False, name="Bassoons I, II")
Instrument(program=60, is_drum=False, name="Horn I, II in F")
Instrument(program=60, is_drum=False, name="Horn III, IV in F")
Instrument(program=56, is_drum=False, name="Trumpet I in F")
Instrument(program=56, is_drum=False, name="Trumpet II in F")
Instrument(program=57, is_drum=False, name="Bass  Trombone")
Instrument(program=58, is_drum=False, name="Tuba")
Instrument(program=47, is_drum=False, name="Timpani")
Instrument(program=0, is_drum=True, name="Percussion")
Instrument(program=46, is_drum=False, name="Harp")
Instrument(program=48, is_drum=False, name="Violin I")
Instrument(program=48, is_drum=False, name="Violin II")
Instrument(program=45, is_drum=False, name="Violin II")
Instrument(program=48, is_drum=False, name="Violas")
Instrument(program=45, is_drum=False, name="Violas")
Instrument(program=48, is_drum=False, name="Violoncellos")
Instrument(program=45, is_drum=False, name="Violoncellos")
Instrument(program=45, is_drum=False, name="Contrabass")
Instrument(program=48, is_drum=False, name="Contrabass")
```

##### class `pretty_midi.Instrument(program, is_drum=False, name='')`

| Attributes      | Meaning                                                      |
| --------------- | ------------------------------------------------------------ |
| program         | (int) The [program number](https://en.wikipedia.org/wiki/General_MIDI#Program_change_events) of this instrument. `[0, 127]` |
| is_drum         | (bool) Is the instrument a drum instrument?<br />*In GM standard MIDI files, channel 10 **(9)** is reserved for [percussion instruments](https://en.wikipedia.org/wiki/General_MIDI#Percussion) only.* |
| name            | (str) Name of the instrument.                                |
| **notes**       | (list) List of [`pretty_midi.Note`](class pretty_midi.Note(velocity, pitch, start, end)) objects. |
| pitch_bends     | (list) List of `pretty_midi.PitchBend` objects.              |
| control_changes | (list) List of `pretty_midi.ControlChange` objects.          |

| Methods                                                      | Function                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `get_onsets`()                                               | Get all onsets (start_time) of all notes played by this instrument. May contain duplicates (polyphony).<br />**returns** np.ndarray |
| `get_piano_roll`(<br />fs=100,<br />times=None,<br />pedal_threshold=64) | Compute a piano roll matrix of this instrument.<br />fs (int): Sampling frequency of the columns, i.e. each column is spaced apart by `1/fs` seconds.<br />times (np.ndarray): Times of the start of each column in the piano roll.<br />pedal_threshold (int): Value of control change 64 (sustain pedal) message that is less than *this value* is reflected as *pedal_off*. Pedals will be reflected as elongation of notes in the piano roll. If None, then CC64 message is ignored.<br />**returns** np.ndarray, shape=(128, time.shape[0]) |
| `get_chroma`()                                               | Get a sequence of chroma vectors from this instrument.<br />Same format as `get_piano_roll`(). |
| `get_end_time`()                                             | Returns the time of the end of the events in this instrument.<br />**returns** (float) Time, in seconds, of the last event. |
| **`remove_invalid_notes`()**                                 | Removes any notes whose end time is before or at their start_time. |

##### class pretty_midi.Note(velocity, pitch, start, end)

* velocity: (int) Note velocity.
* pitch: (int) Note pitch, as a [MIDI note number](https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies).
* start: (int) Note start time, **absolute**, in seconds.
* end: (int) Note end time, **absolute**, in seoncds.
* `get_duration`(): Get the duration of the note in seconds.

### Key Signatures

List of `pretty_mid.KeySignature` objects.

```python
A Major at 0.00 seconds
```

##### class `pretty_midi.KeySignature(key_number, time)`

| Attributes | Meaning                                                      |
| ---------- | ------------------------------------------------------------ |
| key_number | (int) Key number according to `[0, 11]` Major, `[12, 23]` minor. (12-tone)<br />For example, 0 is C Major, 12 is C minor. |
| time       | (float) Time of event in seconds.                            |

### Time Signatures

List of `pretty_mid.TimeSignature` objects.

```python
6/8 at 0.00 seconds
3/4 at 70.71 seconds
7/8 at 91.71 seconds
3/4 at 92.88 seconds
2/4 at 168.73 seconds
3/4 at 169.43 seconds
1/4 at 169.43 seconds
3/4 at 169.82 seconds
2/4 at 201.82 seconds
3/4 at 202.48 seconds
1/4 at 218.48 seconds
3/4 at 218.82 seconds
2/4 at 438.63 seconds
3/4 at 439.30 seconds
4/4 at 441.32 seconds
3/4 at 442.67 seconds
15/8 at 448.74 seconds
1/4 at 451.27 seconds
3/4 at 451.64 seconds
9/8 at 631.33 seconds
```

##### class `pretty_midi.TimeSignature(numerator: int, denominator: int, time: float)`

### Methods

##### class `pretty_midi.PrettyMIDI(midi_file=None, resolution=220, initial_tempo=120.0)

| Methods                                                      | Function                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `get_tempo_changes`()                                        | Returns arrays of tempo changes in **quarter-notes-per-minute** and their times.<br />**returns **`tuple`(tempo_change_times: np.ndarray, tempi: np.ndarray) |
| `get_end_time`()                                             | Returns the time of the end of the MIDI object (time of the last event in all instruments/meta-events). |
| `estimate_tempi`()                                           | Return an empirical estimate of tempos and each tempo's probability in a `tuple` of np.ndarray pair. |
| `estimate_tempo`()                                           | (float) Returns the best tempo estimate from `estimate_tempi`(). |
| `get_beats`(<br />start_time=0.0)                            | Returns a *list* of beat locations, according to MIDI *tempo changes*. For *compound meters* (any whose numerator is a multiple of 3 greater than 3), this method returns every third denominator note (for 6/8 or 6/16 time, for example, it wil return **every third 8th note or 16th note**, respectively). For all other meters, this method returns **every denominator note** (every quarter note for 3/4 or 4/4 time, for example).<br />**returns** (np.ndarray) Beat locations, in seconds |
| `get_downbeats`(<br />start_time=0.0)                        | Return a list of downbeat locations, according to MIDI *tempo changes* and *time signature change* events. |
| `get_onsets`()                                               | Return a sorted list of the times of all onsets (start_time) of all notes from all instruments. May have duplicate entries.<br />**returns** (np.ndarray) Onset locations, in seconds |
| `synthesize`(<br />fs=44100,<br />wave=<ufunc 'sin'>)        | Synthesize the pattern using some waveshape. Ignores drum track.<br />fs (int): Sampling rate of the synthesized audio signal<br />wave (function): Function which returns a periodic waveform, e.g. `np.sin`, `script.signal.square`, etc.<br />**returns** (np.ndarray) Waveform of the MIDI data, synthesized at `fs`. |
| `fluidsynth`(<br />fs=44100,<br />sf2_path=None)             | Synthesize using fluid synth.<br />fs (int): Sampling rate of the synthesized audio signal<br />sf2_path (str): Path to a .sf2 file. Default `None`, which uses the TimBM6mb.sf2 file included with `pretty_midi`. |
| `tick_to_time`(tick: int)                                    | (float) Converts from an absolute tick to time in seconds using `self.__tick_to_time`. |
| `time_to_tick`(time: float)                                  | (int) Converts from a time in seconds to absolute tick using `self._tick_scales`. |
| `adjust_times`(<br />original_times: np.ndarray<br />, new_times: np.ndarray) | Adjusts the timing of the events in the MIDI object. The parameters `original_times` and `new_times` define a mapping, so that if an event orignally occurs at time `original_times[n]`, it will be moved so that it occurs at `new_times[n]`. If events don't occur exactly on a time in `original_times`, their timing will be linearly interpolated. |
| `remove_invalid_notes`()                                     | Removes any notes whose end time is before of at their start_time |
| write(filename)                                              | Write the MIDI data out to a .mid file.<br />filename (str or file): Path or file to write .mid file to. |

## Utility functions

| Function                                                     | Remarks                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `key_number_to_key_name`(key_number)                         | Convert a key number to a key string.                        |
| `key_name_to_key_number`(key_string)                         | Convert a key name string to key number.<br />key_string **format** is `'(root) (mode)'`, where:<br />- `(root)` is one of ABCDEFG or abcdefg. A lowercase root indicates a minor key when no mode string is specified. Optionally a # for sharp or b for flat can be specified.<br />- `(mode)` is optionally specified either as one of ‘M’, ‘Maj’, ‘Major’, ‘maj’, or ‘major’ for major or ‘m’, ‘Min’, ‘Minor’, ‘min’, ‘minor’ for minor. If no mode is specified and the root is uppercase, the mode is assumed to be major; if the root is lowercase, the mode is assumed to be minor. |
| `mode_accidentals_to_key_number`(mode, num_accidentals)      | Convert a given number of accidentals and mode to a key number.<br />mode (int): 0 is major, 1 is minor.<br />num_accidentals (int): Positive number is used for sharps, negative number is used for flats. |
| `key_number_to_mode_accidentals`(key_number)                 | Convert a key number to `tuple`(mode, number of accidentals.) |
| `qpm_to_bpm`(quarter_note_tempo: float, numerator: int, denominator: int) | (float) Converts from quarter notes per minute to beats per minute. |
| `note_number_to_hz`(note_number: float)                      | (float) Convert a (fractional) MIDI note number to its frequency in Hz. |
| `hz_to_note_number`(frequency: float)                        | (float) Convert a frequency in Hz to a (fractional) note number. |
| `note_name_to_number`(note_name: str)                        | Converts a note name in the format `'(note)(accidental)(octave number)'` (e.g. `'C#4'`) to MIDI note number.<br />`'(note)'` is required, and is case-insensitive.<br />`'(accidental)'` should be `''` for natural, `'#'` for sharp and `'!'` or `'b'` for flat.<br />If `'(octave)'` is `''`, octave 0 is assumed. |
| `note_number_to_name`(note_number: int)                      | Convert a MIDI note number to its name, in the format `'(note)(accidental)(octave number)'` (e.g. `'C#4'`). |
| `note_number_to_drum_name`(note_number: int)                 | Converts a MIDI note number in a percussion instrument to the corresponding drum name, according to the General MIDI standard.<br />Any MIDI note number outside of the valid range (note 35-81, zero-indexed) will result in an empty string. |
| `drum_name_to_note_number`(drum_name)                        | Converts a drum name to the corresponding MIDI note number for a percussion instrument. Conversion is case, whitespace, and non-alphanumeric character insensitive. |
| `program_to_instrument_name`(program_number)                 | Converts a MIDI program number to the corresponding General MIDI instrument name. |
| `instrument_name_to_program`(instrument_name)                | Converts an instrument name to the corresponding General MIDI program number. Conversion is case, whitespace, and non-alphanumeric character insensitive. |
| `program_to_instrument_class`(program_number)                | Converts a MIDI program number to the corresponding General MIDI instrument class. |
| `pitch_bend_to_semitones`(pitch_bend, semitone_range=2.0)    | Convert a MIDI pitch bend value (in the range `[-8192, 8191]`) to the bend amount in semitones. |
| `semitones_to_pitch_bend`(semitones, semitone_range=2.0)     | Convert a semitone value to the corresponding MIDI pitch bend integer. |

