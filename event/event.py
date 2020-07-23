ID_ANY = -1


class Event:
    def __init__(self, id, type, values=()):
        self._type = type
        self._id = id
        self._values = values

    def __str__(self):
        return f"Event {self.type()} From Source {self.id()} " \
            f"With Value {self.values()}"

    def id(self):
        return self._id

    def type(self):
        return self._type

    def values(self):
        return self._values

    def __eq__(self, obj):
        if not isinstance(obj, Event):
            return NotImplemented
        return (obj.id() == self.id() \
            or obj.id() == ID_ANY or self.id() == ID_ANY) \
            and obj.type() == self.type() \
            and obj.values() == self.values()


CLOSE = Event(ID_ANY, "ACTION", "CLOSE")
