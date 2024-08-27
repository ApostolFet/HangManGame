from dataclasses import dataclass
from typing import Literal
import tomllib


@dataclass
class Config:
    language: Literal["ru", "en"] = "ru"
    max_errors: int = 10
    token: str | None = None

    @classmethod
    def load_config(cls, path: str = "config.toml") -> "Config":
        with open(path, "rb") as file:
            return Config(**tomllib.load(file))
