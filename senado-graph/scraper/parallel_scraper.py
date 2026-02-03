#!/usr/bin/env python3
"""
Parallel scraper runner - runs 3 scraper instances concurrently.
Each instance handles a different subset of data for faster scraping.
"""

import subprocess
import json
import os
from datetime import datetime
from typing import List, Dict
from concurrent.futures import ProcessPoolExecutor, as_completed
import sys


def scrape_senators_and_parties():
    """Task 1: Scrape senators and parties."""
    print("[Process 1] Starting senators and parties scraping...")
    try:
        from spider import SenateScraper

        scraper = SenateScraper()
        senators = scraper.scrape_senators()
        parties = scraper.scrape_parties(senators)

        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)

        # Save to temporary file
        with open(f"{data_dir}/senators_parties_temp.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "senators": [s.to_dict() for s in senators],
                    "parties": [p.to_dict() for p in parties],
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(f"[Process 1] Found {len(senators)} senators and {len(parties)} parties")
        return {"senators": len(senators), "parties": len(parties)}
    except Exception as e:
        print(f"[Process 1] Error: {e}")
        return {"error": str(e)}


def scrape_laws_and_votes():
    """Task 2: Scrape laws, authorships, and votes."""
    print("[Process 2] Starting laws and votes scraping...")
    try:
        from spider import SenateScraper

        scraper = SenateScraper()
        laws, authorships, votes = scraper.scrape_laws(days=30)

        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)

        with open(f"{data_dir}/laws_temp.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "laws": [l.to_dict() for l in laws],
                    "authorships": authorships,
                    "votes": votes,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(
            f"[Process 2] Found {len(laws)} laws, {len(authorships)} authorships, {len(votes)} votes"
        )
        return {"laws": len(laws), "authorships": len(authorships), "votes": len(votes)}
    except Exception as e:
        print(f"[Process 2] Error: {e}")
        return {"error": str(e)}


def scrape_lobby_data():
    """Task 3: Scrape lobbyists, meetings, trips, and donations."""
    print("[Process 3] Starting lobby data scraping...")
    try:
        from spider import SenateScraper

        scraper = SenateScraper()
        lobbyists, meetings = scraper.scrape_lobbyists(days=30)
        trips = scraper.scrape_trips(days=30)
        donations = scraper.scrape_donations(days=30)

        data_dir = os.path.join(os.path.dirname(__file__), "data")
        os.makedirs(data_dir, exist_ok=True)

        with open(f"{data_dir}/lobby_temp.json", "w", encoding="utf-8") as f:
            json.dump(
                {
                    "lobbyists": lobbyists,
                    "meetings": meetings,
                    "trips": trips,
                    "donations": donations,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(
            f"[Process 3] Found {len(lobbyists)} lobbyists, {len(meetings)} meetings, {len(trips)} trips, {len(donations)} donations"
        )
        return {
            "lobbyists": len(lobbyists),
            "meetings": len(meetings),
            "trips": len(trips),
            "donations": len(donations),
        }
    except Exception as e:
        print(f"[Process 3] Error: {e}")
        return {"error": str(e)}


def merge_temp_files():
    """Merge temporary files into final data files."""
    print("\n[Merging] Combining data from parallel processes...")
    data_dir = os.path.join(os.path.dirname(__file__), "data")

    try:
        # Load senators and parties
        if os.path.exists(f"{data_dir}/senators_parties_temp.json"):
            with open(
                f"{data_dir}/senators_parties_temp.json", "r", encoding="utf-8"
            ) as f:
                sp_data = json.load(f)

            with open(f"{data_dir}/senators.json", "w", encoding="utf-8") as f:
                json.dump(sp_data["senators"], f, ensure_ascii=False, indent=2)

            with open(f"{data_dir}/parties.json", "w", encoding="utf-8") as f:
                json.dump(sp_data["parties"], f, ensure_ascii=False, indent=2)

            os.remove(f"{data_dir}/senators_parties_temp.json")

        # Load laws, authorships, and votes
        if os.path.exists(f"{data_dir}/laws_temp.json"):
            with open(f"{data_dir}/laws_temp.json", "r", encoding="utf-8") as f:
                laws_data = json.load(f)

            with open(f"{data_dir}/laws.json", "w", encoding="utf-8") as f:
                json.dump(laws_data["laws"], f, ensure_ascii=False, indent=2)

            with open(f"{data_dir}/authorships.json", "w", encoding="utf-8") as f:
                json.dump(laws_data["authorships"], f, ensure_ascii=False, indent=2)

            with open(f"{data_dir}/votes.json", "w", encoding="utf-8") as f:
                json.dump(laws_data["votes"], f, ensure_ascii=False, indent=2)

            os.remove(f"{data_dir}/laws_temp.json")

        # Load lobby data
        if os.path.exists(f"{data_dir}/lobby_temp.json"):
            with open(f"{data_dir}/lobby_temp.json", "r", encoding="utf-8") as f:
                lobby_data = json.load(f)

            with open(f"{data_dir}/lobbyists.json", "w", encoding="utf-8") as f:
                json.dump(lobby_data["lobbyists"], f, ensure_ascii=False, indent=2)

            with open(f"{data_dir}/lobby_meetings.json", "w", encoding="utf-8") as f:
                json.dump(lobby_data["meetings"], f, ensure_ascii=False, indent=2)

            with open(f"{data_dir}/lobby_trips.json", "w", encoding="utf-8") as f:
                json.dump(lobby_data["trips"], f, ensure_ascii=False, indent=2)

            with open(f"{data_dir}/lobby_donations.json", "w", encoding="utf-8") as f:
                json.dump(lobby_data["donations"], f, ensure_ascii=False, indent=2)

            os.remove(f"{data_dir}/lobby_temp.json")

        print("[Merging] Data merged successfully!")
        return True
    except Exception as e:
        print(f"[Merging] Error: {e}")
        return False


def run_parallel_scrapers():
    """Run 3 scraper processes in parallel."""
    print("Starting parallel scraping with 3 processes...")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    start_time = datetime.now()

    # Run tasks in parallel
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(scrape_senators_and_parties): "Senators & Parties",
            executor.submit(scrape_laws_and_votes): "Laws & Votes",
            executor.submit(scrape_lobby_data): "Lobby Data",
        }

        results = {}
        for future in as_completed(futures):
            task_name = futures[future]
            try:
                result = future.result()
                results[task_name] = result
                print(f"\n✅ {task_name} completed: {result}")
            except Exception as e:
                print(f"\n❌ {task_name} failed: {e}")
                results[task_name] = {"error": str(e)}

    print("-" * 60)

    # Merge all data
    merge_temp_files()

    end_time = datetime.now()
    duration = end_time - start_time

    print(f"\nEnd time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total duration: {duration}")
    print("\nParallel scraping complete! Data saved to data/ directory")
    print("\nTo seed the database, run: python seed_neo4j.py")


if __name__ == "__main__":
    run_parallel_scrapers()
