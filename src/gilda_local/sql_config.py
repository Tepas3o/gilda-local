"""SQL database configuration."""

from pydantic import BaseModel


class SQLConfig(BaseModel):
    """SQL Config to establish the connection."""

    user: str = "homeassistant"
    password: str = ""
    host: str = "homeassistant.local"
    database: str = "homeassistant"
    port: int | str = 3306
