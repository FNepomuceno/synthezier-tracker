from data.parse.note import import_note


class Note:
    def __str__(self):
        if self.is_empty():
            return f"Note(EMPTY, {self.duration()})"
        elif self.is_silent():
            return f"Note(SILENT, {self.duration()})"
        else:
            return f"Note({self.degree()}, {self.octave()}, " \
                f"{self.volume()}, {self.duration()})"

    def __repr__(self):
        return str(self)

    def degree(self):
        if "degree" not in self._data:
            raise Exception("Note is blank or silent")
        return self._data["degree"]

    def duration(self):
        return self._data["duration"]

    def is_empty(self):
        return "degree" not in self._data and "volume" not in self._data

    def is_silent(self):
        return ("degree" not in self._data and "volume" in self._data) \
            or "volume" in self._data and self._data["volume"] == 0

    def octave(self):
        if "octave" not in self._data:
            raise Exception("Note is blank or silent")
        return self._data["octave"]

    def volume(self):
        if "volume" not in self._data:
            raise Exception("Note is blank")
        return self._data["volume"]

    def load(self, data):
        self._data = import_note(data)
        return self


def data_to_note(data):
    if "degree" not in data and "volume" not in data:
        return empty_note(data["duration"])
    elif "degree" not in data and "volume" in data:
        return silent_note(data["duration"])
    else:
        result = {}
        result["tick"] = data["duration"]
        result["volm"] = int(data["volume"], 16)
        result["octave"] = int(data["octave"], 16)
        result["degree"] = data["degree"]
        return Note().load(result)


# note that silences the previous note
def silent_note(duration=1):
    result = {}

    result["volm"] = 0
    result["tick"] = duration

    return Note().load(result)


# placeholder note
def empty_note(duration=1):
    result = {}

    result["tick"] = duration

    return Note().load(result)
