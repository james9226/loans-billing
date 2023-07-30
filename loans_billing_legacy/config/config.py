# type: ignore

from pydantic import BaseSettings


class Settings(BaseSettings):
    project_id: str
    client_id: str
    client_x509_cert_url: str
    firebase_private_key_id: str
    firebase_client_email: str

    class Config:
        env_file = ".env"


settings = Settings()
