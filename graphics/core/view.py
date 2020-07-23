class GfxView:
    def __init__(self, frame):
        self._frame = frame

    def panel_from_id(self, id):
        return self._frame.panel(id)

    def recreate(self):
        self._frame.recreate_view()

    def refresh(self):
        self._frame.Refresh()
