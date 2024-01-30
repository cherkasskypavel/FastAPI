from dataclasses import dataclass
from typing import Optional


from environs import Env

SECRET_KEY = 'mysecret_key'
ALGORITHM = 'HS256'

JWT_EXPIRE_DELTA = 2    #   minutes


@dataclass
class Config:
    db_url: str
    secret_key: str
    algorithm: str
    jwt_expire_delta: int


def load_config(path: Optional[str] = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        db_url=env("DB_URL"),
        secret_key=env("SECRET_KEY"),
        algorithm=env("ALGORITHM"),
        jwt_expire_delta=env("JWT_EXPIRE_DELTA")
    )


