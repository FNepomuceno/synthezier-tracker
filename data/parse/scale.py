from decimal import Decimal
from fractions import Fraction
from os.path import dirname, split, join
from re import search
from yaml import safe_load_all as load


# TODO: add file option to use this default scale
def default_scale():
    result = {}

    result["pitches"] = [
        "Cbb", "Cb", "C", "C#", "Cx",
        "Dbb", "Db", "D", "D#", "Dx",
        "Ebb", "Eb", "E", "E#", "Ex",
        "Fbb", "Fb", "F", "F#", "Fx",
        "Gbb", "Gb", "G", "G#", "Gx",
        "Abb", "Ab", "A", "A#", "Ax",
        "Bbb", "Bb", "B", "B#", "Bx",
    ]
    pitch_semitones = [
        -2, -1, 0, 1, 2,
        0, 1, 2, 3, 4,
        2, 3, 4, 5, 6,
        3, 4, 5, 6, 7,
        5, 6, 7, 8, 9,
        7, 8, 9, 10, 11,
        9, 10, 11, 12, 13,
    ]
    result["intervals"] = [
        format_interval(Decimal(f"{100*n}.0"))
        for n in pitch_semitones
    ]
    result["division"] = format_interval(Decimal("1200.0"))
    result["size"] = len(result["pitches"])

    return result


def midi_scale():
    result = {}

    result["pitches"] = ["C", "C#", "D", "Eb", "E", "F",
            "F#", "G", "G#", "A", "Bb", "B"]
    result["intervals"] = [
        format_interval(Decimal(f"{100*n}.0"))
        for n in range(12)
    ]
    result["division"] = format_interval(Decimal("1200.0"))
    result["size"] = len(result["pitches"])

    return result


def import_scale(input_path):
    with open(input_path) as file:
        text = file.read()
    header, data = list(load(text))

    if "scalefile" not in header:
        return midi_scale()

    result = {}

    # Pitches and size
    result["pitches"] = header["scalenotes"]
    result["size"] = len(result["pitches"])

    # Intervals and division
    file_dir = dirname(input_path)
    file_name = header["scalefile"]
    file_path = join(file_dir, file_name) 
    scale_intervals = import_intervals(file_path)
    result["file_name"] = file_name
    result["file_path"] = file_dir
    UNISON = Decimal("0.0")

    result["intervals"] = [
        format_interval(interval)
        for interval in [UNISON] + scale_intervals[:-1]
    ]
    result["division"] = format_interval(scale_intervals[-1])

    # Verify interval array and scale array are the same size
    interval_size = len(result["intervals"])
    if interval_size != result["size"]:
        raise ValueError("Interval and pitch lists do not match in size")

    return result


def import_intervals(input_path):
    lines_before_intervals = 2
    notes = []

    with open(input_path) as file:
        for line in file:
            line = line.strip()
            if line[0] == '!':
                continue # Line is a comment
            elif lines_before_intervals > 0:
                lines_before_intervals -= 1
            else:
                ratio = to_ratio(line)
                cents = to_cents(line)
                notes.append(ratio or cents)

    return notes


def to_ratio(text):
    pat = r"^\s*(\d+)(?:/(\d+))?(?:\s+.*|)$"
    match = search(pat, text)
    if match is None:
        return None
    num, den = match.groups()
    num = int(num)
    den = int(den) if den is not None else 1
    if num < 0 or den <= 0:
        raise ValueError("Invalid fraction")
    return Fraction(num, den)


def to_cents(text):
    pat = r"\s*(\d+)\.(\d+)?(?:\s+.*|)$"
    match = search(pat, text)
    if match is None:
        return None
    whl, prt = match.groups()
    whl = whl
    prt = prt if prt is not None else '0'
    return Decimal("{}.{}".format(whl, prt))


def format_interval(interval):
    if isinstance(interval, Decimal):
        return (interval, "CENTS")
    elif isinstance(interval, Fraction):
        return (interval, "PURE")
    else:
        raise ValueError("Invalid interval type")
