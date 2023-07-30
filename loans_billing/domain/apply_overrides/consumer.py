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
from loans_billing.domain.principal_due.calculate_due import set_due_balances
from loans_billing.domain.state.state_manager import update_account_state


def consume_disbursal_event(message: Message) -> None:
    loan_id = message.attributes.loan_id
    firestore = get_sync_firestore()
    loan_ref = firestore.collection("loans").document(str(loan_id))
    existing_loan = lock_document(loan_ref)

    if not existing_loan.exists:
        print("Critical - could not handle disbursal event as loan does not exist!")
        return

    loan = Loan(**existing_loan.to_dict())

    loan.behaviour += message.attributes  # TODO - fix this!

    loan = update_behaviours(loan, message.attributes.event_id)

    publish_loan_event(
        loan,
        loan.balance - loan.balance,
        message.attributes.event_id,
        LoanEventType.LOAN_BEHAVIOUR_OVERRIDE_APPLIED,
    )
    loan_ref.set(loan.dict(), merge=True)

    release_lock(loan_ref)
    message.ack()
