from event.event import Event
from event.handler import EventHandler


class AudController(EventHandler):
    def __init__(self, view, player):
        EventHandler.__init__(self)
        self._view = view
        self._player = player

    def handle_event(self, event: Event):
        def handle_key(source_id, values):
            if values == ("SPACE",):
                self._player.play_pause()
        def reset_player(source_id, values):
            self._player.stop()
        def restart_player(source_id, values):
            self._view.reset()
            self._player.stop()

        handle = {
        "KEY": handle_key,
        "MODEL_UPDATE": reset_player,
        "DATA_UPDATE": restart_player,
        }.get(event.type(), lambda *_:None)

        handle(event.id(), event.values())
