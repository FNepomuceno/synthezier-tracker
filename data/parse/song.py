from os.path import split
from yaml import safe_load_all as load
from yaml import safe_dump_all as dump

from data.core.scale import Scale
from data.core.section import Section
from data.parse.section import export_sections


def default_song():
    result = {}

    result["file_name"] = ""
    result["file_path"] = ""
    result["section_names"] = ["00"]
    result["voice_names"] = ["00"]
    result["sequence"] = ["00"]
    result["sequence_index"] = 0
    result["scale"] = Scale().load()
    result["sections"] = Section().load()

    return result


def import_song(input_path):
    with open(input_path) as file:
        text = file.read()
    header, data = list(load(text))
    file_path, file_name = split(input_path)

    result = {}

    result["file_name"] = file_name
    result["file_path"] = file_path
    result["section_names"] = header["sections"]
    result["voice_names"] = header["voices"]
    result["sequence"] = header["sequence"]
    result["sequence_index"] = 0
    result["scale"] = Scale().load(input_path)
    result["sections"] = Section().load(input_path)

    return result

def export_song(stream=None):
    header = export_header()
    sections = export_sections()
    result = dump(
        [header, sections],
        stream=stream,
        default_flow_style=False
    )
    return result

def export_header():
    from data.core.song import Song

    song = Song()
    scale = song.scale()

    result = {}

    result["api_ver"] = 1
    result["sections"] = list(sorted(song.sections()))
    result["voices"] = list(sorted(song.voices()))
    result["sequence"] = song.sequence()

    if not scale.is_midi():
        result["scalenotes"] = scale.pitch_list()
        result["scalefile"] = scale.file_name()

    return result
