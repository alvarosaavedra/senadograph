"""Data models for scraped entities."""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Senator:
    """Represents a Chilean Senator."""

    id: str
    name: str
    name_en: Optional[str] = None
    party: str = ""
    region: str = ""
    region_en: Optional[str] = None
    email: Optional[str] = None
    photo_url: Optional[str] = None
    biography: Optional[str] = None
    biography_en: Optional[str] = None
    start_date: Optional[str] = None
    active: bool = True

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "nameEn": self.name_en,
            "party": self.party,
            "region": self.region,
            "regionEn": self.region_en,
            "email": self.email,
            "photoUrl": self.photo_url,
            "biography": self.biography,
            "biographyEn": self.biography_en,
            "startDate": self.start_date,
            "active": self.active,
        }


@dataclass
class Party:
    """Represents a political party."""

    id: str
    name: str
    name_en: Optional[str] = None
    short_name: str = ""
    color: str = "#cccccc"
    ideology: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "nameEn": self.name_en,
            "shortName": self.short_name,
            "color": self.color,
            "ideology": self.ideology,
        }


@dataclass
class Law:
    """Represents a legislative project (law)."""

    id: str
    boletin: str
    title: str
    title_en: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None
    date_proposed: str = ""
    status: str = "in_discussion"
    topic: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "boletin": self.boletin,
            "title": self.title,
            "titleEn": self.title_en,
            "description": self.description,
            "descriptionEn": self.description_en,
            "dateProposed": self.date_proposed,
            "status": self.status,
            "topic": self.topic,
        }


@dataclass
class Committee:
    """Represents a senate committee."""

    id: str
    name: str
    name_en: Optional[str] = None

    def to_dict(self):
        return {"id": self.id, "name": self.name, "nameEn": self.name_en}


@dataclass
class Vote:
    """Represents a voting session."""

    id: str
    date: str
    session: str
    result: str

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "session": self.session,
            "result": self.result,
        }


@dataclass
class Lobbyist:
    """Represents a lobbyist entity."""

    id: str
    name: str
    type: str  # company, union, ngo, professional_college
    industry: Optional[str] = None
    industry_en: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "industry": self.industry,
            "industryEn": self.industry_en,
        }


@dataclass
class CommitteeMembership:
    """Represents a senator's committee membership."""

    senator_id: str
    committee_id: str
    role: str  # member, president, vice_president


@dataclass
class Authorship:
    """Represents a law authorship relationship."""

    senator_id: str
    law_id: str
    role: str  # principal, co_sponsor
    date: Optional[str] = None


@dataclass
class VotingRecord:
    """Represents a senator's vote."""

    senator_id: str
    vote_id: str
    vote: str  # favor, against, abstained, absent
    date: str


@dataclass
class LobbyMeeting:
    """Represents a meeting between senator and lobbyist."""

    senator_id: str
    lobbyist_id: str
    date: str
    topic: Optional[str] = None
    senator_name: Optional[str] = None
    lobbyist_name: Optional[str] = None


@dataclass
class LobbyTrip:
    """Represents a trip financed by a lobbyist."""

    senator_id: str
    lobbyist_id: str
    destination: str
    purpose: str
    cost: int
    funded_by: str
    invited_by: str
    senator_name: Optional[str] = None
    lobbyist_name: Optional[str] = None


@dataclass
class LobbyDonation:
    """Represents a donation received by a senator."""

    senator_id: str
    lobbyist_id: str
    date: str
    occasion: str
    item: str
    donor: str
    senator_name: Optional[str] = None
    lobbyist_name: Optional[str] = None


@dataclass
class VotingSimilarity:
    """Represents voting similarity between two senators."""

    senator1_id: str
    senator2_id: str
    agreement: float


@dataclass
class CoSponsorship:
    """Represents co-sponsorship relationship between two senators."""

    senator1_id: str
    senator2_id: str
    law_id: str
