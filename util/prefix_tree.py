class BoundPrefixTree:
    def __init__(self, max_length):
        self._max_length = max_length
        self._root = BoundPrefixTreeNode(0, max_length)
        self._num_items = 0

    def __str__(self):
        nodes = [self._root]
        lines = []
        while nodes:
            node = nodes.pop()
            for child in list(node._ch_map.values())[::-1]:
                nodes.append(child)
            if node.is_valid():
                lines.append(f"(\"{node}\", {node._index})")
        return '\n'.join(lines)

    @staticmethod
    def create(max_length, items):
        tree = BoundPrefixTree(max_length)
        for item in items:
            tree.add(item)
        return tree

    def add(self, string):
        self._root.add_string(string, self._num_items)
        self._num_items += 1

    def find(self, string):
        return self._root.find(string.strip())

    def find_next(self, string):
        return self._root.find_next(string.strip())

    def contains(self, string):
        return self._root.contains(string.strip())


class BoundPrefixTreeNode:
    def __init__(self, depth, limit, parent=None, value = ''):
        self._parent = parent
        self._value = value
        self._depth = depth
        self._limit = limit

        self._index = -1
        self._ch_map = {}

    def is_valid(self):
        return self._index >= 0

    def contains(self, string):
        if string == '':
            return True

        ch, rest = string[0], string[1:]
        if ch not in self._ch_map:
            return False
        else:
            return self._ch_map[ch].contains(rest)

    def find(self, string):
        if string == '':
            return self._index

        ch, rest = string[0], string[1:]
        if ch not in self._ch_map:
            return -1
        else:
            return self._ch_map[ch].find(rest)

    def find_after(self):
        keys = sorted(self._ch_map.keys())
        for key in keys:
            node = self._ch_map[key]
            if node.is_valid():
                return str(node)

            result = node.find_after()
            if result is not None:
                return result
        return None

    # Find first string with matching prefix
    def find_next(self, string):
        # Found node matching prefix
        if string == '':
            if self.is_valid():
                return str(self)
            else:
                return self.find_after()

        # Iterate through prefix string
        ch, rest = string[0], string[1:]
        if ch not in self._ch_map:
            return None
        else:
            return self._ch_map[ch].find_next(rest)

    def add_string(self, string, index):
        if string == '':
            self._index = index
            return
        if self._depth == self._limit:
            raise Exception("STRING IS TOO LONG")

        ch, rest = string[0], string[1:]
        if ch not in self._ch_map:
            self._ch_map[ch] = BoundPrefixTreeNode(self._depth+1,
                    self._limit, self, self._value+ch)
        self._ch_map[ch].add_string(rest, index)

    def __str__(self):
        return self._value.center(self._limit)

    def __repr__(self):
        return ('BPTN({}, {})'.format(self._value, self._index))


if __name__ == "__main__":
    test = ['c', 'c#', 'd', 'eb', 'e', 'f', 'f#', 'g', 'g#', 'a', 'bb',
            'b']
    tree = BoundPrefixTree.create(3, test)
    tree.print_elements()

