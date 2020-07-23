from .slice import Slice
from data.parse.section import default_sections, import_sections


class Section:
    def slice(self, section_name, voice_name):
        return self._data[section_name][voice_name]

    def load(self, input_path=None):
        if input_path:
            self._data = import_sections(input_path)
        else:
            self._data = default_sections()
        return self
