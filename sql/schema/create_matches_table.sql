-- Simple matches table for Week 2 SQL practice.
-- Full star schema (fact_matches, dim_teams, etc.) comes in Week 6.

CREATE TABLE IF NOT EXISTS matches (
    match_id SERIAL PRIMARY KEY,
    match_date DATE NOT NULL,
    home_team VARCHAR(100) NOT NULL,
    away_team VARCHAR(100) NOT NULL,
    home_goals INTEGER NOT NULL,
    away_goals INTEGER NOT NULL,
    result CHAR(1) NOT NULL CHECK (result IN ('H', 'D', 'A')),
    season VARCHAR(10) NOT NULL,
    UNIQUE (match_date, home_team, away_team)
);

CREATE INDEX IF NOT EXISTS idx_matches_home_team ON matches(home_team);
CREATE INDEX IF NOT EXISTS idx_matches_away_team ON matches(away_team);
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date);