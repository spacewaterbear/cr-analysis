import pytest

from processing.pdf_processing import PDFProcessing
import variables as v
import os

from utils.utils import Utils


os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


test_data = [
    ("./test_units/pdf_tests/Séance du Conseil de Paris des 17 et 18 novembre 2020_page_320_324.pdf", (4, 2, [1,2])),
]

@pytest.mark.parametrize("inputs, outputs", test_data)
def test_pdf_processing_class(inputs, outputs):
    """Output contains in order the number of pages, the number of pages with presence and the index of the pages with presence"""
    # change current working directory to project's root

    pdf_p = PDFProcessing(inputs)
    extracted = pdf_p.extract_text_with_present_persons(matching_first_presence_page=v.matching_first_presence_page)
    assert pdf_p.nb_pages == outputs[0]
    assert pdf_p.nb_pages_with_presence == outputs[1]
    assert pdf_p.nb_pages_with_presence_index == outputs[2]
    assert len(extracted) == outputs[1]








test_data = [
    (("Bonjour toi", "toi"), True),
    (("Bonjour les présents", "presents?"), True),
]

@pytest.mark.parametrize("inputs, outputs", test_data)
def test_check_if_at_least_one_word_from_a_words_list_is_in_text(inputs, outputs):
    assert PDFProcessing.check_if_at_least_one_word_from_a_words_list_is_in_text(*inputs) == outputs