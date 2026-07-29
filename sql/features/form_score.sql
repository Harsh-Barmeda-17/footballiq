-- Rolling 5-match form score (points), separate for home and away.
-- This is the query we already built and tested against team_match_results.

SELECT
    team,
    match_date,
    season,
    venue,
    points,
    SUM(points) OVER (
        PARTITION BY team, season, venue
        ORDER BY match_date
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ) AS form_score_last_5
FROM team_match_results
ORDER BY team, match_date;

-- NOTE: partitioning by venue here gives separate home-form and away-form,
-- per your build guide's "Home/away split — separate home and away rolling
-- stats (teams play differently at home)" requirement.