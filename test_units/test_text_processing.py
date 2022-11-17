import os

import pytest

from models.cr import PresenceRegexPattern, presence_regex_mapping, present_template, date_template
from processing.text_processing import FromTextToDF
from utils.file_handler import FileHandler

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

base_extracted_text = "./test_units/pdf_tests/extracted_{}.txt"

test_data = [
    (0, (2, ["Mardi 17 novembre - Matin", "Mardi 17 novembre - Après-midi"])),
    (1, (2, ["Mercredi 18 novembre - Matin", "Mercredi 18 novembre - Après-midi"])),
    (2, (1, ["Mercredi 18 novembre - Après-midi"])),
    (3, (1, ["Jeudi 7 juillet 2022 - Après-midi"])),
]


@pytest.mark.parametrize("inputs, outputs", test_data)
def test_split_text_per_day_period(inputs, outputs):
    """First output is the number of day period detected"""
    file_path = base_extracted_text.format(inputs)
    text = FileHandler.read_file(file_path)
    dico = FromTextToDF.split_text_per_day_period(text)
    expected_nb_elements, dates = outputs[0], outputs[1]
    assert len(dico) == expected_nb_elements
    assert list(dico.keys()) == dates


test_data = [
    ((0, present_template), ["absent", "legit_forgive", "present"]),
    ((1, present_template), ["absent", "legit_forgive", "present"]),
    ((2, present_template), ["absent", "legit_forgive", "present"]),
    ((3, date_template), ["absent", "legit_forgive", "present", "forgive"]),
]


@pytest.mark.parametrize("inputs, outputs", test_data)
def test_presence_extraction(inputs, outputs):
    file_number, template = inputs
    file_path = base_extracted_text.format(file_number)
    text = FileHandler.read_file(file_path)
    presence_regex_pattern: PresenceRegexPattern = presence_regex_mapping[template]
    dico = FromTextToDF.extract_names_according_to_status_and_return_list(text, presence_regex_pattern)
    assert set(list(dico.keys())) == set(outputs)


test_data = [
    (('M. Christophe GIRARD', "absent"), [{"title": "M.", "last_name": "GIRARD", "first_name": "Christophe", "status": "absent"}]),
    (('M. Patrick VIRY, M. Ariel WEIL', "absent"), [
        {"title": "M.", "last_name": "VIRY", "first_name": "Patrick", "status": "absent"},
        {"title": "M.", "last_name": "WEIL", "first_name": "Ariel", "status": "absent"},
    ]),
]


@pytest.mark.parametrize("inputs, outputs", test_data)
def test__convert_raw_text_to_dict(inputs, outputs):
    assert FromTextToDF._convert_raw_text_to_dict(*inputs) == outputs
