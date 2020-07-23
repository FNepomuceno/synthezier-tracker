import wx

from data.core.song import Song
from data.view.slice import SliceText
from event import EventSource
from .slice import SliceView
from .voice import VoiceView


class MainView(wx.Frame, EventSource):
    def __init__(self, parent, *args, font_size=20, **kwargs):
        wx.Frame.__init__(self, parent, *args, **kwargs)
        EventSource.__init__(self)

        self._font_size=font_size

        # Setup
        self._panels = None
        self._setup_font()
        self._setup_container()
        self._setup_sections()
        self._setup_menu()
        self._setup_event_handling()

    def _catch_close(self, event):
        self.emit("ACTION", "CLOSE")

    def _catch_edit_voice(self, event):
        VoiceView(None)

    def _catch_new(self, event):
        self.emit("REQUEST_NEW", ())

    def _catch_open(self, event):
        with wx.FileDialog(self, "Open new file",
                wildcard="YAML files (*.yaml;*.yml)|*.yaml;*.yml",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return # User changed their mind

            # Proceed with chosen file
            pathname = file_dialog.GetPath()
            self.emit("REQUEST_LOAD", (pathname,))

    def _catch_save(self, event):
        with wx.FileDialog(self, "Save file",
                wildcard="YAML files (*.yaml;*.yml)|*.yaml;*.yml",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return # User changed their mind

            # Proceed with chosen path
            file_path = file_dialog.GetPath()
            self.emit("REQUEST_SAVE", (file_path,))

    def _catch_quit(self, event):
        self.Close()

    def _setup_container(self):
        # Make sizer
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self._sizer)

        # Add scrolled container
        scroller = wx.ScrolledWindow(self, size=(640, 480))
        self._sizer.Add(scroller, 1, wx.EXPAND)

        # Add sizer to scrolled container
        s_sizer = wx.BoxSizer(wx.VERTICAL)
        scroller.SetSizer(s_sizer)

        # Add container to scrolled container
        self._container = wx.Panel(scroller)
        s_sizer.Add(self._container, 1)

        # Add sizer to container
        c_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._container.SetSizer(c_sizer)

        # Set up scrolling and app settings
        scroller.SetScrollRate(self._font_width, self._font_height)
        self.Centre()
        self.Fit()

    def _setup_event_handling(self):
        # wxPython event handling
        self.Bind(wx.EVT_MENU, self._catch_new,
                self._menu["file"]["new"])
        self.Bind(wx.EVT_MENU, self._catch_open,
                self._menu["file"]["open"])
        self.Bind(wx.EVT_MENU, self._catch_save,
                self._menu["file"]["save"])
        self.Bind(wx.EVT_MENU, self._catch_quit,
                self._menu["file"]["quit"])
        self.Bind(wx.EVT_MENU, self._catch_edit_voice,
                self._menu["edit"]["voices"])
        self.Bind(wx.EVT_CLOSE, self._catch_close)

    def _setup_font(self):
        self._font = wx.Font(self._font_size, wx.FONTFAMILY_TELETYPE,
                wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        dc = wx.ClientDC(self)
        dc.SetFont(self._font)
        fm = dc.GetFontMetrics()
        self._font_width = fm.averageWidth
        self._font_height = fm.height

    def _setup_menu(self):
        # Setup to save menu items
        self._menu = {}
        self._menu["file"] = {}
        self._menu["edit"] = {}

        # Menus
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        edit_menu = wx.Menu()

        # File new
        file_new = file_menu.Append(
            wx.ID_NEW, "&New\tCtrl-N", "New Document")
        self._menu["file"]["new"] = file_new

        # File open
        file_open = file_menu.Append(
            wx.ID_OPEN, "&Open\tCtrl-O", "Load Document")
        self._menu["file"]["open"] = file_open

        # File save
        file_save = file_menu.Append(
            wx.ID_SAVE, "&Save\tCtrl-S", "Save Document")
        self._menu["file"]["save"] = file_save

        # File quit
        file_quit = file_menu.Append(
            wx.ID_EXIT, "E&xit", "Exit Application")
        self._menu["file"]["quit"] = file_quit

        # Edit voices
        edit_voices = edit_menu.Append(wx.ID_ANY, "Voices", "Manage "
                "voices")
        self._menu["edit"]["voices"] = edit_voices

        # Set menu bar
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(edit_menu, "&Edit")
        self.SetMenuBar(menu_bar)

    def _setup_sections(self):
        self._panels = [
            SliceView(self._container, self._font,
                model=SliceText(Song().selected_section(), voice))
            for voice in Song().voices()
        ]
        self._id_map = {
            panel.source_id(): panel
            for panel in self._panels
        }

        self._container.GetSizer().AddMany([
            (panel, 1) for panel in self._panels
        ])

        # Set title as well
        name = Song().file_name()
        if not name:
            name = "untitled"
        title = f"{name} | Note Tracker" 
        self.SetTitle(title)

    def panel(self, source_id):
        return self._id_map.get(source_id, None)

    def recreate_view(self):
        # Detach and destroy old panels
        self._container.GetSizer().Clear()
        [panel.Destroy() for panel in self._panels]

        # Create new panels and update view
        self._setup_sections()
        self.Layout()

    def refresh(self):
        self.Refresh()
