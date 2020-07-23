import re

from util.prefix_tree import BoundPrefixTree
from util.select import Selector
from util.text_grid import TextGrid, TextSelector
from data.core import Scale, Song


EMPTY_PITCH = "---"
SILENT_PITCH = "[_]"
EMPTY_EFFECT = "--"
EFFECT_NAMES = [EMPTY_EFFECT]
FIELDS = ["pitch", "octave", "volume", "effect", "value"]
COLUMNS = {
    "pitch": 3,
    "octave": 1,
    "volume": 2,
    "effect": 2,
    "value": 2,
}


class SliceText:
    WIDTH = 10
    TEXT_PATTERN = '---000--00'

    def __init__(self, section_name, voice_name):
        self._section = section_name
        self._voice = voice_name
        self._data = load_slice(section_name, voice_name)
        self._text = TextGrid(SliceText.WIDTH, self._data["length"],
            columns=[COLUMNS[field] for field in FIELDS],
            pattern=SliceText.TEXT_PATTERN)
        self._selection_index = 0

        for row, note in self._data["notes"].items():
            column = 0
            for i, field in enumerate(FIELDS):
                if field in note:
                    entry = note[field]
                else:
                    entry = self._data["selectors"][field].default()
                self._text.select(column, row)
                self._text.edit(entry)
                column += COLUMNS[field]
        self._text.reset_position()

    def __str__(self):
        return str(self._text)

    def _note_data(self):
        result = []

        # Gather Notes
        _, height = self._text.size()
        for i in range(height):
            row_str = self._text.row(i)
            note = {}

            note_name = row_str[0:3].strip()
            if note_name == EMPTY_PITCH:
                continue
            elif note_name == SILENT_PITCH:
                note["pitch"] = SILENT_PITCH
                note["volume"] = "00"
            else:
                note["pitch"] = note_name
                note["octave"] = row_str[3:4]
                note["volume"] = row_str[4:6]
            note["row"] = i
            result.append(note)

        # Convert row into duration
        offset = result[0].pop("row") if result else height
        cur_row = offset

        for i in range(len(result)-1):
            nxt_row = result[i+1].pop("row")
            result[i]["duration"] = nxt_row - cur_row
            cur_row = nxt_row

        if result:
            result[-1]["duration"] = height - cur_row
        if offset:
            result.insert(0, {"duration": offset})

        return result

    def as_data(self):
        result = {}
        result["speed"] = self._data["speed"]
        result["divisions"] = self._data["divisions"]
        result["notes"] = self._note_data()
        result["section"] = self._section
        result["voice"] = self._voice
        return result

    def get_cell(self, x, y):
        return self._text.cell(x, y)

    def get_size(self):
        return self._text.size()

    def input_ch(self, ch):
        if not self._text.is_selected():
            return

        old_selection = self._text.selection() \
            .strip()[:self._selection_index]

        x, _ = self._text.selection_pos()
        selector = self._data["selectors"][x]

        selector.set_selection(old_selection)
        new_selection, _, new_index = selector.match(ch)

        self._text.edit(new_selection)
        self._selection_index = new_index

    def select(self, x, y):
        self._selection_index = 0
        self._text.select(x, y)

        new_x = self._text.selection_pos()[0]
        self._data["selectors"][new_x].reset()

    def unselect(self):
        self._text.select(-1, -1)


def extract_selectors(scale):
    selectors = {}

    # Pitch
    pitch_names = [EMPTY_PITCH, SILENT_PITCH] + scale.pitch_list()
    selectors["pitch"] = Selector(3, values=pitch_names)

    # Octave, Volume, Effects, Effect Values
    selectors["octave"] = Selector(1)
    selectors["volume"] = Selector(2)
    selectors["effect"] = Selector(2, values=EFFECT_NAMES)
    selectors["value"] = Selector(2)

    # Additional mapping by column number
    selectors[0] = selectors["pitch"]
    selectors[3] = selectors["octave"]
    selectors[4] = selectors["volume"]
    selectors[6] = selectors["effect"]
    selectors[8] = selectors["value"]
    
    return selectors


def extract_notes(slice_notes):
    row = 0
    result = {}
    for note in slice_notes:
        note_value = {}
        if note.is_empty():
            row += note.duration()
            continue
        elif note.is_silent():
            note_value["pitch"] = SILENT_PITCH
        else:
            degree = note.degree()
            note_value["pitch"] = Song().scale().pitch_name(degree)
            note_value["octave"] = "{:01x}".format(note.octave())
            note_value["volume"] = "{:02x}".format(note.volume())
        result[row] = note_value
        row += note.duration()

    return result


def load_slice(section_name, voice_name):
    result = {}
    result["selectors"] = extract_selectors(Song().scale())
    section_slice = Song().slice(section_name, voice_name)

    notes = section_slice.notes()
    result["speed"] = section_slice.speed()
    result["divisions"] = section_slice.divisions()
    result["length"] = sum(note.duration() for note in notes)
    result["notes"] = extract_notes(notes)

    return result
