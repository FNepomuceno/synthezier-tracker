class TextSelector:
    def __init__(self, width, height, columns, rows):
        self._width = width
        self._height = height

        if not columns:
            columns = [1 for _ in range(self._width)]
        elif sum(column for column in columns) != width:
            raise ValueError("Columns do not match width")

        if not rows:
            rows = [1 for _ in range(self._height)]
        elif sum(row for row in rows) != height:
            raise ValueError("Rows do not match height")

        self._columns = columns
        self._rows = rows

        self._selected_position = (-1, -1)
        self._selected_size = (0, 0)

    def is_selected(self, x, y):
        def within_bounds(i, start, size):
            return i >= start and i < start + size
        x_selected = within_bounds(
            x, self._selected_position[0], self._selected_size[0])
        y_selected = within_bounds(
            y, self._selected_position[1], self._selected_size[1])
        return x_selected and y_selected

    def is_valid(self):
        x, y = self._selected_position
        return x >= 0 and x < self._width and y >= 0 and y < self._height

    def select(self, x, y):
        col_start = 0
        col_size = 0
        for column in self._columns:
            if x >= col_start and x < col_start + column:
                col_size = column
                break
            col_start += column

        row_start = 0
        row_size = 0
        for row in self._rows:
            if y >= row_start and y < row_start + row:
                row_size = row
                break
            row_start += row

        if col_start == self._width or row_start == self._height:
            self._selected_position = (-1, -1)
            self._selected_size = (0, 0)
        else:
            self._selected_position = (col_start, row_start)
            self._selected_size = (col_size, row_size)

    def selection(self):
        return (self._selected_position, self._selected_size)


class TextGrid:
    def __init__(self, width, height, columns=None, rows=None, pattern=' '):
        self._width = width
        self._height = height

        self._selector = TextSelector(width, height, columns, rows)

        pat_len = len(pattern)
        num_reps = (width+pat_len-1) // pat_len
        pat_str = pattern * num_reps
        self._data = [
            [pat_str[i] for i in range(width)]
            for _ in range(height)
        ]

    def __str__(self):
        return "Text({})".format(self.selection())
        # "Full Output"
        # lines = []
        # for i in range(self._height):
        #     lines.append(''.join(self._data[i]))
        # return '\n'.join(lines)

    def cell(self, x, y):
        return self._data[y][x], self._selector.is_selected(x, y)

    def edit(self, text):
        (x, y), (w, h) = self._selector.selection()

        if len(text) > w*h:
            raise ValueError("Text is too long")
        elif len(text) < w*h:
            text = text.center(w*h)

        for i in range(w):
            for j in range(h):
                self._data[y+j][x+i] = text[j*w+i]

    def is_selected(self):
        (w, h) = self._selector.selection()[1]
        return w > 0 and h > 0

    def reset_position(self):
        self._selector.select(-1, -1)

    def row(self, y):
        text = []
        for i in range(self._width):
            text.append(self._data[y][i])
        return ''.join(text)

    def select(self, x, y):
        self._selector.select(x, y)

    def selection(self):
        selection = []
        (x, y), (w, h) = self._selector.selection()
        for j in range(h):
            row = []
            for i in range(w):
                row.append(self._data[y+j][x+i])
            selection.append(''.join(row))
        selection = '\n'.join(selection)

        return selection

    def selection_size(self):
        _, (w, h) = self._selector.selection()
        return w * h

    def selection_pos(self):
        (x, y), _ = self._selector.selection()
        return (x, y)

    def size(self):
        return (self._width, self._height)
