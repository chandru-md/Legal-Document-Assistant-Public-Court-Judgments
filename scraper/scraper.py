import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

BASE_URL = "https://www.supremecourt.gov/opinions/23pdf/23-719_19m2.pdf"   # Replace with real site
CATEGORY = "constitutional"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SAVE_FOLDER = os.path.join(BASE_DIR, "..", "raw_data", CATEGORY)
SAVE_FOLDER = os.path.abspath(SAVE_FOLDER)

os.makedirs(SAVE_FOLDER, exist_ok=True)

print("Final save folder:", SAVE_FOLDER)

headers = {
    "User-Agent": "Mozilla/5.0 (Legal Research Bot - Educational Project)"
}


def get_case_links():
    response = requests.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    case_links = []

    for link in soup.find_all("a", href=True):
        if ".pdf" in link["href"]:
            full_url = urljoin(BASE_URL, link["href"])
            case_links.append(full_url)

    return case_links


def download_pdf(pdf_url):
    filename = pdf_url.split("/")[-1]
    save_path = os.path.join(SAVE_FOLDER, filename)

    print("Saving to:", save_path)

    if os.path.exists(save_path):
        return

    response = requests.get(pdf_url, headers=headers)

    with open(save_path, "wb") as f:
        f.write(response.content)

    time.sleep(2)   # Polite delay


def main():
    case_links = get_case_links()

    print(f"Found {len(case_links)} cases")

    for link in tqdm(case_links):
        download_pdf(link)


if __name__ == "__main__":
    main()

