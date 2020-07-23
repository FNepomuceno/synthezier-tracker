from event.event import Event


class EventHandler:
    def __init__(self):
        from event.manager import EventManager

        if self.__class__ == EventHandler:
            raise NotImplementedError("Derived Classes Only")
        EventManager().attach(self)

    def handle_event(self, event:Event):
        raise NotImplementedError("Derived Classes Only")
