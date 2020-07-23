from decimal import Decimal
from fractions import Fraction
from math import log2

from data.parse.scale import default_scale, import_scale, midi_scale


class Scale:
    def file_name(self):
        if "file_name" in self._data:
            return self._data["file_name"]
        else:
            return None

    def file_path(self):
        if "file_path" in self._data:
            return self._data["file_path"]
        else:
            return None

    def pitch_midi(self, degree, octave):
        interval = self._data["intervals"][degree]
        if interval[1] == "CENTS":
            midival = float(interval[0]/100)
        elif interval[1] == "PURE":
            midival = log2(interval[0])*12
        else:
            raise ValueError("Invalid interval in scale")
        return 12 + 12*octave + midival

    def pitch_name(self, degree):
        return self._data["pitches"][degree % self._data["size"]]

    def pitch_degree(self, name):
        return self._data["pitches"].index(name)

    def pitch_list(self):
        return self._data["pitches"]

    def is_midi(self):
        return self._data == midi_scale()

    def load(self, input_path=None):
        if input_path:
            self._data = import_scale(input_path)
        else:
            # self._data = default_scale()
            self._data = midi_scale()
        return self
