from event.handler import EventHandler


class EventPrinter(EventHandler):
    def __init__(self):
        pass

    def handle_event(self, event):
        print(event)
