import wx

from data.view.slice import SliceText
from event.event import Event
from event.source import EventSource


class SliceView(wx.Panel, EventSource):
    def __init__(self, parent, font, *args, model=None,
            style=wx.WANTS_CHARS, **kwargs):
        style |= wx.WANTS_CHARS
        wx.Panel.__init__(self, parent, *args, style=style, **kwargs)
        EventSource.__init__(self)

        self._font = font
        self._model = model if model is not None else SliceText()
        self.Bind(wx.EVT_PAINT, self.paint)

        # Set panel size
        self._text_width, self._text_height = self._model.get_size()
        dc = wx.ClientDC(self)
        dc.SetFont(self._font)
        fm = dc.GetFontMetrics()
        self._font_width = fm.averageWidth
        self._font_height = fm.height
        self._client_width = self._text_width * self._font_width
        self._client_height = self._text_height * self._font_height
        self.SetInitialSize((self._client_width, self._client_height))
        self.GetParent().GetParent().Layout()

        # Add event handling
        self.Bind(wx.EVT_CHAR, self._catch_char)
        self.Bind(wx.EVT_LEFT_DOWN, self._catch_click)

    def _catch_char(self, event):
        uni_key = event.GetUnicodeKey()
        key_code = event.GetKeyCode()

        # Determine event to send
        key_value = None
        if key_code == wx.WXK_SPACE:
            key_value = "SPACE"
        elif key_code == wx.WXK_RETURN:
            key_value = "RETURN"
        elif key_code == wx.WXK_TAB:
            key_value = "TAB"
        elif key_code == wx.WXK_UP:
            key_value = "UP"
        elif key_code == wx.WXK_LEFT:
            key_value = "LEFT"
        elif key_code == wx.WXK_DOWN:
            key_value = "DOWN"
        elif key_code == wx.WXK_RIGHT:
            key_value = "RIGHT"
        elif key_code == wx.WXK_ESCAPE:
            key_value = "ESCAPE"
        elif uni_key != wx.WXK_NONE:
            ch = chr(uni_key)
            if (event.GetModifiers() == wx.MOD_NONE \
                    or event.GetModifiers() == wx.MOD_SHIFT) \
                    and not ch.isspace() and ch.isprintable():
                key_value = chr(uni_key)

        # Send event
        if key_value is not None:
            self.emit("KEY", (key_value,))

        event.Skip()

    def _catch_click(self, event):
        # Process event
        dc = wx.ClientDC(self)
        pos = event.GetLogicalPosition(dc)

        x = pos[0] // self._font_width
        y = pos[1] // self._font_height

        # Send event
        self.emit("CLICK", (x, y))

        event.Skip()

    def model(self):
        return self._model

    def paint(self, event):
        dc = wx.PaintDC(self)
        dc.SetFont(self._font)

        dc.SetPen(wx.Pen('#000000', 1, wx.TRANSPARENT))
        dc.SetBrush(wx.Brush('#888888'))
        dc.DrawRectangle(0, 0, self._client_width, self._client_height)

        for r in range(self._text_height):
            for c in range(self._text_width):
                ch, hl = self._model.get_cell(c, r)
                if hl:
                    dc.SetTextForeground('#0000FF')
                else:
                    dc.SetTextForeground('#000000')
                dc.DrawText(ch, c*self._font_width, r*self._font_height)
