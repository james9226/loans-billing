from uuid import UUID
from google.cloud.pubsub_v1.subscriber.message import Message

from common.enums.event import LoanEventReportingType
from common.models.loan import Loan

from loans_billing.domain.behaviour.behaviour_calculator import update_loan_behaviour
from loans_billing.domain.loan_events.publish import publish_reporting_loan_event


def update_behaviours(loan: Loan, event_id: UUID):
    loan = update_loan_behaviour(loan)

    publish_reporting_loan_event(
        loan,
        loan.balance - loan.balance,
        event_id,
        LoanEventReportingType.ACCOUNT_BEHAVIOUR_UPDATED,
    )

    return loan
