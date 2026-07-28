"""Season-label helpers for FootballIQ. European football seasons run
August through May, so a season is labelled by its start year and end year
(e.g. '2024-25' runs Aug 2024 - May 2025). All functions here convert between
that label and actual calendar dates.
"""

from datetime import date
from typing import Tuple

# The month a new season is considered to start. Matches from August 1st
# onward belong to the season starting that year.
SEASON_START_MONTH = 8
SEASON_END_MONTH = 5
SEASON_END_DAY = 31


def parse_season_label(season_label: str) -> Tuple[int, int]:
    """Convert a season label like '2024-25' into (start_year, end_year) as ints.

    '2024-25' -> (2024, 2025)
    """
    if "-" not in season_label:
        raise ValueError(f"Invalid season label '{season_label}', expected format 'YYYY-YY'")

    start_str, end_suffix = season_label.split("-")

    if len(start_str) != 4 or not start_str.isdigit():
        raise ValueError(f"Invalid season label '{season_label}', start year must be 4 digits")
    if len(end_suffix) != 2 or not end_suffix.isdigit():
        raise ValueError(f"Invalid season label '{season_label}', end suffix must be 2 digits")

    start_year = int(start_str)
    end_year = (start_year // 100) * 100 + int(end_suffix)

    # Handle century rollover, e.g. '2099-00' -> end_year should be 2100, not 2000
    if end_year <= start_year:
        end_year += 100

    return start_year, end_year


def match_date_to_season(match_date_str: str) -> str:
    """Given a match date string 'YYYY-MM-DD', return the season label it
    belongs to, e.g. '2024-11-30' -> '2024-25', '2025-03-15' -> '2024-25'.
    """
    parsed = date.fromisoformat(match_date_str)

    if parsed.month >= SEASON_START_MONTH:
        start_year = parsed.year
    else:
        start_year = parsed.year - 1

    end_year = start_year + 1
    return f"{start_year}-{str(end_year)[-2:]}"


def season_date_range(season_label: str) -> Tuple[date, date]:
    """Given a season label like '2024-25', return (season_start_date, season_end_date).

    '2024-25' -> (date(2024, 8, 1), date(2025, 5, 31))
    """
    start_year, end_year = parse_season_label(season_label)
    start = date(start_year, SEASON_START_MONTH, 1)
    end = date(end_year, SEASON_END_MONTH, SEASON_END_DAY)
    return start, end