from event.event import Event
from event.manager import EventManager

class SourceId:
    __prev_id = -1

    def __init__(self):
        raise NotImplementedError("Cannot Create Object")

    @classmethod
    def next(cls):
        cls.__prev_id += 1
        return cls.__prev_id

class EventSource:
    def __init__(self):
        if self.__class__ == EventSource:
            raise NotImplementedError("Derived Classes Only")
        self._id = f"{self.__class__.__name__} {SourceId.next()}"

    def source_id(self):
        return self._id

    def get_source_id(self):
        raise Exception("stop using this")
        return self._id

    def emit(self, event_type:str, event_values):
        event = Event(self.source_id(), event_type, event_values)
        EventManager().delegate(event)
