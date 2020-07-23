from data.core.note import Note, empty_note
from data.parse.note import export_note


def default_slice():
    result = {
        "speed": 100,
        "divisions": 1,
        "notes": [
            empty_note(16),
        ]
    }

    return result


def import_slice(data):
    result = {
        "speed": data["speed"],
        "divisions": data["divisions"],
        "notes": [
            Note().load(note_notes)
            for note_notes in data["notes"]
        ]
    }

    return result


def export_slice(slc):
    result = {}
    result["name"] = slc.section()
    result["voice"] = slc.voice()
    result["speed"] = slc.speed()
    result["divisions"] = slc.divisions()
    result["notes"] = [export_note(note) for note in slc.notes()]
    return result
