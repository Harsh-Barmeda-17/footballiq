-- Rolling 5-match xG per team, split by home/away.
-- NOTE: xG data isn't loaded yet (arrives Week 5 from Understat/FBref).
-- Using goals_for as a stand-in for now — swap to actual xG column once
-- fact_matches has home_xg/away_xg populated.

SELECT
    home_team AS team,
    match_date,
    season,
    AVG(home_goals) OVER (
        PARTITION BY home_team, season
        ORDER BY match_date
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ) AS rolling_xg_last_5_home
FROM matches
ORDER BY home_team, match_date;

-- TODO (Week 5+): replace home_goals with home_xg once ingestion is built.
-- TODO (Week 6): this becomes AVG(home_xg) OVER (PARTITION BY home_team_id, season_id ...)
--                against fact_matches, per your build guide's exact spec.