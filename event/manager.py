from typing import List

from event.event import Event
from event.handler import EventHandler


class EventManager:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance._handlers: List[EventHandler] = []
        return cls.__instance

    def delegate(self, event:Event):
        for handler in self._handlers:
            handler.handle_event(event)

    def attach(self, handler:EventHandler):
        if not isinstance(handler, EventHandler):
            raise ValueError("Can only attach EventHandler's")
        if handler in self._handlers:
            raise ValueError("Handler already attached")
        self._handlers.append(handler)
