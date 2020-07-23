from data.core.song import Song
from event.event import Event
from event.handler import EventHandler

class GfxController(EventHandler):
    def __init__(self, view):
        EventHandler.__init__(self)
        self._view = view
        self._selected_panel = None

    def handle_event(self, event: Event):
        def recreate_view(*_):
            self._view.recreate()

        def select_data(source_id, values):
            if self._selected_panel:
                self._selected_panel.model().unselect()

            panel = self._view.panel_from_id(source_id)
            if not panel:
                return
            self._selected_panel = panel

            text = panel.model()
            if not text:
                return
            text.select(*values)
            self._view.refresh()

        def edit_data(source_id, values):
            if values == ("SPACE",) or values == ("TAB",):
                return

            panel = self._view.panel_from_id(source_id)
            if not panel or panel != self._selected_panel:
                return

            text = panel.model()
            text.input_ch(*values)

            data = text.as_data()
            Song().edit(data)

            self._view.refresh()

        handle = {
        "DATA_UPDATE": recreate_view,
        "CLICK": select_data,
        "KEY": edit_data,
        }.get(event.type(), lambda *_:None)

        handle(event.id(), event.values())
