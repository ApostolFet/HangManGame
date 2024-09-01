import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass
class Config:
    language: Literal["ru", "en"] = "ru"
    max_errors: int = 10
    token: str | None = None
    db_path: str | None = None

    @classmethod
    def load_config(cls, path: str = "config.toml") -> "Config":
        with Path(path).open("rb") as file:
            return Config(**tomllib.load(file))
