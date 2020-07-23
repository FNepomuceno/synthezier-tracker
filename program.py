from data.core import Song
from event import Event, CLOSE, EventHandler, EventManager
from event.debug import EventPrinter
from graphics.program import GfxProgram
from audio.program import AudProgram


class Program(EventHandler):
    def __init__(self, filepath=None, debug=False):
        EventHandler.__init__(self)

        if filepath:
            Song().reset_to_load(filepath)
        if debug:
            printer = EventPrinter()
            EventManager().attach(printer)

        self._audio = AudProgram()
        self._graphics = GfxProgram()

    def run(self):
        self._graphics.start()

    def stop(self):
        self._audio.stop()
        self._graphics.stop()

    def handle_event(self, event:Event):
        if event == CLOSE:
            self.stop()


def main():
    Program(debug=True).run()


if __name__ == "__main__":
    main()
