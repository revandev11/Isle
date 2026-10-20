"""
Azərbaycandakı IT recruiter / talent acquisition LinkedIn profillərini SerpAPI ilə gətirir.

Quraşdırma:
1) pip install requests
2) serpapi.com-da qeydiyyatdan keç, dashboard-dan API key-i kopyala
3) export SERPAPI_KEY="..."      (Windows PowerShell: $env:SERPAPI_KEY="...")
4) python recruiter_linkedin_serpapi.py

"""
import csv
import os
import re
import sys
import time
from datetime import date

import requests

API_KEY = os.getenv("SERPAPI_KEY")

TITLES = [
    '"IT recruiter"',
    '"technical recruiter"',
    '"talent acquisition"',
    '"recruitment specialist"',
]

# Krediti qənaət etmək üçün siyahını qısalda bilərsən
COMPANIES = [
    "Kapital Bank", "PASHA Bank", "Azercell", "Bakcell", "Azerconnect",
    "ATL Tech", "Kontakt Home", "Rabita", "AccessBank", "Unibank",
    "ABB", "Azersun", "Naxtech", "Code Academy", 
]

PAGES_PER_QUERY = 1  # hər səhifə ~10 nəticə = 1 kredit
CSV_FILE = f"recruiters_linkedin_{date.today()}.csv"
PROFILE_RE = re.compile(r"linkedin\.com/in/[^/?#]+", re.I)


def search(query, page=0):
    r = requests.get(
        "https://serpapi.com/search.json",
        params={
            "engine": "google",
            "q": query,
            "api_key": API_KEY,
            "num": 10,
            "start": page * 10,
            "hl": "en",
        },
        timeout=30,
    )
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        print(f"SerpAPI xətası: {data['error']}")
        return []
    return data.get("organic_results", [])


def parse_title(title):
    # "Ad Soyad - Vəzifə - Şirkət | LinkedIn"
    clean = title.replace("| LinkedIn", "").strip()
    parts = [p.strip() for p in clean.split(" - ")]
    name = parts[0] if parts else ""
    headline = " - ".join(parts[1:]) if len(parts) > 1 else ""
    return name, headline


def build_queries():
    titles = "(" + " OR ".join(TITLES) + ")"
    queries = [("Ümumi", f"site:linkedin.com/in {titles} (Azerbaijan OR Baku)")]
    for c in COMPANIES:
        queries.append((c, f'site:linkedin.com/in {titles} "{c}" (Azerbaijan OR Baku)'))
    return queries


def main():
    if not API_KEY:
        print("SERPAPI_KEY təyin olunmayıb. Faylın başındakı izahata bax.")
        sys.exit(1)

    seen, rows = set(), []

    for label, q in build_queries():
        for page in range(PAGES_PER_QUERY):
            try:
                items = search(q, page)
            except requests.HTTPError as e:
                print(f"[{label}] xəta: {e}")
                break
            if not items:
                break
            for it in items:
                link = it.get("link", "")
                m = PROFILE_RE.search(link)
                if not m:
                    continue
                key = m.group(0).lower()
                if key in seen:
                    continue
                seen.add(key)
                name, headline = parse_title(it.get("title", ""))
                rows.append([name, headline, link, label, "baxılmayıb", ""])
                print(f"{name} | {headline}\n  {link}")
            time.sleep(0.5)

    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["Ad", "Başlıq", "LinkedIn", "Axtarış", "Status", "Qeyd"])
        w.writerows(rows)

    print(f"\nTapıldı: {len(rows)} profil. Fayl: {CSV_FILE}")


if __name__ == "__main__":
    main()