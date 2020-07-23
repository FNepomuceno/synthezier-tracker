from data.parse.slice import default_slice, import_slice
from data.core.note import data_to_note


class Slice:
    def divisions(self):
        return self._data["divisions"]

    def edit(self, data):
        data["notes"] = [data_to_note(item) for item in data["notes"]]
        self._replace_data(data)

    def _replace_data(self, data):
        # TODO: log changes?
        self._data = data

    def notes(self):
        return self._data["notes"]

    def load(self, section, voice, data=None):
        if data:
            self._data = import_slice(data)
        else:
            self._data = default_slice()
        self._data["section"] = section
        self._data["voice"] = voice
        return self

    def section(self):
        return self._data["section"]

    def speed(self):
        return self._data["speed"]

    def voice(self):
        return self._data["voice"]
