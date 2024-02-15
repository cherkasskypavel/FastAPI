from dataclasses import dataclass
from typing import  Optional

from environs import Env

@dataclass
class TestConfig:
    test_db_url: str


def load_config(path: Optional[str] = None) -> TestConfig:
    env = Env()
    env.read_env(path)
    return TestConfig(
        test_db_url=env("TEST_DB_URL"),

    )
