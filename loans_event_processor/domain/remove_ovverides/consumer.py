from google.cloud.pubsub_v1.subscriber.message import Message

from common.enums.event import LoanEventType
from common.models.loan import Loan
from common.services.firestore.firestore import get_sync_firestore
from common.services.firestore.sync.transactional.lock import (
    lock_document,
    release_lock,
)

from loans_event_processor.domain.behaviour.behaviour_manager import update_behaviours
from loans_event_processor.domain.loan_events.publish import publish_loan_event


def consume_override_removal_message(message: Message) -> None:
    loan_id = message.attributes.loan_id
    firestore = get_sync_firestore()
    loan_ref = firestore.collection("loans").document(str(loan_id))
    existing_loan = lock_document(loan_ref)

    if not existing_loan.exists:
        print("Critical - will not handle override removal as loan does not exist!")
        return

    loan = Loan(**existing_loan.to_dict())

    if message.attributes.id not in [x.id for x in loan.overrides]:
        print(
            "Warning - will not handle override removal as override does not exist on loan!"
        )
        message.ack()
        return

    loan.overrides = [x for x in loan.overrides if x.id != message.attributes.id]

    loan = update_behaviours(loan, message.attributes.event_id)

    publish_loan_event(
        loan,
        loan.balance - loan.balance,
        message.attributes.event_id,
        LoanEventType.LOAN_BEHAVIOUR_OVERRIDE_REMOVED,
    )
    loan_ref.set(loan.dict(), merge=True)

    release_lock(loan_ref)
    message.ack()
    return
