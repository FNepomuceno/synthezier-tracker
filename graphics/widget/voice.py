import wx

from data.core.song import Song
from event import EventSource


class VoiceView(wx.Frame, EventSource):
    def __init__(self, parent, *args, font_size=12, **kwargs):
        wx.Frame.__init__(self, parent, *args, title="Manage Voices",
            size=(350, 300), **kwargs)
        EventSource.__init__(self)

        self._font_size = font_size
        self._font = wx.Font(self._font_size, wx.FONTFAMILY_TELETYPE,
                wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        self._data = Song()
        self._font_size = font_size

        # Setup
        self._sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self._sizer)

        # Voice List
        sample_list = ['abra', 'kadabra', 'alakazam']
        voice_panel = wx.ListBox(self, choices=sample_list,
                style=wx.LB_SINGLE)
        voice_panel.SetFont(self._font)
        voice_panel.Fit()
        self._sizer.Add(voice_panel, 0, wx.EXPAND)

        # Edit Buttons

        # Instrument Properties

        # More things
        self.Centre()
        self.Show(True)

