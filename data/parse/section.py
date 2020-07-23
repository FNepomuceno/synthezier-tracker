from collections import defaultdict
from yaml import safe_load_all as load

from data.core.slice import Slice
from data.parse.slice import export_slice


def default_sections():
    section_names = ["00"]
    voice_names = ["00"]

    result = {
        section_name: {
            voice_name: Slice().load(section_name, voice_name)
            for voice_name in voice_names
        }
        for section_name in section_names
    }

    return result


def import_sections(input_path):
    with open(input_path) as file:
        text = file.read()
    header, data = list(load(text))

    # Section and voice names for slice normalizing
    section_names = set(header["sections"])
    voice_names = set(header["voices"])

    result = defaultdict(dict)
    for slice_data in data:
        section_name = slice_data["name"]
        voice_name = slice_data["voice"]

        # Skip extraneous sections
        if section_name not in section_names \
                or voice_name not in voice_names:
            continue 

        result[section_name][voice_name] = Slice().load(section_name,
                voice_name, slice_data)

    # Create missing sections
    for section in section_names:
        for voice in voice_names:
            if not result[section][voice]:
                result[section][voice] = default_slice()
                section["section"] = section_name
                section["voice"] = voice_name

    result = dict(result)
    return result

def export_sections():
    from data.core.song import Song

    song = Song()
    result = []

    sections = song.sections()
    voices = song.voices()

    for section in sections:
        for voice in voices:
            sec_slice = song.slice(section, voice)
            result.append(export_slice(sec_slice))

    return result
