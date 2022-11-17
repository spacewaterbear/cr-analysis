import os


pdf_folder = "./pdfs"
csvs_folder = "./csvs"
json_link_name_pdf = os.path.join(pdf_folder, "link_name_pdf.json")

short_prefix = "short_"

all_csv_name= "all.csv"
all_csv_path = os.path.join(csvs_folder, all_csv_name)



paris_pdf_url = "https://www.paris.fr/pages/comptes-rendus-et-debats-et-deliberations-du-conseil-224"



# random user agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}
