from datetime import datetime
import json
from uuid import UUID
from common.enums.event import LoanEventReportingType, LoanEventType
from common.models.balance import LoanBalance
from common.models.loan import Loan
from common.services.pubsub.publisher import get_pub_sub_publisher
from loans_billing.config.config import LoansBillingSettings


def publish_loan_event(
    loan: Loan,
    event_id: UUID,
    event_type: LoanEventType,
):
    pub_sub = get_pub_sub_publisher()

    message_json = json.dumps(
        {
            "event_id": event_id,
            "event_time": datetime.now(),
            "event_type": event_type,
        }
        | loan.dict()
    ).encode("utf-8")

    pub_sub.publish_message_sync(message_json, LoansBillingSettings.loan_event_topic_id)


def publish_reporting_loan_event(
    loan: Loan,
    balance_deltas: LoanBalance,
    event_id: UUID,
    event_type: LoanEventReportingType,
):
    pub_sub = get_pub_sub_publisher()

    message_json = json.dumps(
        {
            "event_id": event_id,
            "event_time": datetime.now(),
            "event_type": event_type,
            "balance_deltas": balance_deltas.dict(),
        }
        | loan.dict()
    ).encode("utf-8")

    pub_sub.publish_message_sync(
        message_json, LoansBillingSettings.loan_event_reporting_topic_id
    )
