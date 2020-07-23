import pyo


class SquareWave(pyo.EventInstrument):
    def __init__(self, **args):
        pyo.EventInstrument.__init__(self, **args)
        self.osc = pyo.LFO(freq=self.freq,
                       sharp=1,
                       type=2,
                       mul=self.env)
        self.mixer = pyo.Mixer()
        self.mixer.addInput(0, self.osc)
        self.mixer.setAmp(0, 0, 0.5)
        self.mixer.setAmp(0, 1, 0.5)
        self.mixer.out()
