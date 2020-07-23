import wx

from data.core import Song
from .core.controller import GfxController
from .core.view import GfxView
from .widget.main import MainView

class GfxProgram:
    def __init__(self):
        self._app = wx.App()

        self._frame = MainView(None)
        self._frame.Show()

        view = GfxView(self._frame)
        controller = GfxController(view)

    def _retrieve_data(self):
        return self._prg.get_data()

    def start(self):
        self._app.MainLoop()

    def stop(self):
        self._frame.Destroy()
