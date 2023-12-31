from common.enums.product import ProductType
from common.enums.transaction_type import TransactionType
from common.enums.tx_keys import TransactionKey
from common.models.loan_creation import LoanCreationRequest
from common.models.transaction import TransactionDelta, TransactionRequest


def build_initial_transaction_deltas(amount: int):
    deltas = []
    for key in TransactionKey:
        if key == TransactionKey.PRINCIPAL_TO_DISBURSE:
            delta = TransactionDelta(balance_delta_key=key, balance_delta_value=amount)
        else:
            delta = TransactionDelta(balance_delta_key=key, balance_delta_value=0)

        deltas += [delta]

    return deltas


def build_disbursal_transaction_request(
    loan_to_create: LoanCreationRequest, amount: int
):
    deltas = build_initial_transaction_deltas(amount)

    return TransactionRequest(
        product_id=loan_to_create.loan_id,
        product_type=ProductType.UPL,
        event_type=TransactionType.LOAN_CREATED,
        balance_deltas=deltas,
        context=[],
    )
