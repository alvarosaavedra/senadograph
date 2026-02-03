"""Web scraper for Chilean Senate data."""

import requests
import time
import re
from bs4 import BeautifulSoup
from typing import List, Optional, Any
from urllib.parse import urljoin

from config import (
    BASE_URL,
    SENATORS_URL,
    LAWS_URL,
    LOBBY_URL,
    LOBBY_LOBBYISTS_URL,
    LOBBY_TRIPS_URL,
    LOBBY_DONATIONS_URL,
    REQUEST_TIMEOUT,
    REQUEST_DELAY,
    MAX_RETRIES,
    INITIAL_BACKOFF,
    MAX_BACKOFF,
    IMAGES_DIR,
)
from models import (
    Senator,
    Party,
    Law,
    Committee,
    LobbyMeeting,
    LobbyTrip,
    LobbyDonation,
)


class SenateScraper:
    """Scraper for Chilean Senate website."""

    def __init__(
        self,
        max_retries: int = 5,
        initial_backoff: float = 1.0,
        max_backoff: float = 60.0,
    ):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.max_backoff = max_backoff

    def _is_within_days(self, date_str: str, days: int = 30) -> bool:
        """Check if a date string is within the last N days from today.

        Args:
            date_str: Date string in various formats (DD/MM/YYYY, YYYY-MM-DD, etc.)
            days: Number of days to look back (default 30)

        Returns:
            True if date is within the last N days, False if older or parsing fails
        """
        from datetime import datetime, timedelta

        if not date_str or not date_str.strip():
            return True  # Include if no date provided

        date_str = date_str.strip()
        parsed_date = None

        # Try various date formats
        formats_to_try = [
            "%d/%m/%Y",  # DD/MM/YYYY
            "%Y-%m-%d",  # YYYY-MM-DD
            "%d-%m-%Y",  # DD-MM-YYYY
            "%d.%m.%Y",  # DD.MM.YYYY
            "%m/%d/%Y",  # MM/DD/YYYY
            "%Y/%m/%d",  # YYYY/MM/DD
        ]

        for fmt in formats_to_try:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue

        # If none of the formats worked, try extracting date with regex
        if parsed_date is None:
            import re

            # Try to find date patterns like 25/01/2024 or 2024-01-25
            patterns = [
                r"(\d{2})[/-](\d{2})[/-](\d{4})",  # DD/MM/YYYY or DD-MM-YYYY
                r"(\d{4})[/-](\d{2})[/-](\d{2})",  # YYYY-MM-DD or YYYY/MM/DD
            ]
            for pattern in patterns:
                match = re.search(pattern, date_str)
                if match:
                    try:
                        if len(match.group(3)) == 4:  # DD/MM/YYYY
                            parsed_date = datetime(
                                int(match.group(3)),
                                int(match.group(2)),
                                int(match.group(1)),
                            )
                        else:  # YYYY/MM/DD
                            parsed_date = datetime(
                                int(match.group(1)),
                                int(match.group(2)),
                                int(match.group(3)),
                            )
                        break
                    except ValueError:
                        continue

        # If we still couldn't parse, include the data by default
        if parsed_date is None:
            return True

        # Calculate the cutoff date
        cutoff_date = datetime.now() - timedelta(days=days)

        # Return True if date is within range (not older than cutoff)
        return parsed_date >= cutoff_date

    def _get(self, url: str) -> Optional[BeautifulSoup]:
        """Make a GET request and return BeautifulSoup object."""
        return self._get_with_retry(url, return_json=False)

    def _get_with_retry(self, url: str, return_json: bool = False) -> Optional[Any]:
        """Make a GET request with exponential backoff retry."""
        from typing import Any

        attempt = 0
        backoff = self.initial_backoff

        while attempt < self.max_retries:
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()

                if return_json:
                    return response.content

                time.sleep(REQUEST_DELAY)
                return BeautifulSoup(response.content, "html.parser")

            except requests.exceptions.Timeout as e:
                attempt += 1
                if attempt >= self.max_retries:
                    print(
                        f"Error: Max retries ({self.max_retries}) exceeded for {url}: {e}"
                    )
                    return None

                wait_time = min(backoff, self.max_backoff)
                print(
                    f"Timeout on attempt {attempt}/{self.max_retries} for {url}. "
                    f"Retrying in {wait_time:.1f}s..."
                )
                time.sleep(wait_time)
                backoff *= 2

            except requests.exceptions.RequestException as e:
                attempt += 1
                if attempt >= self.max_retries:
                    print(f"Error fetching {url}: {e}")
                    return None

                wait_time = min(backoff, self.max_backoff)
                print(
                    f"Request failed (attempt {attempt}/{self.max_retries}) for {url}: {e}. "
                    f"Retrying in {wait_time:.1f}s..."
                )
                time.sleep(wait_time)
                backoff *= 2

        return None

    def _get_api_response(self, url: str) -> Optional[bytes]:
        """Get API response content with retry logic."""
        attempt = 0
        backoff = self.initial_backoff

        while attempt < self.max_retries:
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                time.sleep(REQUEST_DELAY)
                return response.content

            except requests.exceptions.Timeout as e:
                attempt += 1
                if attempt >= self.max_retries:
                    print(
                        f"Error: Max retries ({self.max_retries}) exceeded for {url}: {e}"
                    )
                    return None

                wait_time = min(backoff, self.max_backoff)
                print(
                    f"API timeout on attempt {attempt}/{self.max_retries} for {url}. "
                    f"Retrying in {wait_time:.1f}s..."
                )
                time.sleep(wait_time)
                backoff *= 2

            except requests.exceptions.RequestException as e:
                attempt += 1
                if attempt >= self.max_retries:
                    print(f"Error fetching API {url}: {e}")
                    return None

                wait_time = min(backoff, self.max_backoff)
                print(
                    f"API request failed (attempt {attempt}/{self.max_retries}) for {url}: {e}. "
                    f"Retrying in {wait_time:.1f}s..."
                )
                time.sleep(wait_time)
                backoff *= 2

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

    def scrape_laws(
        self, limit: Optional[int] = None, days: int = 30
    ) -> tuple[List[Law], List[dict], List[dict]]:
        """Scrape legislative projects from Senate API."""
        import xml.etree.ElementTree as ET
        from datetime import datetime, timedelta
        from models import Authorship

        laws = []
        authorships = []
        if limit:
            print(f"Scraping up to {limit} laws from Senate API...")
        else:
            print(f"Scraping all laws from the last {days} days...")

        try:
            base_api_url = "https://tramitacion.senado.cl/wspublico/tramitacion.php"

            seen_boletines = set()
            current_date = datetime.now()
            days_checked = 0

            while (limit is None or len(laws) < limit) and days_checked < days:
                date_str = current_date.strftime("%d/%m/%Y")
                url = f"{base_api_url}?fecha={date_str}"

                print(f"Fetching laws from {date_str}...")
                response_content = self._get_api_response(url)

                if response_content:
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

                            if limit and len(laws) >= limit:
                                break

                        except Exception as e:
                            print(f"Error parsing law: {e}")
                            continue

                time.sleep(REQUEST_DELAY)
                current_date -= timedelta(days=1)
                days_checked += 1

        except Exception as e:
            print(f"Error scraping laws: {e}")

        # Scrape voting data for each law (optional, for laws that have votes)
        votes = []
        for law in laws[:20]:  # Limit to first 20 to avoid too many API calls
            print(f"Scraping voting data for {law.boletin}...")
            law_votes = self.scrape_law_voting(law.boletin)
            votes.extend(law_votes)

        print(
            f"Found {len(laws)} laws with {len(authorships)} authorships and {len(votes)} votes"
        )
        return laws, authorships, votes

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

    def scrape_law_voting(self, boletin: str) -> List[dict]:
        """Scrape voting data for a specific law by boletin number."""
        import xml.etree.ElementTree as ET

        # Extract the numeric part from boletin (e.g., "10795-33" -> "10795")
        boletin_number = boletin.split("-")[0]

        url = f"https://tramitacion.senado.cl/wspublico/tramitacion.php?boletin={boletin_number}"

        response_content = self._get_api_response(url)
        if not response_content:
            return []

        votes = []
        try:
            root = ET.fromstring(response_content)

            # Find all votaciones (voting sessions)
            votaciones = root.findall(".//votaciones/votacion")
            for votacion in votaciones:
                session = votacion.find("SESION")
                fecha = votacion.find("FECHA")
                tema = votacion.find("TEMA")

                detalle = votacion.find("DETALLE_VOTACION")
                if detalle is not None:
                    # Find individual senator votes
                    for voto in detalle.findall("VOTO"):
                        parlamentario = voto.find("PARLAMENTARIO")
                        seleccion = voto.find("SELECCION")

                        if parlamentario is not None and parlamentario.text:
                            votes.append(
                                {
                                    "law_boletin": boletin,
                                    "session": session.text
                                    if session is not None
                                    else "",
                                    "date": fecha.text if fecha is not None else "",
                                    "topic": tema.text if tema is not None else "",
                                    "senator_name": parlamentario.text,
                                    "vote": self._normalize_vote(
                                        seleccion.text if seleccion is not None else ""
                                    ),
                                }
                            )

        except Exception as e:
            print(f"Error parsing voting data for boletin {boletin}: {e}")

        return votes

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

    def scrape_lobbyists(
        self, years: Optional[List[int]] = None, days: int = 30
    ) -> tuple[List[dict], List[dict]]:
        """Scrape lobbyist registrations and meetings.

        Args:
            years: List of years to scrape (if None, only current year is used)
            days: Only include data from the last N days (default 30)
        """
        lobbyists = []
        meetings = []
        from datetime import datetime

        # Only use current year for date-based filtering
        current_year = datetime.now().year
        if years is None:
            years = [current_year]

        print(f"Scraping lobbyist data for years: {years}, last {days} days only...")

        for year in years:
            url = f"{LOBBY_LOBBYISTS_URL}&ano={year}"
            print(f"Fetching lobbyists from {year}...")

            soup = self._get(url)
            if not soup:
                continue

            try:
                tables = soup.find_all("table", class_="table-result")

                for table in tables:
                    thead = table.find("thead")
                    if not thead:
                        continue

                    headers = [th.get_text(strip=True) for th in thead.find_all("th")]

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

                        # Filter by registration date
                        if not self._is_within_days(date, days):
                            continue

                        lobbyist_id = f"lobbyist_{self._sanitize_id(name)}"

                        lobbyist = {
                            "id": lobbyist_id,
                            "name": name,
                            "type": "organization",
                            "industry": self._extract_industry(activity),
                            "registration_date": date,
                            "origin": origin,
                        }

                        lobbyists.append(lobbyist)

                        if "Reunión realizada" in origin:
                            meeting = self._parse_meeting_from_origin(
                                lobbyist_id, origin, date, activity
                            )
                            # Filter meetings by meeting date
                            if meeting and self._is_within_days(
                                meeting.get("date", ""), days
                            ):
                                meetings.append(meeting)

            except Exception as e:
                print(f"Error parsing lobbyist table for {year}: {e}")
                continue

            time.sleep(REQUEST_DELAY)

        print(
            f"Found {len(lobbyists)} lobbyists and {len(meetings)} meetings (last {days} days)"
        )
        return lobbyists, meetings

    def _parse_meeting_from_origin(
        self, lobbyist_id: str, origin: str, date: str, activity: str
    ) -> Optional[dict]:
        """Extract meeting details from origin text."""
        import re

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

    def scrape_trips(self, days: int = 30) -> List[dict]:
        """Scrape lobbyist-funded trips.

        Args:
            days: Only include trips from the last N days (default 30)
                  Note: The trips table may not have a date column visible.
                  If no date is found, trips are included by default.
        """
        trips = []

        print(f"Scraping lobbyist-funded trips (last {days} days)...")
        soup = self._get(LOBBY_TRIPS_URL)

        if not soup:
            return trips

        try:
            table = soup.find("table", class_="table-result")
            if not table:
                print("No trips table found")
                return trips

            # Check headers to find date column if it exists
            thead = table.find("thead")
            headers = []
            date_column_index = -1
            if thead:
                header_cells = thead.find_all("th")
                headers = [th.get_text(strip=True).lower() for th in header_cells]
                for idx, header in enumerate(headers):
                    if any(
                        keyword in header for keyword in ["fecha", "date", "ingreso"]
                    ):
                        date_column_index = idx
                        break

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

                # Check for date filtering if a date column was identified
                if date_column_index >= 0 and date_column_index < len(tds):
                    trip_date = tds[date_column_index].get_text(strip=True)
                    if trip_date and not self._is_within_days(trip_date, days):
                        continue

                cost = self._parse_cost(cost_text)
                senator_id = f"senator_{self._sanitize_id(senator_name)}"
                lobbyist_id = f"lobbyist_{self._sanitize_id(funded_by)}"

                trip = {
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

                trips.append(trip)

        except Exception as e:
            print(f"Error parsing trips table: {e}")

        print(f"Found {len(trips)} trips (last {days} days)")
        return trips

    def scrape_donations(self, days: int = 30) -> List[dict]:
        """Scrape donations received by senators.

        Args:
            days: Only include donations from the last N days (default 30)
        """
        donations = []

        print(f"Scraping donations (last {days} days)...")
        soup = self._get(LOBBY_DONATIONS_URL)

        if not soup:
            return donations

        try:
            table = soup.find("table", class_="table-result")
            if not table:
                print("No donations table found")
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

                # Filter by donation date
                if not self._is_within_days(date, days):
                    continue

                senator_id = f"senator_{self._sanitize_id(senator_name)}"
                lobbyist_id = f"lobbyist_{self._sanitize_id(donor)}"

                donation = {
                    "senator_id": senator_id,
                    "lobbyist_id": lobbyist_id,
                    "senator_name": senator_name,
                    "lobbyist_name": donor,
                    "date": date,
                    "occasion": occasion,
                    "item": item,
                    "donor": donor,
                }

                donations.append(donation)

        except Exception as e:
            print(f"Error parsing donations table: {e}")

        print(f"Found {len(donations)} donations (last {days} days)")
        return donations

    def _parse_cost(self, cost_text: str) -> int:
        """Parse cost string to integer (in CLP)."""
        try:
            cleaned = cost_text.replace(".", "").replace(",", "").strip()
            if cleaned:
                return int(cleaned)
        except (ValueError, AttributeError):
            pass
        return 0


def main():
    """Main scraping function."""
    print("Starting Senate scraper with exponential backoff retry...")
    print(
        f"Retry configuration: {MAX_RETRIES} max retries, "
        f"{INITIAL_BACKOFF}s initial backoff, {MAX_BACKOFF}s max backoff"
    )
    scraper = SenateScraper(
        max_retries=MAX_RETRIES,
        initial_backoff=INITIAL_BACKOFF,
        max_backoff=MAX_BACKOFF,
    )

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
    laws, authorships, votes = scraper.scrape_laws(days=30)
    print(f"Found {len(laws)} laws with {len(votes)} votes")

    # Scrape lobby data (last 30 days only)
    print("\nScraping lobby data...")
    lobbyists, meetings = scraper.scrape_lobbyists(days=30)
    trips = scraper.scrape_trips(days=30)
    donations = scraper.scrape_donations(days=30)

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

    with open(f"{data_dir}/votes.json", "w", encoding="utf-8") as f:
        json.dump(votes, f, ensure_ascii=False, indent=2)

    with open(f"{data_dir}/lobbyists.json", "w", encoding="utf-8") as f:
        json.dump(lobbyists, f, ensure_ascii=False, indent=2)

    with open(f"{data_dir}/lobby_meetings.json", "w", encoding="utf-8") as f:
        json.dump(meetings, f, ensure_ascii=False, indent=2)

    with open(f"{data_dir}/lobby_trips.json", "w", encoding="utf-8") as f:
        json.dump(trips, f, ensure_ascii=False, indent=2)

    with open(f"{data_dir}/lobby_donations.json", "w", encoding="utf-8") as f:
        json.dump(donations, f, ensure_ascii=False, indent=2)

    print("Scraping complete! Data saved to data/ directory")


if __name__ == "__main__":
    main()
