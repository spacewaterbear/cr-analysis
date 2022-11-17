import os
from pathlib import Path
from typing import List

import dateparser
import pandas as pd
from loguru import logger

import variables as v
from models.cr import PresenceRegexPattern, presence_regex_mapping
from processing.pdf_processing import PDFProcessing
from processing.text_processing import FromTextToDF
from utils.file_handler import FileHandler
from utils.utils import Utils


def from_pdf_path_to_df(pdf_path: str, to_csv=True, refresh=False) -> pd.DataFrame:
    logger.info(f"Processing pdf : {pdf_path}")
    file_name_without_extension = Path(pdf_path).stem
    csv_path = os.path.join(v.csvs_folder, f"{file_name_without_extension}.csv")
    if os.path.exists(csv_path) and not refresh:
        logger.info(f"CSV already exists for {pdf_path}")
        df = pd.read_csv(csv_path)
        return df
    pdf_p = PDFProcessing(pdf_path)
    raw_texts: List[str] = pdf_p.extract_text_with_present_persons()
    presence_regex_pattern: PresenceRegexPattern = presence_regex_mapping[pdf_p.pdf_pattern]
    nb_presences_pages_founds = len(raw_texts)
    if nb_presences_pages_founds == 0:
        logger.warning(f"No presence page found in {pdf_path}")
    else:
        logger.debug(f"len of raw_texts : {nb_presences_pages_founds}")
    df = pd.DataFrame()

    for index_page, raw_text in zip(pdf_p.nb_pages_with_presence_index, raw_texts):
        raw_text_per_day_period: dict= FromTextToDF.split_text_per_day_period(raw_text)
        for period, text_per_period in raw_text_per_day_period.items():
            data: dict = FromTextToDF.extract_names_according_to_status_and_return_list(text_per_period, presence_regex_pattern=presence_regex_pattern)
            tem_df = FromTextToDF.generate_df_from_segmented_data(data)
            tem_df['raw_time'] = period
            tem_df['index_page'] = index_page
            logger.debug(tem_df["status"].value_counts())
            # print(index_page)
            # print( tem_df["status"].value_counts())
            df = pd.concat([df, tem_df], axis=0, ignore_index=True)


    if df.empty:
        FileHandler.update_no_presence_found_pdf(pdf_path=pdf_path)
        logger.warning(f"df is empty for {pdf_path}")
        return df
    logger.info("Cleaning df")
    df = FromTextToDF.add_date_and_period_columns(df, file_name_without_extension)
    df = df.applymap(Utils.clean_string)
    if to_csv:
        df.to_csv(csv_path, index=False)
    return df

def generate_final_csv_from_pdfs(pdf_files_path: List[str], refresh: bool):
    pdf_list = []
    for pdf_path in pdf_files_path:
        pdf_name = Path(pdf_path).stem
        df = from_pdf_path_to_df(pdf_path, refresh=refresh)
        df["pdf_name"] = pdf_name
        pdf_list.append(df)
    df = pd.concat(pdf_list, axis=0, ignore_index=True)
    df["date"] = df["raw_time"].apply(lambda x: dateparser.parse(x.split("-")[0], languages=["fr"]))

    if not df.empty:
        df.to_csv(v.all_csv_path, index=False)
    return df


if __name__ == '__main__':

    use_only_short_pdf = False

    files = os.listdir(v.pdf_folder)
    pdf_files_path = [os.path.join(v.pdf_folder, file) for file in files if file.endswith(".pdf")]
    logger.info(f"Number of pdf files : {len(pdf_files_path)}")
    years = (2022,)
    # years = (2020,)
    pdf_files_path = [pdf_path for pdf_path in pdf_files_path if FileHandler.check_if_years_present_in_file_path(pdf_path, years)]
    if use_only_short_pdf:
        pdf_files_path = [pdf_path for pdf_path in pdf_files_path if os.path.basename(pdf_path).startswith(v.short_prefix)]
        logger.info(f"len of short pdf_files : {len(pdf_files_path)}")
    else:
        pdf_files_path = [pdf_path for pdf_path in pdf_files_path if not os.path.basename(pdf_path).startswith(v.short_prefix)]

        logger.info(f"len of pdf_files_path without short file: {len(pdf_files_path)}")
    # pdf_pahts = ['./pdfs/Séance du Conseil de paris des 17 et 18 novembre 2020.pdf']
    # pdf_files_path = [pdf_path for pdf_path in pdf_files_path if os.path.basename(pdf_path).startswith("Séance exceptionnelle")]
    logger.info(f"len of filtered pdf_files : {len(pdf_files_path)}")

    # pdf_files_path = ['./pdfs/Séance du Conseil de Paris des 17 et 18 novembre 2020.pdf']
    # pdf_files_path = ['./pdfs/Séance du Conseil de Paris des 17 et 18 novembre 2020_page_320_324.pdf']
    # pdf_files_path = ['./pdfs/Séance du Conseil de Paris des 5, 6, 7 et 8 juillet 2022_page_503_513.pdf']
    generate_final_csv_from_pdfs(pdf_files_path, refresh=False)
    # generate_csv_from_pdf(pdf_files_path, refresh=False)

