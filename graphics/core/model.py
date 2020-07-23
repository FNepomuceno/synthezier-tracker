from event import EventHandler, Event

class GfxModel(EventHandler):
    def __init__(self):
        pass

    def handle_event(self, event:Event):
        if event.get_type == "NEW":
            pass
        elif event.get_type == "OPEN":
            pass
