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
            return BeautifulSoup(response.content, "html.parser")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_senators(self) -> List[Senator]:
        """Scrape list of all senators."""
        senators = []
        soup = self._get(SENATORS_URL)

        if not soup:
            return senators

        # Find rows with senator data - each row has 4 tds
        # TD 0: wrapper table, TD 1: photo, TD 2: info, TD 3: party
        all_rows = soup.find_all("tr")
        senator_rows = [
            r for r in all_rows if len(r.find_all("td", class_="clase_td")) >= 3
        ]

        for row in senator_rows:
            try:
                tds = row.find_all("td", class_="clase_td")

                if len(tds) < 3:
                    continue

                # Parse senator info directly from the list page
                # TD with class "clase_td" containing the name is typically the second one (index 2 in nested)
                # But let's find the one with the senator name pattern
                info_td = None
                party_td = None
                photo_td = None

                for td in tds:
                    text = td.get_text()
                    if "Partido:" in text:
                        party_td = td
                    elif any(x in text for x in ["Región:", "Email:", "Teléfono:"]):
                        info_td = td
                    elif td.find("img", class_="imag_senador"):
                        photo_td = td

                if not info_td or not party_td:
                    continue

                # Extract name from info_td
                name_text = info_td.get_text(strip=True)
                name = name_text.split("Región:")[0].strip()

                # Extract region
                region_match = re.search(r"Región:\s*([^|]+)", info_td.get_text())
                region = region_match.group(1).strip() if region_match else ""

                # Extract circumscription
                circ_match = re.search(
                    r"Circunscripción:\s*([^<]+)", info_td.get_text()
                )
                circ = circ_match.group(1).strip() if circ_match else ""

                # Extract email
                email_elem = info_td.find("a", href=re.compile(r"mailto:"))
                email = None
                if email_elem and email_elem.get("href"):
                    email = str(email_elem["href"]).replace("mailto:", "")

                # Extract party
                party_elem = party_td.find("strong")
                party = party_elem.get_text(strip=True) if party_elem else ""

                # Extract photo URL
                photo_url = None
                senator_id = self._sanitize_id(name)
                if photo_td:
                    img = photo_td.find("img", class_="imag_senador")
                    if img and img.get("src"):
                        photo_url = urljoin(BASE_URL, str(img["src"]))
                        self._download_photo(senator_id, photo_url)

                senator = Senator(
                    id=senator_id,
                    name=name,
                    party=party,
                    region=region,
                    email=email,
                    photo_url=photo_url,
                    biography=None,
                    active=True,
                )

                senators.append(senator)

            except Exception as e:
                print(f"Error parsing senator: {e}")
                continue

        return senators

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

    def scrape_parties(self, senators: Optional[List[Senator]] = None) -> List[Party]:
        """Extract political parties from senator data."""
        parties = []

        if senators:
            # Extract unique parties from senators
            seen_parties = {}
            for senator in senators:
                party_name = senator.party.strip()
                if party_name and party_name not in seen_parties:
                    party_id = f"party_{self._sanitize_id(party_name)}"
                    party = Party(
                        id=party_id,
                        name=party_name,
                        short_name=party_name,
                        color=self._get_party_color(party_name),
                    )
                    parties.append(party)
                    seen_parties[party_name] = party

        else:
            # Fallback: try to scrape from the senators page
            soup = self._get(SENATORS_URL)

            if not soup:
                return parties

            try:
                all_rows = soup.find_all("tr")
                senator_rows = [
                    r for r in all_rows if len(r.find_all("td", class_="clase_td")) >= 3
                ]

                seen_parties = {}
                for row in senator_rows:
                    tds = row.find_all("td", class_="clase_td")
                    for td in tds:
                        if "Partido:" in td.get_text():
                            party_elem = td.find("strong")
                            if party_elem:
                                party_name = party_elem.get_text(strip=True)
                                if party_name and party_name not in seen_parties:
                                    party_id = f"party_{self._sanitize_id(party_name)}"
                                    party = Party(
                                        id=party_id,
                                        name=party_name,
                                        short_name=party_name,
                                        color=self._get_party_color(party_name),
                                    )
                                    parties.append(party)
                                    seen_parties[party_name] = party

            except Exception as e:
                print(f"Error scraping parties: {e}")

        return parties

    def scrape_laws(self, limit: int = 100) -> tuple[List[Law], List[dict]]:
        """Scrape legislative projects from Senate API."""
        import xml.etree.ElementTree as ET
        from datetime import datetime, timedelta
        from models import Authorship

        laws = []
        authorships = []
        print(f"Scraping up to {limit} laws from Senate API...")

        try:
            base_api_url = "https://tramitacion.senado.cl/wspublico/tramitacion.php"

            seen_boletines = set()
            current_date = datetime.now()
            days_checked = 0

            while len(laws) < limit and days_checked < 30:
                date_str = current_date.strftime("%d/%m/%Y")
                url = f"{base_api_url}?fecha={date_str}"

                print(f"Fetching laws from {date_str}...")
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)

                if response.status_code == 200:
                    root = ET.fromstring(response.content)
                    proyectos = root.findall(".//proyecto")

                    for proj in proyectos:
                        try:
                            desc = proj.find("descripcion")
                            if desc is None:
                                continue

                            boletin = desc.find("boletin")
                            if boletin is None or boletin.text is None:
                                continue

                            boletin_text = boletin.text.strip()

                            if boletin_text in seen_boletines:
                                continue
                            seen_boletines.add(boletin_text)

                            titulo_elem = desc.find("titulo")
                            titulo = (
                                titulo_elem.text.strip()
                                if titulo_elem is not None and titulo_elem.text
                                else ""
                            )

                            fecha_elem = desc.find("fecha_ingreso")
                            fecha_ingreso = (
                                fecha_elem.text.strip()
                                if fecha_elem is not None and fecha_elem.text
                                else ""
                            )

                            estado_elem = desc.find("estado")
                            estado = (
                                estado_elem.text.strip()
                                if estado_elem is not None and estado_elem.text
                                else ""
                            )

                            materias = []
                            materias_elem = proj.find(".//materias")
                            if materias_elem is not None:
                                for materia in materias_elem.findall("materia"):
                                    desc_materia = materia.find("DESCRIPCION")
                                    if desc_materia is not None and desc_materia.text:
                                        materias.append(desc_materia.text.strip())

                            law_id = f"law_{self._sanitize_id(boletin_text)}"
                            law = Law(
                                id=law_id,
                                boletin=boletin_text,
                                title=titulo,
                                description=" | ".join(materias) if materias else "",
                                date_proposed=fecha_ingreso,
                                status=self._normalize_status(estado),
                                topic=materias[0] if materias else None,
                            )
                            laws.append(law)

                            authors_elem = proj.find(".//autores")
                            if authors_elem is not None:
                                for idx, autor in enumerate(
                                    authors_elem.findall("autor")
                                ):
                                    parl = autor.find("PARLAMENTARIO")
                                    if parl is not None and parl.text:
                                        senator_name = parl.text.strip()
                                        senator_id = (
                                            f"senator_{self._sanitize_id(senator_name)}"
                                        )
                                        authorships.append(
                                            {
                                                "senator_id": senator_id,
                                                "senator_name": senator_name,
                                                "law_id": law_id,
                                                "role": "principal"
                                                if idx == 0
                                                else "co_sponsor",
                                                "date": fecha_ingreso,
                                            }
                                        )

                            if len(laws) >= limit:
                                break

                        except Exception as e:
                            print(f"Error parsing law: {e}")
                            continue

                time.sleep(REQUEST_DELAY)
                current_date -= timedelta(days=1)
                days_checked += 1

        except Exception as e:
            print(f"Error scraping laws: {e}")

        print(f"Found {len(laws)} laws with {len(authorships)} authorships")
        return laws, authorships

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
        """Get color for a party."""
        # Map known Chilean parties to their colors
        color_map = {
            "R.N.": "#0054a6",
            "PS": "#e4002b",
            "P.S.": "#e4002b",
            "UDI": "#1a237e",
            "U.D.I.": "#1a237e",
            "PDC": "#0066cc",
            "P.D.C.": "#0066cc",
            "PPD": "#ff6600",
            "P.P.D.": "#ff6600",
            "Evópoli": "#ffc107",
            "P.C": "#d32f2f",
            "Social Cristiano": "#7b1fa2",
            "Demócratas": "#1976d2",
            "Revolución Democrática": "#388e3c",
            "F.R.E.V.S.": "#f57c00",
            "Independiente": "#757575",
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

    # Scrape senators first (we'll extract parties from them)
    print("Scraping senators...")
    senators = scraper.scrape_senators()
    print(f"Found {len(senators)} senators")

    # Extract parties from senators
    print("Extracting parties from senators...")
    parties = scraper.scrape_parties(senators)
    print(f"Found {len(parties)} parties")

    # Scrape laws
    print("Scraping laws...")
    laws, authorships = scraper.scrape_laws(limit=50)
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

    with open(f"{data_dir}/authorships.json", "w", encoding="utf-8") as f:
        json.dump(authorships, f, ensure_ascii=False, indent=2)

    print("Scraping complete! Data saved to data/ directory")


if __name__ == "__main__":
    main()
