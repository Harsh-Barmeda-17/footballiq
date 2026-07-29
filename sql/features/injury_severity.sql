-- Injury severity score per team per matchweek:
--   SUM(injured_player_market_value) / SUM(total_squad_market_value)
--
-- BLOCKED: no injury or player market value data loaded yet — this arrives
-- Week 5 (Transfermarkt ingestion) and Week 6 (fact_injuries, dim_players
-- with market_value_eur). This is a stub showing the intended shape.

-- SELECT
--     team_id,
--     matchweek,
--     SUM(player_market_value_eur) FILTER (WHERE is_injured) 
--         / NULLIF(SUM(player_market_value_eur), 0) AS injury_severity_score
-- FROM fact_player_match_performance
-- JOIN dim_players USING (player_id)
-- GROUP BY team_id, matchweek;

-- Placeholder query against current data, just to keep the file runnable:
SELECT
    team,
    match_date,
    0.0 AS injury_severity_score  -- placeholder until real data exists
FROM team_match_results
LIMIT 5;