import os

import pytest
from pydantic import BaseModel

import variables as v
from processing.pdf_processing import PDFProcessing

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

test_data = [
    ("./test_units/pdf_tests/Séance du Conseil de Paris des 17 et 18 novembre 2020_page_320_324.pdf", (4, 2, [1, 2])),
    ("./test_units/pdf_tests/Séance du Conseil de Paris des 5, 6, 7 et 8 juillet 2022_page_503_513.pdf", (10, 7, list(range(1, 8)))),
    ("./test_units/pdf_tests/Séance du Conseil de Paris des 31 mai, 1er et 2 juin 2022_page_410_417.pdf", (7, 6, list(range(0, 6)))),
]


@pytest.mark.parametrize("inputs, outputs", test_data)
def test_pdf_processing_class(inputs, outputs):
    """Output contains in order the number of pages, the number of pages with presence and the index of the pages with presence"""
    # change current working directory to project's root

    pdf_p = PDFProcessing(inputs)
    extracted = pdf_p.extract_text_with_present_persons()
    assert pdf_p.nb_pages == outputs[0]
    assert pdf_p.nb_pages_with_presence == outputs[1]
    assert pdf_p.nb_pages_with_presence_index == outputs[2]
    assert len(extracted) == outputs[1]


class FakeBaseModel(BaseModel):
    """Fake class to test the BaseModel class"""
    random_string: str


test_data = [
    (("Bonjour toi", FakeBaseModel(random_string="toi")), True),
    (("Bonjour les présents", FakeBaseModel(random_string="présents?")), True),
    (("Bonjour les présents", FakeBaseModel(random_string="presents?")), False),
]


@pytest.mark.parametrize("inputs, outputs", test_data)
def test_check_if_at_least_one_word_from_a_words_list_is_in_text(inputs, outputs):
    assert PDFProcessing.check_if_at_least_one_word_from_a_words_list_is_in_text(*inputs) == outputs
