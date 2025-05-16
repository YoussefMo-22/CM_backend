import requests
from bs4 import BeautifulSoup
import os
import hashlib

URLS = [
    "https://en.wikipedia.org/wiki/Coptic_Orthodox_Church",
    "https://en.wikipedia.org/wiki/Coptic_history",
    "https://en.wikipedia.org/wiki/Coptic_Museum",
    "https://copticorthodox.church/en/",
    "https://en.wikipedia.org/wiki/Coptic_art",
]

SAVE_DIR = "data/web_data"
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_and_clean(url):
    try:
        print(f"Fetching {url}")
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        return text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def save_text(text, url):
    hashname = hashlib.md5(url.encode()).hexdigest()
    filename = os.path.join(SAVE_DIR, f"{hashname}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    for url in URLS:
        content = fetch_and_clean(url)
        if content:
            save_text(content, url)

if __name__ == "__main__":
    main()