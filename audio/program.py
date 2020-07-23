import pyo

from .core.controller import AudController
from .core.view import AudView
from .core.player import AudPlayer


class AudProgram:
    def __init__(self):
        view = AudView()
        self._player = AudPlayer(view)
        controller = AudController(view, self._player)

    def start(self):
        pass

    def stop(self):
        self._player.stop()
