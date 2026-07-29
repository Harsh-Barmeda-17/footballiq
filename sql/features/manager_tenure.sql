-- Manager tenure in days as of each match: EXTRACT(DAY FROM match_date - tenure_start_date)
-- BLOCKED: no dim_managers table yet — arrives Week 6.

-- SELECT
--     m.match_id,
--     m.match_date,
--     t.team_id,
--     EXTRACT(DAY FROM m.match_date - mgr.tenure_start_date) AS manager_tenure_days
-- FROM fact_matches m
-- JOIN dim_teams t ON m.home_team_id = t.team_id
-- JOIN dim_managers mgr ON mgr.team_id = t.team_id
--     AND m.match_date BETWEEN mgr.tenure_start_date AND COALESCE(mgr.tenure_end_date, m.match_date);

-- Placeholder, just to keep the file runnable:
SELECT
    home_team AS team,
    match_date,
    NULL::integer AS manager_tenure_days  -- placeholder until dim_managers exists
FROM matches
LIMIT 5;