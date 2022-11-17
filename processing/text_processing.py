import re
from typing import List

import dateparser
import pandas as pd
from loguru import logger

from models.cr import get_presence_per_period, PresenceRegexPattern
from models.custom_execption import RegexFailed


class FromTextToDF:
    @staticmethod
    def extract_names_according_to_status(text: str, regex_pattern: str) -> str:
        """
        Extract the names of the persons according to their status.

        :return: the names of the persons
        """
        matches = re.findall(regex_pattern, text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if matches:
            return matches[0]
        else:
            logger.warning(f"Could not find the text with {regex_pattern=} in  {text[:40]=}")

    @staticmethod
    def extract_names_according_to_status_and_return_list(text: str, presence_regex_pattern: PresenceRegexPattern) -> dict:
        data = {}
        for absence_type, regex_pattern in presence_regex_pattern.dict().items():
            data[absence_type] = FromTextToDF.extract_names_according_to_status(text=text, regex_pattern=regex_pattern)
        # remove key where walue is none
        data = {k: v for k, v in data.items() if v is not None}
        return data

    @staticmethod
    def _extract_parsed_person_information_from_raw_text(text: str, status: str) -> dict:
        """
        Extract the parsed person information from the raw text.
        :param text: the raw text containing title firstname and lastname
        :return: the parsed person information
        """

        try:
            name_s = text.split()
            d = {"title": name_s[0].strip()}
            first_name = name_s[1].strip()
            last_name = "".join(name_s[2:]).strip().strip(",")
            # separate the first name and the last name by catching text in high caps which is the last names and lower caps which is the first names with
            # accent
            d["last_name"] = last_name
            d["first_name"] = first_name
            d["status"] = status
            return d
        except Exception as e:
            logger.error(f"Could not parse the name {text}")
            logger.error(e)

    @staticmethod
    def _convert_raw_text_to_dict(raw_text: str, status: str) -> List[dict]:
        """
        Convert the raw text to a dict with the status as key and the names as value.
        :param raw_text: the raw text
        :return: a dict with the status as key and the names as value
        """
        re_pattern_to_extract_names = r"(?:Mme|M\.)(?:.*?)(?:,|\b$|\.\n?$)"
        names = re.findall(re_pattern_to_extract_names, raw_text, re.DOTALL)
        if not names:
            raise RegexFailed(regex_pattern=re_pattern_to_extract_names, text=raw_text)
        parsed_names = [FromTextToDF._extract_parsed_person_information_from_raw_text(name, status=status) for name in names]
        return parsed_names

    @staticmethod
    def generate_df_from_segmented_data(data: dict) -> pd.DataFrame:
        """
        Generate a dataframe from the raw text.
        :param data: keys : presence status of the person, values : raw text containings the names
        :return: a dataframe
        """
        full_data = []
        for status, raw_text in data.items():
            full_data.extend(FromTextToDF._convert_raw_text_to_dict(raw_text, status))
        df = pd.DataFrame(full_data)
        return df

    @staticmethod
    def split_text_per_day_period(raw_text, prod=False) -> dict:
        """Sometimes, it can have the morning and the afternoon session in the same page : todo: fix prod stuff"""
        matches = re.finditer(get_presence_per_period, raw_text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        starting_index_match = [m.start(0) for m in matches]
        nb_matches = len(starting_index_match)
        if nb_matches == 0:
            message = f"Date not found for {raw_text=}"
            if prod:
                logger.warning(message)
            else:
                raise Exception(message)
        texts = []
        dates = re.findall(get_presence_per_period, raw_text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        for i, index in enumerate(starting_index_match):
            if i != len(starting_index_match) - 1:
                texts.append(raw_text[index:starting_index_match[i + 1]])
            else:
                texts.append(raw_text[index:])
        text_info = dict(zip(dates, texts))
        return text_info

    @staticmethod
    def add_date_and_period_columns(df: pd.DataFrame, file_name_without_extension: str) -> pd.DataFrame:
        """
        Add the date and the period columns to the dataframe.
        :param df: the dataframe
        :param file_name_without_extension: the file name without extension
        :return: the dataframe with the date and the period columns
        """
        # create day_period by splitting df['raw_time'] by "-" and keeping the second element striped
        df["day_period"] = df["raw_time"].str.split("-").str[1].str.strip()

        # get year from file name using regex
        year = re.findall(r"\d{4}", file_name_without_extension)[0]
        # use dateparser to get the date from the column "raw_time"
        df["date"] = df["raw_time"].apply(lambda x: dateparser.parse(year + re.sub(r"\d{4}", "", x.split("-")[0]), languages=["fr"]))

        return df
