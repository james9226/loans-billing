from google.oauth2 import service_account
from originations.services.secretsmanager.secrets import access_secret_version
from originations.config.config import settings
import cachetools.func


@cachetools.func.ttl_cache(ttl=10 * 60)
def load_credentials() -> service_account.Credentials:
    private_key = access_secret_version("firebase_private_key").replace(
        "\\n", "\n"
    )  # Needed due to Pythons ever so helpful auto-escaping
    credentials = {
        "type": "service_account",
        "project_id": settings.project_id,
        "private_key_id": settings.firebase_private_key_id,
        "private_key": private_key,
        "client_email": settings.firebase_client_email,
        "client_id": settings.client_id,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": settings.client_x509_cert_url,
    }

    google_auth_credentials = service_account.Credentials.from_service_account_info(
        info=credentials
    )

    return google_auth_credentials
