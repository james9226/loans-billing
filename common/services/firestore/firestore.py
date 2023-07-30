from google.cloud.firestore import AsyncClient, Client
from loans_billing_legacy.services.firestore.config import load_credentials
from loans_billing_legacy.config.config import settings

async_firestore = None

sync_firestore = None


async def initialize_async_firestore():
    global async_firestore
    PROJECT_ID = settings.project_id

    async_firestore = AsyncClient(project=PROJECT_ID, credentials=load_credentials())


def get_async_firestore() -> AsyncClient:
    return async_firestore


def initialize_sync_firestore():
    global sync_firestore
    PROJECT_ID = settings.project_id

    sync_firestore = Client(project=PROJECT_ID, credentials=load_credentials())


def get_sync_firestore() -> Client:
    return sync_firestore
