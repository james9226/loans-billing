from loans_billing_legacy.services.firestore.firestore import load_firestore
from loans_billing_legacy.services.firestore.format import format_dict


async def post_event(collection: str, document_id: str, body: dict) -> None:
    formatted_body = await format_dict(body)
    firestore = await load_firestore()

    collection_ref = firestore.collection(collection)

    await collection_ref.document(document_id).set(formatted_body)


async def post_batch_events(collection: str, events: dict) -> None:
    firestore = await load_firestore()
    collection = firestore.collection("policy_outcomes")

    batch = firestore.batch()

    for id, body in events:
        doc_ref = collection.document(id)  # type: ignore
        batch.set(doc_ref, body)

    await batch.commit()
