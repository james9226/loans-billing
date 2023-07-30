from typing import Optional
from loans_billing_legacy.middleware.context import get_request_id
from loans_billing_legacy.models.application import ApplicationRequest
from datetime import datetime, timedelta
from loans_billing_legacy.services.bureau.equifax.mock_endpoint import (
    create_mock_bureau_file,
)
from loans_billing_legacy.services.firestore.firestore import load_firestore
from loans_billing_legacy.services.logging import log_handler


async def load_existing_credit_file(applicant_hash: str) -> Optional[dict]:
    firestore = await load_firestore()

    collection = firestore.collection("equifax_credit_file_state_store").document(
        applicant_hash
    )

    docs = await collection.get()

    return docs.to_dict()


async def save_new_credit_file(applicant_hash: str, credit_file: dict) -> None:
    firestore = await load_firestore()

    doc_ref = firestore.collection("equifax_credit_file_state_store").document(
        applicant_hash
    )

    body = {
        "expirey_timestamp": str(datetime.now() + timedelta(days=30)),
        "created_timestamp": str(datetime.now()),
    } | credit_file

    await doc_ref.set(body)


async def mock_equifax_request(request: ApplicationRequest):
    # if no valid cached file, external request to get new one

    log_handler.info(f"Searching for existing credit file!")
    res = await load_existing_credit_file(request.applicant_hash)

    if res:
        log_handler.info(f"Found existing credit file!")
        if res["expirey_timestamp"] > str(datetime.now()):
            log_handler.info(f"Existing credit file still valid!")
            return res
        else:
            log_handler.info(f"Existing credit file no longer valid!")
    else:
        log_handler.info(f"No existing credit file found!")

    log_handler.info(f"Creting new credit file for request {get_request_id()}")

    # Fake External Request
    credit_file = await create_mock_bureau_file()

    await save_new_credit_file(request.applicant_hash, credit_file)

    return credit_file
