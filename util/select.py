from util.digit_generator import hex_generator
from util.prefix_tree import BoundPrefixTree


class Selector:
    def __init__(self, length, values=None):
        if values is None:
            values = hex_generator(length)
        self._tree = BoundPrefixTree.create(length, values)
        self._index = 0
        self._length = length
        self._selection = ""
        self._default = self._tree.find_next("")
        self._text = self._default

    def default(self):
        return self._default

    def reset(self):
        self._selection = ""
        self._text = self._default
        self._index = 0

    def set_selection(self, st):
        # Update selection only if string `st` is valid
        if self._tree.find(st) > 0:
            self._selection = st
            self._text = self._tree.find_next(st)
            self._index = len(st) % self._length
        return (self._text, self._selection, self._index)

    def match(self, ch):
        self._selection += ch
        text = self._tree.find_next(self._selection)
        if not text:
            self._selection = ch
            self._index = 0
            text = self._tree.find_next(ch)

        if not text:
            self.reset()
        else:
            self._text = text 
            self._index = (self._index + 1) % self._length

        return (self._text, self._selection, self._index)
