import os

from models.cr import PresenceRegexPattern

pdf_folder = "./pdfs"
csvs_folder = "./csvs"
json_link_name_pdf = os.path.join(pdf_folder, "link_name_pdf.json")

short_prefix = "short_"

all_csv_name= "all.csv"
all_csv_path = os.path.join(csvs_folder, all_csv_name)

# matching_text = "Excusés au sens du règlement"
matching_first_presence_page = "Présents :"
matching_texts = (PresenceRegexPattern().present, PresenceRegexPattern().legit_forgive, PresenceRegexPattern().forgive, PresenceRegexPattern().absent)

week_days = r"(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)"
months = r"(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)"
part_days = r"(?:matin|après-midi|soir|nuit)"
get_presence_per_period = f"{week_days} \d?\d {months} - {part_days}"


paris_pdf_url = "https://www.paris.fr/pages/comptes-rendus-et-debats-et-deliberations-du-conseil-224"



# random user agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}
