"""Loads and validates environment configuration for FootballIQ.
Fails immediately (EnvironmentError) if a required variable is missing —
never silently returns None, since a silently-missing DB password causes
confusing failures much later in the pipeline.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()  # reads .env into os.environ, if present

# Every env var the app requires to run. Add to this list as new features
# (Airflow, MLflow, etc.) introduce new required variables.
_REQUIRED_VARS = [
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
]


def _get_required(key: str) -> str:
    value = os.environ.get(key)
    if value is None or value == "":
        raise EnvironmentError(
            f"Required environment variable '{key}' is not set. "
            f"Check your .env file against .env.example."
        )
    return value


@dataclass(frozen=True)
class Config:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str
    environment: str
    log_level: str

    @property
    def database_url(self) -> str:
        """SQLAlchemy connection string for psycopg2."""
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


def load_config() -> Config:
    """Build a validated Config object. Raises EnvironmentError if anything
    required is missing — call this once at application startup, not lazily,
    so failures surface immediately rather than mid-pipeline."""
    return Config(
        db_host=_get_required("DB_HOST"),
        db_port=int(_get_required("DB_PORT")),
        db_name=_get_required("DB_NAME"),
        db_user=_get_required("DB_USER"),
        db_password=_get_required("DB_PASSWORD"),
        environment=os.environ.get("ENVIRONMENT", "development"),
        log_level=os.environ.get("LOG_LEVEL", "INFO"),
    )