import pandas as pd
import pytest
import os

from main import from_pdf_path_to_df

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



test_data = [
    (("./test_units/pdf_tests/Séance du Conseil de Paris des 17 et 18 novembre 2020_page_320_324.pdf", False, True),
     {'legit_forgive': 10, 'present': 642, 'absent': 4}), # tabun 642
]

@pytest.mark.parametrize("inputs, outputs", test_data)
def test_from_pdf_path_to_df(inputs, outputs):
    """The first bool is to precise we don't want to save the df, the second bool is to precise we want to refresh"""
    df = from_pdf_path_to_df(*inputs)
    nb_presence_per_type : dict = df.groupby("status").count().T.to_dict(orient="records")[0]
    assert nb_presence_per_type == outputs