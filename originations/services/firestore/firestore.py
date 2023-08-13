from google.cloud.firestore import AsyncClient
from originations.services.firestore.config import load_credentials
from originations.config.config import settings


async def load_firestore() -> AsyncClient:
    PROJECT_ID = settings.project_id

    db = AsyncClient(project=PROJECT_ID, credentials=load_credentials())
    return db
