from google.cloud.firestore import AsyncClient
from loans_billing_legacy.services.firestore.config import load_credentials
from loans_billing_legacy.config.config import settings

firestore = None


async def initialize_firestore():
    global firestore
    PROJECT_ID = settings.project_id

    firestore = AsyncClient(project=PROJECT_ID, credentials=load_credentials())


def get_firestore() -> AsyncClient:
    return firestore
