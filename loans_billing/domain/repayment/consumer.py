from google.cloud.pubsub_v1.subscriber.message import Message

from common.enums.event import LoanEventType
from common.models.loan import Loan
from common.services.firestore.firestore import get_sync_firestore
from common.services.firestore.sync.transactional.lock import (
    lock_document,
    release_lock,
)
from loans_billing.domain.behaviour.behaviour_manager import update_behaviours
from loans_billing.domain.loan_events.publish import publish_loan_event
from loans_billing.domain.repayment.waterfall import apply_payment_waterfall
from loans_billing.domain.state.state_manager import update_account_state


def consume_repayment_event(message: Message):
    loan_id = message.attributes.loan_id
    event_id = message.attributes.event_id
    amount = message.attributes.amount

    firestore = get_sync_firestore()
    loan_ref = firestore.collection("loans").document(str(loan_id))
    existing_loan = lock_document(loan_ref)

    if not existing_loan.exists:
        print("Critical - will not handle repayment as loan does not exist!")
        return

    if amount < 0:
        print("Critical - repayment is negative!")
        return

    loan = Loan(**existing_loan.to_dict())

    loan = apply_payment_waterfall(event_id, amount, event_id)
    loan = update_account_state(loan, event_id)
    loan = update_behaviours(loan, event_id)

    publish_loan_event(
        loan=loan,
        event_id=event_id,
        event_type=LoanEventType.REPAYMENT_APPLIED,
    )

    loan_ref.set(loan.dict(), merge=True)

    release_lock(loan_ref)

    message.ack()
    return
