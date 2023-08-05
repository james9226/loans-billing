from datetime import datetime
import json
from uuid import UUID
from common.enums.event import LoanEventReportingType, LoanEventType
from common.models.balance import LoanBalance
from common.models.loan import Loan
from common.services.firestore.format import format_dict
from common.services.pubsub.publisher import get_pub_sub_publisher
from loans_billing.config.config import settings


async def publish_loan_event(
    loan: Loan,
    event_id: UUID,
    event_type: LoanEventType,
):
    pub_sub = get_pub_sub_publisher()

    message_json = json.dumps(
        {
            "event_id": str(event_id),
            "event_time": str(datetime.now()),
            "event_type": event_type,
        }
        | format_dict(loan.dict())
    ).encode("utf-8")

    await pub_sub.publish_message_async(message_json, settings.loan_event_topic_id)


async def publish_reporting_loan_event(
    loan: Loan,
    balance_deltas: LoanBalance,
    event_id: UUID,
    event_type: LoanEventReportingType,
):
    pub_sub = get_pub_sub_publisher()

    message_json = json.dumps(
        {
            "event_id": str(event_id),
            "event_time": str(datetime.now()),
            "event_type": event_type,
            "balance_deltas": balance_deltas.dict(),
        }
        | format_dict(loan.dict())
    ).encode("utf-8")

    await pub_sub.publish_message_async(
        message_json, settings.loan_event_reporting_topic_id
    )
