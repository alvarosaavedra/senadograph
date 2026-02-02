"""Web scraper for Chilean Senate data."""

import requests
import time
import re
from bs4 import BeautifulSoup
from typing import List, Optional
from urllib.parse import urljoin

from config import (
    BASE_URL,
    SENATORS_URL,
    LAWS_URL,
    LOBBY_URL,
    REQUEST_TIMEOUT,
    REQUEST_DELAY,
    IMAGES_DIR,
)
from models import Senator, Party, Law, Committee


class SenateScraper:
    """Scraper for Chilean Senate website."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def _get(self, url: str) -> Optional[BeautifulSoup]:
        """Make a GET request and return BeautifulSoup object."""
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            time.sleep(REQUEST_DELAY)
            return BeautifulSoup(response.content, "lxml")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_senators(self) -> List[Senator]:
        """Scrape list of all senators."""
        senators = []
        soup = self._get(SENATORS_URL)

        if not soup:
            return senators

        # Find senator elements
        senator_elements = soup.find_all("div", class_="senador-item")

        for element in senator_elements:
            try:
                link = element.find("a", href=True)
                if not link:
                    continue

                detail_url = urljoin(BASE_URL, link["href"])
                senator = self._scrape_senator_detail(detail_url)

                if senator:
                    senators.append(senator)

            except Exception as e:
                print(f"Error parsing senator: {e}")
                continue

        return senators

    def _scrape_senator_detail(self, url: str) -> Optional[Senator]:
        """Scrape detailed information for a single senator."""
        soup = self._get(url)

        if not soup:
            return None

        try:
            # Extract senator ID from URL
            senator_id = self._extract_id_from_url(url, "senator")

            # Extract name
            name_elem = soup.find("h1", class_="senador-nombre")
            name = name_elem.text.strip() if name_elem else "Unknown"

            # Extract party
            party_elem = soup.find("span", class_="senador-partido")
            party = party_elem.text.strip() if party_elem else ""

            # Extract region
            region_elem = soup.find("span", class_="senador-region")
            region = region_elem.text.strip() if region_elem else ""

            # Extract email
            email_elem = soup.find("a", href=re.compile(r"mailto:"))
            email = email_elem["href"].replace("mailto:", "") if email_elem else None

            # Extract photo URL
            photo_elem = soup.find("img", class_="senador-foto")
            photo_url = None
            if photo_elem and photo_elem.get("src"):
                photo_url = urljoin(BASE_URL, photo_elem["src"])
                self._download_photo(senator_id, photo_url)

            # Extract biography
            bio_elem = soup.find("div", class_="senador-biografia")
            biography = bio_elem.text.strip() if bio_elem else None

            return Senator(
                id=senator_id,
                name=name,
                party=party,
                region=region,
                email=email,
                photo_url=photo_url,
                biography=biography,
                active=True,
            )

        except Exception as e:
            print(f"Error scraping senator detail: {e}")
            return None

    def _download_photo(self, senator_id: str, photo_url: str):
        """Download and save senator photo."""
        try:
            response = self.session.get(photo_url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            # Save to images directory
            filename = f"{senator_id}.jpg"
            filepath = f"{IMAGES_DIR}/{filename}"

            with open(filepath, "wb") as f:
                f.write(response.content)

        except Exception as e:
            print(f"Error downloading photo for {senator_id}: {e}")

    def scrape_parties(self) -> List[Party]:
        """Scrape political parties."""
        parties = []
        soup = self._get(SENATORS_URL)

        if not soup:
            return parties

        try:
            # Find party filter or list
            party_elements = soup.find_all("span", class_="partido-badge")

            seen_parties = set()
            for element in party_elements:
                party_name = element.text.strip()
                if party_name and party_name not in seen_parties:
                    seen_parties.add(party_name)
                    party_id = f"party_{self._sanitize_id(party_name)}"

                    parties.append(
                        Party(
                            id=party_id,
                            name=party_name,
                            short_name=party_name,
                            color=self._get_party_color(party_name),
                        )
                    )

        except Exception as e:
            print(f"Error scraping parties: {e}")

        return parties

    def scrape_laws(self, limit: int = 100) -> List[Law]:
        """Scrape legislative projects."""
        laws = []
        soup = self._get(LAWS_URL)

        if not soup:
            return laws

        try:
            law_elements = soup.find_all("div", class_="proyecto-item")

            for element in law_elements[:limit]:
                try:
                    link = element.find("a", href=True)
                    if not link:
                        continue

                    detail_url = urljoin(BASE_URL, link["href"])
                    law = self._scrape_law_detail(detail_url)

                    if law:
                        laws.append(law)

                except Exception as e:
                    print(f"Error parsing law: {e}")
                    continue

        except Exception as e:
            print(f"Error scraping laws: {e}")

        return laws

    def _scrape_law_detail(self, url: str) -> Optional[Law]:
        """Scrape detailed information for a single law."""
        soup = self._get(url)

        if not soup:
            return None

        try:
            law_id = self._extract_id_from_url(url, "law")

            # Extract boletin
            boletin_elem = soup.find("span", class_="proyecto-boletin")
            boletin = boletin_elem.text.strip() if boletin_elem else ""

            # Extract title
            title_elem = soup.find("h1", class_="proyecto-titulo")
            title = title_elem.text.strip() if title_elem else ""

            # Extract status
            status_elem = soup.find("span", class_="proyecto-estado")
            status = self._normalize_status(
                status_elem.text.strip() if status_elem else "in_discussion"
            )

            # Extract date
            date_elem = soup.find("span", class_="proyecto-fecha")
            date_proposed = date_elem.text.strip() if date_elem else ""

            return Law(
                id=law_id,
                boletin=boletin,
                title=title,
                date_proposed=date_proposed,
                status=status,
            )

        except Exception as e:
            print(f"Error scraping law detail: {e}")
            return None

    def _extract_id_from_url(self, url: str, prefix: str) -> str:
        """Extract ID from URL."""
        # Extract last part of URL path
        parts = url.rstrip("/").split("/")
        last_part = parts[-1] if parts else "unknown"
        return f"{prefix}_{last_part}"

    def _sanitize_id(self, text: str) -> str:
        """Sanitize text to create a valid ID."""
        sanitized = re.sub(r"[^\w\s-]", "", text.lower())
        sanitized = re.sub(r"[-\s]+", "_", sanitized)
        return sanitized[:50]

    def _get_party_color(self, party_name: str) -> str:
        """Get color for a party (placeholder)."""
        # This would map known parties to their colors
        color_map = {
            "RN": "#0054a6",
            "PS": "#e4002b",
            "UDI": "#1a237e",
            "PDC": "#0066cc",
            "PPD": "#ff6600",
        }
        return color_map.get(party_name, "#cccccc")

    def _normalize_status(self, status: str) -> str:
        """Normalize law status."""
        status_lower = status.lower()
        if "aprobado" in status_lower:
            return "approved"
        elif "rechazado" in status_lower:
            return "rejected"
        elif "retirado" in status_lower:
            return "withdrawn"
        return "in_discussion"


def main():
    """Main scraping function."""
    print("Starting Senate scraper...")
    scraper = SenateScraper()

    # Scrape parties
    print("Scraping parties...")
    parties = scraper.scrape_parties()
    print(f"Found {len(parties)} parties")

    # Scrape senators
    print("Scraping senators...")
    senators = scraper.scrape_senators()
    print(f"Found {len(senators)} senators")

    # Scrape laws
    print("Scraping laws...")
    laws = scraper.scrape_laws(limit=50)
    print(f"Found {len(laws)} laws")

    # Save to JSON files for inspection
    import json
    import os

    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)

    with open(f"{data_dir}/parties.json", "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in parties], f, ensure_ascii=False, indent=2)

    with open(f"{data_dir}/senators.json", "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in senators], f, ensure_ascii=False, indent=2)

    with open(f"{data_dir}/laws.json", "w", encoding="utf-8") as f:
        json.dump([l.to_dict() for l in laws], f, ensure_ascii=False, indent=2)

    print("Scraping complete! Data saved to data/ directory")


if __name__ == "__main__":
    main()
