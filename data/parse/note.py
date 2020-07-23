def import_note(data):
    result = {}

    if "note" in data:
        midinote = data["note"]
        if midinote >= 0:
            result["degree"] = (midinote-12) % 12
            result["octave"] = (midinote-12) // 12
    elif "degree" in data:
        result["degree"] = data["degree"]
        result["octave"] = data["octave"]

    if "volm" in data:
        result["volume"] = data["volm"]

    result["duration"] = data["tick"]

    return result

def export_note(note):
    from data.core.song import Song
    result = {}

    duration = note.duration()
    result["tick"] = duration
    if note.is_empty():
        return result

    volume = note.volume()
    result["volm"] = volume
    if note.is_silent():
        return result

    degree = note.degree()
    octave = note.octave()

    # TODO later: add condition for Song().scale().is_default()
    if Song().scale().is_midi():
        midinote = degree + 12 * octave + 12
        result["note"] = midinote
    else:
        result["degree"] = degree
        result["octave"] = octave

    return result
