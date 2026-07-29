"""Loads the La Liga 2024/25 Football-Data.co.uk CSV into the `matches` table.
Idempotent — safe to run multiple times, thanks to the UNIQUE constraint on
(match_date, home_team, away_team) plus an upsert (ON CONFLICT DO NOTHING).
"""

from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

from utils.logger import get_logger
from utils.config import load_config
from utils.date_utils import match_date_to_season

logger = get_logger(__name__)

CSV_PATH = Path("data/la_liga_2024_25.csv")


def parse_date(raw_date: str) -> str:
    """Football-Data.co.uk uses DD/MM/YYYY or DD/MM/YY. Returns ISO format string."""
    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(raw_date, fmt).date().isoformat()
        except ValueError:
            continue
    raise ValueError(f"Unrecognised date format: '{raw_date}'")


def load_matches():
    config = load_config()
    engine = create_engine(config.database_url)

    logger.info(f"Reading {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")

    # Keep only the columns we need, rename to match our table schema
    clean = df[["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]].copy()
    clean = clean.rename(columns={
        "Date": "match_date",
        "HomeTeam": "home_team",
        "AwayTeam": "away_team",
        "FTHG": "home_goals",
        "FTAG": "away_goals",
        "FTR": "result",
    })

    clean = clean.dropna(subset=["home_team", "away_team", "result"])
    clean["match_date"] = clean["match_date"].apply(parse_date)
    clean["season"] = clean["match_date"].apply(match_date_to_season)

    logger.info(f"Parsed {len(clean)} matches, loading into database")

    # Load into a staging table first, then upsert into `matches` to respect
    # the UNIQUE constraint and stay idempotent on reruns.
    with engine.begin() as conn:
        clean.to_sql("matches_staging", conn, if_exists="replace", index=False)

        result = conn.execute(text("""
            INSERT INTO matches (match_date, home_team, away_team, home_goals, away_goals, result, season)
            SELECT match_date::date, home_team, away_team, home_goals, away_goals, result, season
            FROM matches_staging
            ON CONFLICT (match_date, home_team, away_team) DO NOTHING
        """))

        conn.execute(text("DROP TABLE matches_staging"))

    logger.info(f"Load complete. Rows affected: {result.rowcount}")


if __name__ == "__main__":
    load_matches()