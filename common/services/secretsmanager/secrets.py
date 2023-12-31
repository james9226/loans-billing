from google.cloud import secretmanager
from loans_billing_legacy.config.config import settings


def access_secret_version(secret_id, version_id="latest"):
    PROJECT_ID = settings.project_id

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode("UTF-8")
