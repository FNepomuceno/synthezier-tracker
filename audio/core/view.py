from audio.instruments.square import SquareWave
from event import Event, EventHandler
from data.core import Song


class AudView(EventHandler):
    def __init__(self):
        EventHandler.__init__(self)
        self._model = Song()
        self.reset()

    def _create(self, section, voice):
        entry = {}

        # Instrument (only one choice here)
        entry["instrument"] = SquareWave

        # Slice (needed for later stuff
        sec_slice = self._model.slice(section, voice)

        # Speed (in bpm)
        entry["speed"] = sec_slice.speed()

        # Notes (for the rest of the stuff needed)
        notes = sec_slice.notes()

        # (midinote, beat, amp) triple for each note
        data = []
        cur_data = [-1, 0, 0]
        for note in notes:
            if note.is_empty():
                cur_data[1] += note.duration()
            elif note.is_silent():
                if cur_data[2] == 0:
                    cur_data[1] += note.duration()
                else:
                    data.append(cur_data)
                    cur_data = [-1, note.duration(), 0]
            else:
                if cur_data[1] > 0:
                    data.append(cur_data)
                degree = note.degree()
                octave = note.octave()
                midinote = Song().scale().pitch_midi(degree, octave)
                cur_data = [midinote, note.duration(),
                        note.volume()/256]
                pass
        if cur_data[1] > 0:
            data.append(cur_data)

        # Convert to midinote, beat, amp lists
        entry["pitch"], entry["duration"], entry["volume"] = zip(*data)

        self._data[section][voice] = entry

    def handle_event(self, event:Event):
        if event.type() == "MODEL_UPDATE":
            self._create(**event.values()[0])

    def reset(self):
        sections = self._model.sections()
        voices = self._model.voices()
        self._data = {}
        for section in sections:
            self._data[section] = {}
            for voice in voices:
                self._create(section=section, voice=voice)

    def slice_data(self, section, voice):
        return self._data[section][voice]
