from google.cloud.pubsub_v1.subscriber.message import Message

from common.enums.event import LoanEventType
from common.enums.state import LoanState
from common.models.loan import Loan

from common.services.firestore.firestore import get_sync_firestore
from common.services.firestore.sync.transactional.lock import (
    lock_document,
    release_lock,
)

from loans_billing.domain.behaviour.behaviour_manager import update_behaviours
from loans_billing.domain.loan_events.publish import publish_loan_event
from loans_billing.domain.state.state_manager import update_account_state
from loans_billing.domain.writeoff.writeoff import writeoff_loan


def consume_closure_event(message: Message) -> None:
    loan_id = message.attributes.loan_id
    event_id = message.attributes.event_id
    firestore = get_sync_firestore()

    loan_ref = firestore.collection("loans").document(str(loan_id))
    existing_loan = lock_document(loan_ref)

    if not existing_loan.exists:
        print("Critical - could not handle closure event as loan does not exist!")
        return

    loan = Loan(**existing_loan.to_dict())

    if loan.balance.total_balance() > 0:
        loan = writeoff_loan(loan, event_id)

    loan.state = LoanState.CLOSED
    loan = update_account_state(loan, event_id)

    loan = update_behaviours(loan, event_id)

    publish_loan_event(
        loan,
        event_id,
        LoanEventType.LOAN_CLOSED,
    )

    loan_ref.set(loan.dict(), merge=True)

    release_lock(loan_ref)
    message.ack()

    return
