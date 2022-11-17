import json
import os
from pathlib import Path
from typing import Tuple

# open a pdf with pydf2
import PyPDF2
from loguru import logger


class FileHandler:

    @staticmethod
    def read_file(file_path: str):
        with open(file_path, "r") as f:
            return f.read()

    @staticmethod
    def save_dic_as_json(dic: dict, json_path: str):
        """Save dic as json"""
        logger.info(f"Saving dic as json in {json_path}")
        with open(json_path, "w") as f:
            json.dump(dic, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load_json(json_path: str):
        """Load json file"""
        logger.info(f"Loading json from {json_path}")
        with open(json_path, "r") as f:
            return json.load(f)

    @staticmethod
    def save_file(text: str, file_name: str):
        """Save text in file"""
        logger.info(f"Saving text in {file_name}")
        with open(file_name, "w") as f:
            f.write(text)

    @staticmethod
    def extract_specific_page_from_pdf(pdf_path: str, page_range: Tuple[int, int]):
        """Use for test and debug purpose"""
        new_pdf_path = os.path.join(os.path.dirname(pdf_path), f"{Path(pdf_path).stem}_page_{page_range[0]}_{page_range[1]}.pdf")
        pdf_file_obj = open(pdf_path, 'rb')
        logger.info(f"Opening pdf {pdf_path} and saving only pages {page_range} to {new_pdf_path}")
        pdf_writer = PyPDF2.PdfFileWriter()
        pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
        for page_num in range(page_range[0], page_range[1]):
            page_obj = pdf_reader.getPage(page_num)
            pdf_writer.addPage(page_obj)

        with open(new_pdf_path, 'wb') as out:
            pdf_writer.write(out)

    @staticmethod
    def check_if_years_present_in_file_path(file_path: str, years: tuple) -> bool:
        """

        :param file_path:
        :param years:
        :return:
        """

        for year in years:
            if str(year) in file_path:
                return True
        return False

    @staticmethod
    def update_no_presence_found_pdf(pdf_path: str):
        with open('logs.txt', "a+") as f:
            f.write(f"{pdf_path}\n")
