-- Head-to-head win rate in the last 5 meetings between two specific teams.
-- True self-join version (Week 6+, once fact_matches has team_id columns):
--
--   SELECT m1.*, m2.*
--   FROM fact_matches m1
--   JOIN fact_matches m2
--     ON (m1.home_team_id = m2.away_team_id AND m1.away_team_id = m2.home_team_id)
--    AND m1.match_id != m2.match_id
--
-- For now, with only team names available, a direct filter gives the same result:

SELECT
    match_date,
    home_team,
    away_team,
    home_goals,
    away_goals,
    result
FROM matches
WHERE (home_team = :team_a AND away_team = :team_b)
   OR (home_team = :team_b AND away_team = :team_a)
ORDER BY match_date DESC
LIMIT 5;

-- Usage example (replace :team_a / :team_b, or bind as params from Python):
-- WHERE (home_team = 'Barcelona' AND away_team = 'Real Madrid')
--    OR (home_team = 'Real Madrid' AND away_team = 'Barcelona')