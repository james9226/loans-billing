import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from google.cloud.firestore_v1.async_document import AsyncDocumentReference
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore import async_transactional

from originations.services.firestore.firestore import load_firestore


@dataclass
class LockResult:
    success: bool
    document_snapshot: Optional[DocumentSnapshot]


async def release_lock(
    document_reference: AsyncDocumentReference,
    lock_column: str = "is_locked",
    lock_timestamp_column: str = "lock_enabled_timestamp",
):
    await document_reference.set(
        {lock_column: False, lock_timestamp_column: None}, merge=True
    )
    print(f"Released lock on loan!")


async def lock_document(
    document_reference: AsyncDocumentReference,
    lock_column: str = "is_locked",
    lock_timestamp_column: str = "lock_enabled_timestamp",
) -> Optional[DocumentSnapshot]:
    MAX_RETRIES = 30
    RETRY_DELAY_IN_SECONDS = 1

    for _ in range(MAX_RETRIES):
        # We try a maximum of 30 times (30 seconds)
        lock_result = await __try_to_obtain_lock(
            document_reference, lock_column, lock_timestamp_column
        )

        if lock_result.success:
            print(f"Obtained lock on loan!")
            return lock_result.document_snapshot
        print("Retrying lock...")
        await asyncio.sleep(RETRY_DELAY_IN_SECONDS)

    raise RuntimeError(
        f"Maximum retries of {MAX_RETRIES} reached attempting to set a lock!"
    )


async def __try_to_obtain_lock(
    document_reference: AsyncDocumentReference,
    lock_column: str,
    lock_timestamp_column: str,
) -> LockResult:
    firestore = await load_firestore()
    transaction = firestore.transaction()

    @async_transactional
    async def try_to_lock_in_transactio(
        transaction,
        document_reference: AsyncDocumentReference,
        lock_column: str,
        lock_timestamp_column: str,
    ) -> LockResult:
        doc = await document_reference.get(transaction=transaction)

        if doc.exists:
            if doc.to_dict()["is_locked"]:  # Can we make this more robust
                print("Loan is locked!")
                return LockResult(False, None)

        transaction.set(
            document_reference,
            {lock_column: True, lock_timestamp_column: datetime.now()},
            merge=True,
        )
        return LockResult(True, doc)

    return await try_to_lock_in_transactio(
        transaction=transaction,
        document_reference=document_reference,
        lock_column=lock_column,
        lock_timestamp_column=lock_timestamp_column,
    )
