from decimal import Decimal
from fractions import Fraction
from math import log2 as log


UNISON = Decimal("0.0")
OCTAVE = Decimal("1200.0")
DEFAULT_INTERVALS = [Decimal(f"{n*100}.0") for n in range(12)]


def to_midi(self, interval, octave, division):
    BASE_NOTE = 12 # C0

    oct_size = to_cents(division)/100
    deg_offset = to_cents(interval)/100

    note = BASE_NOTE + deg_offset + oct_size*octave

    return note


def to_cents(self, interval):
    if isinstance(interval, Decimal):
        return float(interval)
    elif isinstance(interval, Fraction):
        return 1200*log(interval)
    else:
        raise ValueError("Invalid Interval")
