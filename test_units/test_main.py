import os

import pytest

from main import from_pdf_path_to_df

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

test_data = [
    ("./test_units/pdf_tests/Séance du Conseil de Paris des 17 et 18 novembre 2020_page_320_324.pdf",
     {'legit_forgive': 10, 'present': 642, 'absent': 4}),
    ("./test_units/pdf_tests/Séance du Conseil de Paris des 5, 6, 7 et 8 juillet 2022_page_503_513.pdf",
     {'legit_forgive': 102, 'present': 1016, 'absent': 23, 'forgive': 7}),
    ("./test_units/pdf_tests/Séance du Conseil de Paris des 31 mai, 1er et 2 juin 2022_page_410_417.pdf",
     {'legit_forgive': 44, 'present': 912, 'absent': 16, 'forgive': 12}),
]


@pytest.mark.parametrize("inputs, outputs", test_data)
def test_from_pdf_path_to_df(inputs, outputs):
    save_csv, refresh = False, True
    df = from_pdf_path_to_df(pdf_path=inputs, to_csv=save_csv, refresh=refresh)
    nb_presence_per_type: dict = df.groupby("status").count().T.to_dict(orient="records")[0]
    assert nb_presence_per_type == outputs
