from pydantic import BaseSettings


class DBSettings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: str
    db_connection_name: str

    class Config:
        env_file = ".env"


db_settings = DBSettings()
