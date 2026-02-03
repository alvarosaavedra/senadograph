#!/usr/bin/env python3
"""
Advanced parallel scraper for Chilean Senate data with two-level parallelization.

Level 1: Parallel Days - Scrape laws from multiple days concurrently
Level 2: Parallel Law Voting - Scrape voting data for all laws in parallel
"""

import requests
import xml.etree.ElementTree as ET
import re
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass
from threading import Lock
from tqdm import tqdm

from config import (
    BASE_URL,
    SENATORS_URL,
    LAWS_URL,
    LOBBY_LOBBYISTS_URL,
    LOBBY_TRIPS_URL,
    LOBBY_DONATIONS_URL,
    REQUEST_TIMEOUT,
    DATA_DIR,
)
from models import Senator, Party, Law


@dataclass
class ScrapingResult:
    """Container for scraping results."""

    laws: List[Law]
    authorships: List[Dict]
    votes: List[Dict]
    errors: List[str]


class AdvancedParallelScraper:
    """
    Advanced parallel scraper with two-level parallelization for Chilean Senate data.

    Level 1: Parallel Days - Scrape laws from multiple days concurrently
    Level 2: Parallel Law Voting - Scrape voting data for all laws in parallel
    """

    def __init__(self, max_workers: int = 5, days: int = 30):
        """
        Initialize the advanced parallel scraper.

        Args:
            max_workers: Number of concurrent threads for parallel operations
            days: Number of days to look back for data
        """
        self.max_workers = max_workers
        self.days = days
        self.base_api_url = "https://tramitacion.senado.cl/wspublico/tramitacion.php"

        # Create a session for connection pooling
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

        # Thread-safe lock for shared resources
        self._lock = Lock()

        # Statistics tracking
        self.stats = {
            "days_processed": 0,
            "days_failed": 0,
            "laws_found": 0,
            "laws_unique": 0,
            "votes_found": 0,
            "votes_failed": 0,
        }

    def _sanitize_id(self, text: str) -> str:
        """Sanitize text to create a valid ID."""
        sanitized = re.sub(r"[^\w\s-]", "", text.lower())
        sanitized = re.sub(r"[-\s]+", "_", sanitized)
        return sanitized[:50]

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

    def _get_api_response(self, url: str) -> Optional[bytes]:
        """Get API response content with retry logic."""
        max_retries = 3
        backoff = 1.0

        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                return response.content
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = min(backoff, 30.0)
                    time.sleep(wait_time)
                    backoff *= 2
                else:
                    return None
        return None

    def _scrape_single_day(
        self, date: datetime
    ) -> Tuple[List[Law], List[Dict], List[str]]:
        """
        Scrape laws from a single day.

        Args:
            date: Date to scrape

        Returns:
            Tuple of (laws, authorships, errors) for that day
        """
        laws = []
        authorships = []
        errors = []

        date_str = date.strftime("%d/%m/%Y")
        url = f"{self.base_api_url}?fecha={date_str}"

        try:
            response_content = self._get_api_response(url)

            if not response_content:
                errors.append(f"Failed to fetch data for {date_str}")
                return laws, authorships, errors

            root = ET.fromstring(response_content)
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

                    # Extract authorships
                    authors_elem = proj.find(".//autores")
                    if authors_elem is not None:
                        for idx, autor in enumerate(authors_elem.findall("autor")):
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

                except Exception as e:
                    errors.append(f"Error parsing law on {date_str}: {e}")
                    continue

        except Exception as e:
            errors.append(f"Error scraping day {date_str}: {e}")

        return laws, authorships, errors

    def scrape_laws_parallel(self) -> ScrapingResult:
        """
        Level 1: Scrape laws from multiple days in parallel.

        Uses ThreadPoolExecutor to query the Senate API for laws from each day
        concurrently. Collects all laws and removes duplicates.

        Returns:
            ScrapingResult containing laws, authorships, and any errors
        """
        print(f"\n[Level 1] Starting parallel law scraping for {self.days} days...")
        print(f"Using {self.max_workers} concurrent threads")

        # Generate list of dates to scrape
        dates = [datetime.now() - timedelta(days=i) for i in range(self.days)]

        all_laws = []
        all_authorships = []
        all_errors = []

        # Use ThreadPoolExecutor for parallel day scraping
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all day scraping tasks
            future_to_date = {
                executor.submit(self._scrape_single_day, date): date for date in dates
            }

            # Process results as they complete with progress bar
            with tqdm(total=len(dates), desc="Scraping days", unit="day") as pbar:
                for future in as_completed(future_to_date):
                    date = future_to_date[future]
                    try:
                        laws, authorships, errors = future.result()

                        with self._lock:
                            all_laws.extend(laws)
                            all_authorships.extend(authorships)
                            all_errors.extend(errors)
                            self.stats["days_processed"] += 1
                            self.stats["laws_found"] += len(laws)

                        if errors:
                            pbar.set_postfix({"errors": len(errors)})

                    except Exception as e:
                        with self._lock:
                            all_errors.append(
                                f"Failed to scrape {date.strftime('%d/%m/%Y')}: {e}"
                            )
                            self.stats["days_failed"] += 1

                    pbar.update(1)

        # Remove duplicate laws by boletin
        seen_boletines = set()
        unique_laws = []
        for law in all_laws:
            if law.boletin not in seen_boletines:
                seen_boletines.add(law.boletin)
                unique_laws.append(law)

        # Remove duplicate authorships
        seen_authorships = set()
        unique_authorships = []
        for auth in all_authorships:
            key = (auth["senator_id"], auth["law_id"])
            if key not in seen_authorships:
                seen_authorships.add(key)
                unique_authorships.append(auth)

        self.stats["laws_unique"] = len(unique_laws)

        print(f"\n[Level 1] Completed: {self.stats['days_processed']} days processed")
        print(f"  - {self.stats['days_failed']} days failed")
        print(f"  - {len(unique_laws)} unique laws found")
        print(f"  - {len(unique_authorships)} authorships")

        return ScrapingResult(
            laws=unique_laws,
            authorships=unique_authorships,
            votes=[],
            errors=all_errors,
        )

    def _scrape_law_votes(self, law: Law) -> Tuple[List[Dict], str]:
        """
        Scrape voting data for a single law.

        Args:
            law: Law object to scrape votes for

        Returns:
            Tuple of (votes list, law boletin for tracking)
        """
        votes = []
        boletin = law.boletin

        try:
            # Extract the numeric part from boletin
            boletin_number = boletin.split("-")[0]
            url = f"{self.base_api_url}?boletin={boletin_number}"

            response_content = self._get_api_response(url)
            if not response_content:
                return votes, boletin

            root = ET.fromstring(response_content)
            votaciones = root.findall(".//votaciones/votacion")

            for votacion in votaciones:
                try:
                    session = votacion.find("SESION")
                    fecha = votacion.find("FECHA")
                    tema = votacion.find("TEMA")

                    detalle = votacion.find("DETALLE_VOTACION")
                    if detalle is not None:
                        for voto in detalle.findall("VOTO"):
                            parlamentario = voto.find("PARLAMENTARIO")
                            seleccion = voto.find("SELECCION")

                            if parlamentario is not None and parlamentario.text:
                                vote_value = self._normalize_vote(
                                    seleccion.text if seleccion is not None else ""
                                )
                                votes.append(
                                    {
                                        "law_boletin": boletin,
                                        "law_id": law.id,
                                        "session": session.text
                                        if session is not None
                                        else "",
                                        "date": fecha.text if fecha is not None else "",
                                        "topic": tema.text if tema is not None else "",
                                        "senator_name": parlamentario.text.strip(),
                                        "senator_id": f"senator_{self._sanitize_id(parlamentario.text.strip())}",
                                        "vote": vote_value,
                                    }
                                )
                except Exception:
                    continue

        except Exception:
            pass

        return votes, boletin

    def _normalize_vote(self, vote: Optional[str]) -> str:
        """Normalize vote to standard values."""
        if not vote:
            return "absent"
        vote_lower = vote.lower()
        if vote_lower == "si":
            return "favor"
        elif vote_lower == "no":
            return "against"
        elif "abstenc" in vote_lower:
            return "abstained"
        elif "pareo" in vote_lower:
            return "paired"
        return "absent"

    def scrape_votes_parallel(self, laws: List[Law]) -> List[Dict]:
        """
        Level 2: Scrape voting data for all laws in parallel.

        Uses ThreadPoolExecutor to query each law's voting endpoint concurrently.

        Args:
            laws: List of Law objects to scrape votes for

        Returns:
            List of vote dictionaries
        """
        print(f"\n[Level 2] Starting parallel vote scraping for {len(laws)} laws...")
        print(f"Using {self.max_workers} concurrent threads")

        all_votes = []
        failed_laws = []

        # Use ThreadPoolExecutor for parallel vote scraping
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all vote scraping tasks
            future_to_law = {
                executor.submit(self._scrape_law_votes, law): law for law in laws
            }

            # Process results as they complete with progress bar
            with tqdm(total=len(laws), desc="Scraping votes", unit="law") as pbar:
                for future in as_completed(future_to_law):
                    law = future_to_law[future]
                    try:
                        votes, boletin = future.result()

                        with self._lock:
                            all_votes.extend(votes)
                            self.stats["votes_found"] += len(votes)

                        pbar.set_postfix({"votes": len(votes)})

                    except Exception as e:
                        with self._lock:
                            failed_laws.append(law.boletin)
                            self.stats["votes_failed"] += 1

                    pbar.update(1)

        print(f"\n[Level 2] Completed:")
        print(f"  - {len(all_votes)} total votes found")
        print(f"  - {len(failed_laws)} laws failed")

        return all_votes

    def scrape_senators(self) -> Tuple[List[Senator], List[Party]]:
        """
        Scrape senators (sequential - not much data).

        Returns:
            Tuple of (senators list, parties list)
        """
        print("\n[Sequential] Scraping senators...")

        senators = []

        try:
            response = self.session.get(SENATORS_URL, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            from bs4 import BeautifulSoup

            soup = BeautifulSoup(response.content, "html.parser")

            # Find rows with senator data
            all_rows = soup.find_all("tr")
            senator_rows = [
                r for r in all_rows if len(r.find_all("td", class_="clase_td")) >= 3
            ]

            for row in senator_rows:
                try:
                    tds = row.find_all("td", class_="clase_td")

                    if len(tds) < 3:
                        continue

                    info_td = None
                    party_td = None

                    for td in tds:
                        text = td.get_text()
                        if "Partido:" in text:
                            party_td = td
                        elif any(x in text for x in ["Región:", "Email:", "Teléfono:"]):
                            info_td = td

                    if not info_td or not party_td:
                        continue

                    # Extract name
                    name_text = info_td.get_text(strip=True)
                    name = name_text.split("Región:")[0].strip()

                    # Extract region
                    region_match = re.search(r"Región:\s*([^|]+)", info_td.get_text())
                    region = region_match.group(1).strip() if region_match else ""

                    # Extract email
                    email_elem = info_td.find("a", href=re.compile(r"mailto:"))
                    email = None
                    if email_elem and email_elem.get("href"):
                        email = str(email_elem["href"]).replace("mailto:", "")

                    # Extract party
                    party_elem = party_td.find("strong")
                    party = party_elem.get_text(strip=True) if party_elem else ""

                    senator_id = self._sanitize_id(name)

                    senator = Senator(
                        id=senator_id,
                        name=name,
                        party=party,
                        region=region,
                        email=email,
                        photo_url=None,
                        biography=None,
                        active=True,
                    )

                    senators.append(senator)

                except Exception as e:
                    print(f"Error parsing senator: {e}")
                    continue

        except Exception as e:
            print(f"Error scraping senators: {e}")

        # Extract parties from senators
        parties = self._extract_parties(senators)

        print(f"  - {len(senators)} senators found")
        print(f"  - {len(parties)} parties found")

        return senators, parties

    def _extract_parties(self, senators: List[Senator]) -> List[Party]:
        """Extract unique parties from senator data."""
        parties = []
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

        return parties

    def _get_party_color(self, party_name: str) -> str:
        """Get color for a party."""
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

    def scrape_lobby_parallel(self) -> Dict[str, List[Dict]]:
        """
        Scrape lobby data in parallel where possible.

        Returns:
            Dictionary with lobbyists, meetings, trips, and donations
        """
        print("\n[Parallel] Scraping lobby data...")

        result = {
            "lobbyists": [],
            "meetings": [],
            "trips": [],
            "donations": [],
        }

        # Scrape lobbyists and meetings
        try:
            response = self.session.get(LOBBY_LOBBYISTS_URL, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            from bs4 import BeautifulSoup

            soup = BeautifulSoup(response.content, "html.parser")

            tables = soup.find_all("table", class_="table-result")

            for table in tables:
                try:
                    thead = table.find("thead")
                    if not thead:
                        continue

                    tbody = table.find("tbody")
                    if not tbody:
                        continue

                    rows = tbody.find_all("tr")

                    for row in rows:
                        tds = row.find_all("td")
                        if len(tds) < 4:
                            continue

                        name = tds[0].get_text(strip=True)
                        date = tds[1].get_text(strip=True)
                        origin = tds[2].get_text(strip=True)
                        activity = tds[3].get_text(strip=True)

                        lobbyist_id = f"lobbyist_{self._sanitize_id(name)}"

                        lobbyist = {
                            "id": lobbyist_id,
                            "name": name,
                            "type": "organization",
                            "industry": self._extract_industry(activity),
                            "registration_date": date,
                            "origin": origin,
                        }

                        result["lobbyists"].append(lobbyist)

                        if "Reunión realizada" in origin:
                            meeting = self._parse_meeting_from_origin(
                                lobbyist_id, origin, date, activity
                            )
                            if meeting:
                                result["meetings"].append(meeting)

                except Exception as e:
                    print(f"Error parsing lobbyist table: {e}")

        except Exception as e:
            print(f"Error scraping lobbyists: {e}")

        # Scrape trips
        try:
            result["trips"] = self._scrape_trips()
        except Exception as e:
            print(f"Error scraping trips: {e}")

        # Scrape donations
        try:
            result["donations"] = self._scrape_donations()
        except Exception as e:
            print(f"Error scraping donations: {e}")

        print(f"  - {len(result['lobbyists'])} lobbyists found")
        print(f"  - {len(result['meetings'])} meetings found")
        print(f"  - {len(result['trips'])} trips found")
        print(f"  - {len(result['donations'])} donations found")

        return result

    def _scrape_trips(self) -> List[Dict]:
        """Scrape lobbyist-funded trips."""
        trips = []

        try:
            response = self.session.get(LOBBY_TRIPS_URL, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            from bs4 import BeautifulSoup

            soup = BeautifulSoup(response.content, "html.parser")

            table = soup.find("table", class_="table-result")
            if not table:
                return trips

            tbody = table.find("tbody")
            if not tbody:
                return trips

            rows = tbody.find_all("tr")

            for row in rows:
                tds = row.find_all("td")
                if len(tds) < 6:
                    continue

                senator_name = tds[0].get_text(strip=True)
                destination = tds[1].get_text(strip=True)
                purpose = tds[2].get_text(strip=True)
                cost_text = tds[3].get_text(strip=True)
                funded_by = tds[4].get_text(strip=True)
                invited_by = tds[5].get_text(strip=True)

                cost = self._parse_cost(cost_text)
                senator_id = f"senator_{self._sanitize_id(senator_name)}"
                lobbyist_id = f"lobbyist_{self._sanitize_id(funded_by)}"

                trips.append(
                    {
                        "senator_id": senator_id,
                        "lobbyist_id": lobbyist_id,
                        "senator_name": senator_name,
                        "lobbyist_name": funded_by,
                        "destination": destination,
                        "purpose": purpose,
                        "cost": cost,
                        "funded_by": funded_by,
                        "invited_by": invited_by,
                    }
                )

        except Exception as e:
            print(f"Error parsing trips: {e}")

        return trips

    def _scrape_donations(self) -> List[Dict]:
        """Scrape donations received by senators."""
        donations = []

        try:
            response = self.session.get(LOBBY_DONATIONS_URL, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            from bs4 import BeautifulSoup

            soup = BeautifulSoup(response.content, "html.parser")

            table = soup.find("table", class_="table-result")
            if not table:
                return donations

            tbody = table.find("tbody")
            if not tbody:
                return donations

            rows = tbody.find_all("tr")

            for row in rows:
                tds = row.find_all("td")
                if len(tds) < 5:
                    continue

                senator_name = tds[0].get_text(strip=True)
                date = tds[1].get_text(strip=True)
                occasion = tds[2].get_text(strip=True)
                item = tds[3].get_text(strip=True)
                donor = tds[4].get_text(strip=True)

                senator_id = f"senator_{self._sanitize_id(senator_name)}"
                lobbyist_id = f"lobbyist_{self._sanitize_id(donor)}"

                donations.append(
                    {
                        "senator_id": senator_id,
                        "lobbyist_id": lobbyist_id,
                        "senator_name": senator_name,
                        "lobbyist_name": donor,
                        "date": date,
                        "occasion": occasion,
                        "item": item,
                        "donor": donor,
                    }
                )

        except Exception as e:
            print(f"Error parsing donations: {e}")

        return donations

    def _parse_meeting_from_origin(
        self, lobbyist_id: str, origin: str, date: str, activity: str
    ) -> Optional[Dict]:
        """Extract meeting details from origin text."""
        match = re.search(
            r"Reunión realizada el (\d{4}-\d{2}-\d{2}) con ([^)]+)", origin
        )
        if match:
            meeting_date = match.group(1)
            senator_name = match.group(2).strip()
            senator_id = f"senator_{self._sanitize_id(senator_name)}"

            return {
                "senator_id": senator_id,
                "lobbyist_id": lobbyist_id,
                "senator_name": senator_name,
                "lobbyist_name": lobbyist_id.replace("lobbyist_", "").replace("_", " "),
                "date": meeting_date,
                "topic": activity,
            }

        return None

    def _extract_industry(self, activity: str) -> str:
        """Extract industry/sector from activity description."""
        activity_lower = activity.lower()

        industry_keywords = {
            "mining": ["minería", "cobre", "minera", "litio"],
            "energy": ["energía", "renovable", "hidrógeno", "eléctrica"],
            "fishing": ["pesca", "acuicultura", "salmon", "mar"],
            "agriculture": ["agrícola", "agricultura", "fruta", "viña", "vino"],
            "education": ["educación", "universidad", "escuela"],
            "health": ["salud", "farmacéutica", "médico"],
            "finance": ["banca", "financiero", "bancario", "seguro"],
            "technology": ["tecnología", "digital", "software"],
            "environment": ["medio ambiente", "ambiental", "agua"],
            "construction": ["construcción", "inmobiliario", "vivienda"],
            "transport": ["transporte", "aéreo", "ferrocarril"],
            "labor": ["trabajo", "laboral", "sindical"],
            "justice": ["justicia", "legal", "ley"],
        }

        for industry, keywords in industry_keywords.items():
            if any(keyword in activity_lower for keyword in keywords):
                return industry

        return "other"

    def _parse_cost(self, cost_text: str) -> int:
        """Parse cost string to integer (in CLP)."""
        try:
            cleaned = cost_text.replace(".", "").replace(",", "").strip()
            if cleaned:
                return int(cleaned)
        except (ValueError, AttributeError):
            pass
        return 0

    def _save_data(self, data: Dict[str, Any]) -> None:
        """Save all scraped data to JSON files."""
        os.makedirs(DATA_DIR, exist_ok=True)

        # Save senators
        if "senators" in data:
            with open(f"{DATA_DIR}/senators.json", "w", encoding="utf-8") as f:
                json.dump(
                    [s.to_dict() for s in data["senators"]],
                    f,
                    ensure_ascii=False,
                    indent=2,
                )

        # Save parties
        if "parties" in data:
            with open(f"{DATA_DIR}/parties.json", "w", encoding="utf-8") as f:
                json.dump(
                    [p.to_dict() for p in data["parties"]],
                    f,
                    ensure_ascii=False,
                    indent=2,
                )

        # Save laws
        if "laws" in data:
            with open(f"{DATA_DIR}/laws.json", "w", encoding="utf-8") as f:
                json.dump(
                    [l.to_dict() for l in data["laws"]], f, ensure_ascii=False, indent=2
                )

        # Save authorships
        if "authorships" in data:
            with open(f"{DATA_DIR}/authorships.json", "w", encoding="utf-8") as f:
                json.dump(data["authorships"], f, ensure_ascii=False, indent=2)

        # Save votes
        if "votes" in data:
            with open(f"{DATA_DIR}/votes.json", "w", encoding="utf-8") as f:
                json.dump(data["votes"], f, ensure_ascii=False, indent=2)

        # Save lobby data
        if "lobby" in data:
            lobby = data["lobby"]

            with open(f"{DATA_DIR}/lobbyists.json", "w", encoding="utf-8") as f:
                json.dump(lobby.get("lobbyists", []), f, ensure_ascii=False, indent=2)

            with open(f"{DATA_DIR}/lobby_meetings.json", "w", encoding="utf-8") as f:
                json.dump(lobby.get("meetings", []), f, ensure_ascii=False, indent=2)

            with open(f"{DATA_DIR}/lobby_trips.json", "w", encoding="utf-8") as f:
                json.dump(lobby.get("trips", []), f, ensure_ascii=False, indent=2)

            with open(f"{DATA_DIR}/lobby_donations.json", "w", encoding="utf-8") as f:
                json.dump(lobby.get("donations", []), f, ensure_ascii=False, indent=2)

        print(f"\nAll data saved to {DATA_DIR}/")

    def run(self) -> Dict[str, Any]:
        """
        Orchestrate all scraping and save to files.

        Returns:
            Dictionary containing all scraped data
        """
        start_time = time.time()

        print("=" * 70)
        print("Advanced Parallel Senate Scraper")
        print("=" * 70)
        print(f"Configuration:")
        print(f"  - Days to scrape: {self.days}")
        print(f"  - Max workers: {self.max_workers}")
        print(f"  - Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        # Step 1: Scrape senators and parties (sequential)
        senators, parties = self.scrape_senators()

        # Step 2: Scrape laws in parallel (Level 1)
        law_result = self.scrape_laws_parallel()
        laws = law_result.laws
        authorships = law_result.authorships

        # Step 3: Scrape votes in parallel (Level 2)
        votes = self.scrape_votes_parallel(laws)

        # Step 4: Scrape lobby data
        lobby_data = self.scrape_lobby_parallel()

        # Compile final results
        results = {
            "senators": senators,
            "parties": parties,
            "laws": laws,
            "authorships": authorships,
            "votes": votes,
            "lobby": lobby_data,
        }

        # Save to files
        self._save_data(results)

        # Print summary
        elapsed = time.time() - start_time

        print("\n" + "=" * 70)
        print("SCRAPING SUMMARY")
        print("=" * 70)
        print(f"Timing:")
        print(f"  - Total duration: {elapsed:.2f} seconds ({elapsed / 60:.2f} minutes)")
        print(f"\nSenators & Parties:")
        print(f"  - {len(senators)} senators")
        print(f"  - {len(parties)} parties")
        print(f"\nLaws (Two-Level Parallel):")
        print(
            f"  - Level 1: {self.stats['days_processed']} days processed, {self.stats['days_failed']} failed"
        )
        print(f"  - Laws: {len(laws)} unique")
        print(f"  - Authorships: {len(authorships)}")
        print(f"  - Level 2: {len(votes)} votes from {len(laws)} laws")
        print(f"\nLobby Data:")
        print(f"  - {len(lobby_data['lobbyists'])} lobbyists")
        print(f"  - {len(lobby_data['meetings'])} meetings")
        print(f"  - {len(lobby_data['trips'])} trips")
        print(f"  - {len(lobby_data['donations'])} donations")
        print(f"\nFiles saved to: {DATA_DIR}/")
        print("=" * 70)

        return results


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Advanced Parallel Scraper for Chilean Senate Data"
    )
    parser.add_argument(
        "--days", type=int, default=30, help="Number of days to scrape (default: 30)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        help="Number of concurrent workers (default: 5)",
    )

    args = parser.parse_args()

    scraper = AdvancedParallelScraper(max_workers=args.workers, days=args.days)
    scraper.run()


if __name__ == "__main__":
    main()
