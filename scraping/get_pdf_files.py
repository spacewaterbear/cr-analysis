import os
import re
from typing import Tuple

import requests
from loguru import logger

from utils.file_handler import FileHandler
from utils.utils import Utils
import variables as v


def _extract_pdf_url_and_name(text: str) -> Tuple[str, str]:
    """Extract the pdf link and the name associated"""
    pdf_name = re.findall(r'>(.*?)<', text)[0]

    pdf_url = text.split('"')[0]
    return pdf_name, pdf_url


def _get_pdf_link_and_names(save=True, refresh=False) -> dict:
    """Get the pdf link and the name associated
    :return: a dict with the link name as key and the pdf link as value"""

    # check if v.json_link_name_pdf_path exists
    if os.path.exists(v.json_link_name_pdf) and not refresh:
        return FileHandler.load_json(v.json_link_name_pdf)
    r = requests.get(v.paris_pdf_url, headers=v.headers)
    # extract part of request containing the pdf link and link nmae
    raw_links_and_names = re.findall(r'href="(https://cdn.paris.*?)a>', r.text)
    links_pdf = {_extract_pdf_url_and_name(link)[0]: _extract_pdf_url_and_name(link)[1] for link in raw_links_and_names}
    # get only séance du conseil de Paris
    links_pdf = {k: v for k, v in links_pdf.items() if k.startswith("Séance")}
    if save:
        FileHandler.save_dic_as_json(dic=links_pdf, json_path=v.json_link_name_pdf)
    return links_pdf


def _downloading_pdf_files(links_pdf: dict):
    """Download the pdf files"""
    for pdf_name, pdf_url in links_pdf.items():
        file_path = os.path.join(v.pdf_folder, f"{pdf_name}.pdf")
        if not os.path.exists(file_path):
            logger.debug(f"{pdf_name} not found, downloading it")
            r = requests.get(pdf_url, headers=v.headers)
            with open(file_path, "wb") as f:
                f.write(r.content)
            Utils.delay()



def compare_downloaded_pdf_with_websites_one():
    """Compare the pdf downloaded with the one on the website"""
    # get the pdf link and name associated

    if os.path.exists(v.json_link_name_pdf):
        current_informations = FileHandler.load_json(v.json_link_name_pdf)
        links_pdf = _get_pdf_link_and_names(save=True)

        # check if links_pdf is the same as current_informations
        if current_informations == links_pdf:
            logger.info("The pdf downloaded are the same as the one on the website, doing nothing")
        else:
            logger.info("The pdf downloaded are not the same as the one on the website, downloading the new ones")
            _downloading_pdf_files(links_pdf=links_pdf)
    else:
        links_pdf = _get_pdf_link_and_names()
        _downloading_pdf_files(links_pdf=links_pdf)

    return links_pdf


if __name__ == '__main__':
    compare_downloaded_pdf_with_websites_one()
