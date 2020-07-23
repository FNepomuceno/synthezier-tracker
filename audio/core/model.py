from data.core import Song
from event import EventHandler, Event

class AudModel(EventHandler):
    def __init__(self):
        self._data = {
            "section": Song().selected_section()
        }

        print(self._data)
