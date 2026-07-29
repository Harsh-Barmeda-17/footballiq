# FootballIQ

Production-grade data engineering + ML platform for football analytics — ingests match data from 5 free sources across 5 European leagues, builds a validated star-schema warehouse, trains ML models for match outcome, player performance, injury risk, and Ballon d'Or prediction, and serves explained predictions via a FastAPI backend with a React dashboard.

> 🚧 **Status: In active development.** Built as a learning project — see [roadmap](docs/architecture.md) for build progress.

## Architecture

_Full architecture diagram and description — coming Week 31-32._

## Tech Stack

- **Data Engineering:** Python, PostgreSQL, dbt, Apache Airflow, Great Expectations, Docker
- **Machine Learning:** LightGBM, scikit-learn, MLflow, Optuna, SHAP
- **Backend:** FastAPI
- **Frontend:** React

## Getting Started

_Setup instructions — coming as each phase completes._

## Project Structure

footballiq/
├── ingestion/ # Data collection scripts per source
├── dbt_project/ # dbt transformation models
├── ml/ # ML training and inference scripts
├── api/ # FastAPI application
├── frontend/ # React dashboard
├── tests/ # pytest test files
├── sql/ # SQL prototypes (dev/exploration)
├── utils/ # Shared utilities (logging, config, dates)
├── docs/ # Architecture docs and decision records
├── .github/workflows/ # CI/CD
├── docker-compose.yml
├── .env.example
└── requirements.txt

## License

MIT