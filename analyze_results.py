"""Week 1 practice script — reads a Football-Data.co.uk CSV using only the
standard library, computes home/away win rates per team, and writes a
summary JSON. No pandas yet — that comes in Week 4.
"""

import csv
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict

from utils.logger import get_logger

logger = get_logger(__name__)

CSV_PATH = Path("data/la_liga_2024_25.csv")
OUTPUT_PATH = Path("data/summary.json")


@dataclass
class TeamRecord:
    """Tracks one team's home and away results across the season."""
    team: str
    home_played: int = 0
    home_wins: int = 0
    home_draws: int = 0
    home_losses: int = 0
    away_played: int = 0
    away_wins: int = 0
    away_draws: int = 0
    away_losses: int = 0

    @property
    def home_win_rate(self) -> float:
        return round(self.home_wins / self.home_played, 3) if self.home_played else 0.0

    @property
    def away_win_rate(self) -> float:
        return round(self.away_wins / self.away_played, 3) if self.away_played else 0.0

    def to_dict(self) -> dict:
        return {
            "team": self.team,
            "home_played": self.home_played,
            "home_wins": self.home_wins,
            "home_draws": self.home_draws,
            "home_losses": self.home_losses,
            "home_win_rate": self.home_win_rate,
            "away_played": self.away_played,
            "away_wins": self.away_wins,
            "away_draws": self.away_draws,
            "away_losses": self.away_losses,
            "away_win_rate": self.away_win_rate,
        }


class MatchResultsAnalyzer:
    """Reads a Football-Data.co.uk CSV and computes per-team win rates."""

    def __init__(self, csv_path: Path):
        self.csv_path = csv_path
        self.teams: Dict[str, TeamRecord] = {}

    def _get_or_create_team(self, name: str) -> TeamRecord:
        if name not in self.teams:
            self.teams[name] = TeamRecord(team=name)
        return self.teams[name]

    def _parse_date(self, raw_date: str) -> datetime:
        """Football-Data.co.uk uses DD/MM/YYYY (or DD/MM/YY in older files)."""
        for fmt in ("%d/%m/%Y", "%d/%m/%y"):
            try:
                return datetime.strptime(raw_date, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unrecognised date format: '{raw_date}'")

    def process(self) -> None:
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"CSV not found at {self.csv_path}. Download it from "
                f"football-data.co.uk and place it there first."
            )

        with open(self.csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            row_count = 0

            for row in reader:
                # Skip fully blank trailing rows some Football-Data CSVs have
                if not row.get("HomeTeam") or not row.get("AwayTeam"):
                    continue

                home_team = row["HomeTeam"].strip()
                away_team = row["AwayTeam"].strip()
                result = row["FTR"].strip()  # 'H', 'D', or 'A'

                try:
                    self._parse_date(row["Date"])
                except ValueError as e:
                    logger.warning(f"Skipping row with bad date: {e}")
                    continue

                home_record = self._get_or_create_team(home_team)
                away_record = self._get_or_create_team(away_team)

                home_record.home_played += 1
                away_record.away_played += 1

                if result == "H":
                    home_record.home_wins += 1
                    away_record.away_losses += 1
                elif result == "A":
                    away_record.away_wins += 1
                    home_record.home_losses += 1
                elif result == "D":
                    home_record.home_draws += 1
                    away_record.away_draws += 1
                else:
                    logger.warning(f"Unrecognised result '{result}' for {home_team} vs {away_team}")
                    continue

                row_count += 1

            logger.info(f"Processed {row_count} matches across {len(self.teams)} teams")

    def write_summary(self, output_path: Path) -> None:
        summary = {
            "teams": [record.to_dict() for record in sorted(self.teams.values(), key=lambda r: r.team)]
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        logger.info(f"Summary written to {output_path}")


def main():
    analyzer = MatchResultsAnalyzer(CSV_PATH)
    analyzer.process()
    analyzer.write_summary(OUTPUT_PATH)


if __name__ == "__main__":
    main()