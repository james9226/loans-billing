from datetime import date
from uuid import UUID
from google.cloud.pubsub_v1.subscriber.message import Message

from common.enums.event import LoanEventType
from common.enums.state import LoanState
from common.models.loan import Loan
from common.services.firestore.firestore import get_sync_firestore
from common.services.firestore.sync.transactional.lock import (
    lock_document,
    release_lock,
)
from loans_billing.commands.request_auto_payment import request_autopay
from loans_billing.domain.eod_processor.statement_processor import statement_processor
from loans_billing.domain.interest.interest import accrue_interest
from loans_billing.domain.loan_events.publish import publish_loan_event


def consume_eod_event(message: Message):
    loan_id: UUID = message.attributes.loan_id
    eod_date: date = message.attributes.date
    firestore = get_sync_firestore()
    loan_ref = firestore.collection("loans").document(str(loan_id))
    existing_loan = lock_document(loan_ref)

    if not existing_loan.exists:
        print("Critical - will not handle override removal as loan does not exist!")
        return

    loan = Loan(**existing_loan.to_dict())

    loan = accrue_interest(loan, message.attributes.event_id)

    if (loan.first_repayment_date - eod_date).days == 7:
        request_autopay(loan)

    if loan.first_repayment_date == eod_date:
        loan = statement_processor(loan, message.attributes.event_id)

    publish_loan_event(
        loan=loan,
        event_id=message.attributes.event_id,
        event_type=LoanEventType.END_OF_DAY_PROCESSED,
    )

    loan_ref.set(loan.dict(), merge=True)

    release_lock(loan_ref)

    message.ack()
    return
