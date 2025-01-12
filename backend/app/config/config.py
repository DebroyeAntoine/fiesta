# config/config.py
from dataclasses import dataclass
from functools import lru_cache
import os
from enum import Enum
from pathlib import Path
import yaml

class Environment(Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

@dataclass
class DatabaseConfig:
    url: str
    pool_size: int
    max_overflow: int
    echo: bool

@dataclass
class SecurityConfig:
    jwt_secret: str
    jwt_access_expires: int  # in seconds
    jwt_refresh_expires: int  # in seconds
    allowed_origins: list[str]
    password_min_length: int
    rate_limit_default: str
    rate_limit_login: str

@dataclass
class WebSocketConfig:
    ping_timeout: int
    ping_interval: int
    max_clients: int

@dataclass
class AppConfig:
    env: Environment
    debug: bool
    database: DatabaseConfig
    security: SecurityConfig
    websocket: WebSocketConfig

    @classmethod
    @lru_cache
    def load(cls) -> 'AppConfig':
        env = Environment(os.getenv('APP_ENV', 'development'))
        config_path = Path(__file__).parent / f"{env.value}.yaml"

        if config_path.exists():
            with open(config_path, encoding='utf-8') as f:
                yaml_config = yaml.safe_load(f)
        else:
            yaml_config = {}
        allowed_origins_env = os.getenv('ALLOWED_ORIGINS', None)
        allowed_origins_config = yaml_config.get(
                'security', {}).get('allowed_origins', '*')

        if allowed_origins_env:
            # If ALLOWED_ORIGINS is set in the environment, split it into a
            # list
            allowed_origins = allowed_origins_env.split(',')
        elif isinstance(allowed_origins_config, list):
            # If allowed_origins from the config is already a list, use it
            # directly
            allowed_origins = allowed_origins_config
        else:
            # Otherwise, assume it's a string and split it
            allowed_origins = allowed_origins_config.split(',')
        return cls(
            env=env,
            debug=env != Environment.PRODUCTION,
            database=DatabaseConfig(
                url=os.getenv(
                    'DATABASE_URL',
                    yaml_config.get('database', {}).get('url',
                                                        'sqlite:///site.db')),
                pool_size=int(os.getenv(
                    'DB_POOL_SIZE',
                    yaml_config.get('database', {}).get('pool_size', 5))),
                max_overflow=int(os.getenv(
                    'DB_MAX_OVERFLOW',
                    yaml_config.get('database', {}).get('max_overflow', 10))),
                echo=env != Environment.PRODUCTION
            ),
            security=SecurityConfig(
                jwt_secret=os.getenv(
                    'JWT_SECRET',
                    yaml_config.get('security', {}).get('jwt_secret')),
                allowed_origins=allowed_origins,
                jwt_access_expires=int(os.getenv(
                    'JWT_ACCESS_EXPIRES',
                    yaml_config.get('security', {}).get('jwt_access_expires',
                                                        900))),
                password_min_length=int(os.getenv(
                    'PASSWORD_MIN_LENGTH',
                    yaml_config.get('security', {}).get('password_min_length',
                                                        8))),
                jwt_refresh_expires=int(os.getenv(
                    'JWT_REFRESH_EXPIRES',
                    yaml_config.get('security', {}).get('jwt_refresh_expires',
                                                        604800))),
                rate_limit_default=os.getenv(
                    'RATE_LIMIT_DEFAULT',
                    yaml_config.get('security', {}).get('rate_limit_default',
                                                        "200 per day")),
                rate_limit_login=os.getenv(
                    'RATE_LIMIT_LOGIN',
                    yaml_config.get('security', {}).get('rate_limit_login',
                                                        "5 per minute"))
            ),
            websocket=WebSocketConfig(
                ping_timeout=int(os.getenv(
                    'WS_PING_TIMEOUT',
                    yaml_config.get('websocket', {}).get('ping_timeout', 20))),
                ping_interval=int(os.getenv(
                    'WS_PING_INTERVAL',
                    yaml_config.get('websocket', {}).get(
                        'ping_interval', 25))),
                max_clients=int(os.getenv(
                    'WS_MAX_CLIENTS',
                    yaml_config.get('websocket', {}).get('max_clients', 1000)))
            )
        )
