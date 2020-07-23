import pyo

from data.core import Song


class AudPlayer:
    def __init__(self, view):
        self._server = pyo.Server().boot()
        self._data = []
        self._state = "STOP"
        self._model = Song()
        self._view = view

    def _reload(self):
        voices = self._model.voices()
        section = self._model.selected_section()

        self._data = []
        for voice in voices:
            entry = self._view.slice_data(section, voice)
            ev = pyo.Events(instr=entry["instrument"],
                    midinote=entry["pitch"],
                    beat=entry["duration"],
                    bpm=entry["speed"],
                    amp=entry["volume"]).play()
            self._data.append(ev)

    def play_pause(self):
        if self._state == "PLAY":
            self.pause()
        else:
            if self._state != "PAUSE":
                self._reload()
            self.play()

    def play(self):
        self._state = "PLAY"
        self._server.start()

    def pause(self):
        self._state = "PAUSE"
        self._server.stop()

    def stop(self):
        if self._state == "PLAY":
            self._server.stop()
        for voice in self._data:
            voice.stop(0)
        self._state = "STOP"
