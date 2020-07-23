from os.path import split

from data.parse.song import default_song, import_song, export_song
from event import Event, EventHandler, EventSource


class Song(EventHandler, EventSource):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            self = cls.__instance

            EventHandler.__init__(self)
            EventSource.__init__(self)
            
            self.reset_to_new()
        return cls.__instance

    def __init__(self):
        return # Prevent duplicate inits

    def change_file(self, new_path):
        pass

    def edit(self, sec_data):
        # Convert pitch names into scale degrees
        scale = self.scale()
        for note in sec_data["notes"]:
            if "pitch" in note:
                pitch = note.pop("pitch")
                if pitch != "[_]":
                    note["degree"] = scale.pitch_degree(pitch)

        # Find section slice and give it the new data
        section_name = sec_data["section"]
        voice_name = sec_data["voice"]
        sec_slice = self.slice(section_name, voice_name)
        sec_slice.edit(sec_data)

        sec_id = {
            "section": section_name,
            "voice": voice_name
        }

        self.emit("MODEL_UPDATE", (sec_id,))

    def export(self, file_path):
        try:
            with open(file_path, "w") as file:
                export_song(stream=file)
        except Exception as e:
            print(e)
        else:
            self._data["file_path"], self._data["file_name"] = \
                    split(file_path)

    def file_name(self):
        return self._data["file_name"]

    def file_path(self):
        return self._data["file_path"]

    def handle_event(self, event: Event):
        if event.type() == "REQUEST_LOAD":
            self.reset_to_load(event.values()[0])
        elif event.type() == "REQUEST_NEW":
            self.reset_to_new()
        elif event.type() == "REQUEST_SAVE":
            self.export(event.values()[0])

    def load(self, input_path=None):
        if input_path:
            self._data = import_song(input_path)
        else:
            self._data = default_song()
        return self

    def reset_to_load(self, input_path):
        self.load(input_path)
        self.emit("DATA_UPDATE", ())

    def reset_to_new(self):
        self.load()
        self.emit("DATA_UPDATE", ())

    def scale(self):
        return self._data["scale"]

    def sections(self):
        return self._data["section_names"]

    def selected_section(self):
        return self._data["section_names"][self._data["sequence_index"]]

    def sequence(self):
        return self._data["sequence"]

    def slice(self, section, voice):
        return self._data["sections"].slice(section, voice)

    def voices(self):
        return self._data["voice_names"]
