import os.path
import re
from typing import List, Union

import pdfplumber
from loguru import logger

from models.cr import presence_regex_mapping, PresenceRegexPattern, get_presence_per_period


class PDFProcessing:
    """This class is used to extract the text of the cr pages that contains presence"""

    def __init__(self, pdf_path: str):
        """Pdf pattern can be different from pdf according to the year"""
        self.pdf_path = pdf_path
        self.pdf_pattern = None
        self.nb_pages = None
        self.nb_pages_with_presence = None
        self.nb_pages_with_presence_index = None
        self._check_if_file_present()

    def _check_if_file_present(self):
        # find which page "Listes des membres présents" is in first_pdf
        logger.info(f"Extracting text from '{self.pdf_path}'")
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"File {self.pdf_path} does not exist")

    @staticmethod
    def check_if_at_least_one_word_from_a_words_list_is_in_text(text: str, regex_patterns: PresenceRegexPattern) -> bool:
        """

        :param text:
        :param regex_patterns:
        :return:
        """
        regex_patterns = list(regex_patterns.__dict__.values())
        for regex_pattern in regex_patterns:
            if re.search(regex_pattern, text):
                logger.debug(f"Found {regex_pattern=}")
                return True
        return False

    @staticmethod
    def return_string_if_present_in_text(text: str, regex_patterns: List[str]) -> Union[str, bool]:
        """

        :param text:
        :param regex_patterns:
        :return:
        """
        for regex_pattern in regex_patterns:
            if re.search(regex_pattern, text):
                logger.debug(f"Found {regex_pattern=}")
                return regex_pattern
        return False

    def extract_text_with_present_persons(self) -> List[str]:
        """
        Extract text from pdf file and return a list of text with the matching text.
        :param pdf_path: pdf path of CR
        :param matching_first_presence_page: this string will be search in the pdf to determine if the page is the one with the absence and precense of the
        persons
        :return: List of text of the page with the presence and absence of the persons
        """

        texts_in_pages = []
        found_first = False
        # create a pdf object with pdfplumber
        index_pages = []
        with pdfplumber.open(self.pdf_path) as pdf:
            self.nb_pages = len(pdf.pages)
            logger.debug(f"Nb of pages in {self.pdf_path}: {self.nb_pages}")
            # matching_text in test
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                logger.debug(f"index page: {i}")
                matched = PDFProcessing.return_string_if_present_in_text(text, presence_regex_mapping.keys())
                date_present = re.findall(get_presence_per_period, text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
                if (matched and date_present) and not found_first:
                    logger.debug(f"Found first page presence at {i} contains {matched=}")
                    self.pdf_pattern = matched
                    texts_in_pages.append(text)
                    index_pages.append(i)
                    found_first = True
                elif found_first:
                    presence_in_page = PDFProcessing.check_if_at_least_one_word_from_a_words_list_is_in_text(text=text, regex_patterns=presence_regex_mapping[self.pdf_pattern])
                    if presence_in_page:
                        logger.debug(f"Found presence in page {i}")
                        texts_in_pages.append(text)
                        index_pages.append(i)
                    else:
                        break

        self.nb_pages_with_presence = len(texts_in_pages)
        self.nb_pages_with_presence_index = index_pages
        logger.debug(f"Index Pages with presences are {index_pages}")

        return texts_in_pages
