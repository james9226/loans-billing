from datetime import date
from uuid import UUID
from common.enums.context_keys import ContextKey
from common.enums.product import ProductType
from common.enums.transaction_type import TransactionType
from common.models.cloudsql_sqlmodel_models import Loan
from common.models.transaction import TransactionContext, TransactionRequest


def generate_eod_transaction(
    loan: Loan, eod_date: date, correlation_id: UUID
) -> TransactionRequest:
    eod_transaction = TransactionRequest(
        product_id=loan.id,
        product_type=ProductType.UPL,
        event_type=TransactionType.END_OF_DAY_PROCESSED,
        balance_deltas=[],
        context=[
            TransactionContext(
                context_key=ContextKey.PROCESSING_DATE, context_value=str(eod_date)
            ),
            TransactionContext(
                context_key=ContextKey.CORRELATION_ID, context_value=str(correlation_id)
            ),
        ],
    )

    return eod_transaction
