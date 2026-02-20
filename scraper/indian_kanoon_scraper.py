import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

BASE_SEARCH_URL = "https://indiankanoon.org/search/?formInput=constitution%20bench"

CATEGORY = "constitutional"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FOLDER = os.path.abspath(
    os.path.join(BASE_DIR, "..", "raw_data", CATEGORY)
)

os.makedirs(SAVE_FOLDER, exist_ok=True)
print("Final save folder:", SAVE_FOLDER)

headers = {
    "User-Agent": "Mozilla/5.0 (Educational Legal Research Project)"
}


def get_case_links(pages=1):
    case_links = []

    for page in range(1, pages + 1):
        url = f"{BASE_SEARCH_URL}&pagenum={page}"
        print(f"Scraping search page: {url}")

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a", href=True):
            if "/doc/" in link["href"]:
                full_url = urljoin("https://indiankanoon.org", link["href"])
                case_links.append(full_url)

        time.sleep(2)

    return list(set(case_links))  # remove duplicates


def extract_case_text(case_url):
    case_id = case_url.split("/")[-2]

    fragment_url = f"https://indiankanoon.org/docfragment/{case_id}/?big=3"

    response = requests.get(fragment_url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text(separator=" ")
    text = " ".join(text.split())

    if len(text) < 500:
        return None

    return text



def save_case(case_url, text):
    case_id = case_url.split("/")[-2]
    filename = f"{case_id}.txt"
    save_path = os.path.join(SAVE_FOLDER, filename)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    case_links = get_case_links(pages=2)  # adjust pages here
    print(f"Found {len(case_links)} cases")

    for link in tqdm(case_links[:20]):
        print("Processing:", link)  # limit for safety
        text = extract_case_text(link)
        if text:
            print("Text length:", len(text))
            save_case(link, text)
        else:
            print("No judgment text found!")

        time.sleep(2)


if __name__ == "__main__":
    main()
