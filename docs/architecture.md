# FootballIQ Architecture

_To be completed as the pipeline is built out._

## Data Flow

1. Ingestion — 5 sources (FBref, Understat, Football-Data.co.uk, StatsBomb, Transfermarkt)
2. Raw schema — landing zone in PostgreSQL
3. dbt transformation — staging → intermediate → marts → feature store
4. ML training — 4 models (match outcome, player performance, injury risk, Ballon d'Or)
5. Serving — FastAPI + React dashboard

## Decisions Log

See `docs/decisions/` for individual architecture decision records (ADRs) as they're made.