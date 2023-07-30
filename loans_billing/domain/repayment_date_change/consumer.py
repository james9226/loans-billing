from datetime import date
from google.cloud.pubsub_v1.subscriber.message import Message

from common.enums.event import LoanEventType
from common.models.loan import Loan
from common.services.firestore.firestore import get_sync_firestore
from common.services.firestore.sync.transactional.lock import (
    lock_document,
    release_lock,
)
from common.utils.repayment_day_calculator import add_month
from loans_billing.domain.loan_events.publish import publish_loan_event


def consume_repayment_event(message: Message):
    loan_id = message.attributes.loan_id
    event_id = message.attributes.event_id
    new_repayment_day = message.attributes.repay_day
    firestore = get_sync_firestore()
    loan_ref = firestore.collection("loans").document(str(loan_id))
    existing_loan = lock_document(loan_ref)

    if not existing_loan.exists:
        print(
            "Critical - will not handle repayment date change as loan does not exist!"
        )
        return

    loan = Loan(**existing_loan.to_dict())

    if not loan.behaviour.repayment_date_change_enabled:
        print("Refusing to change repayment date as behaviour is disabled!")
        message.ack()
        return

    if new_repayment_day > 28:
        print("Refusing to change repayment date as day is > 28!")
        message.ack()
        return

    for i in range(0, 2):
        # TODO - messy logic here

        proposed_date = date(
            loan.first_repayment_date.year,
            loan.first_repayment_date.month + i,
            new_repayment_day,
        )

        if (proposed_date - loan.previous_repayment_day).days > 56:
            continue

        if (loan.first_repayment_date - proposed_date).days > 7:
            loan.first_repayment_date = proposed_date
            loan.second_next_repayment_date = add_month(proposed_date, 1)

    # TODO - update principal due and expected interest!

    publish_loan_event(
        loan=loan,
        event_id=event_id,
        event_type=LoanEventType.REPAYMENT_DATE_CHANGED,
    )

    loan_ref.set(loan.dict(), merge=True)

    release_lock(loan_ref)

    message.ack()
    return
