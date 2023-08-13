from decimal import Decimal

from common.enums.tx_keys import TransactionKey
from common.models.cloudsql_sqlmodel_models import Loan
from common.models.transaction import TransactionDelta

WATERFALL = [
    TransactionKey.INTEREST_MPD4_PLUS,
    TransactionKey.INTEREST_MPD3,
    TransactionKey.INTEREST_MPD2,
    TransactionKey.INTEREST_MPD1,
    TransactionKey.PRINCIPAL_MPD4_PLUS,
    TransactionKey.PRINCIPAL_MPD3,
    TransactionKey.PRINCIPAL_MPD2,
    TransactionKey.PRINCIPAL_MPD1,
    TransactionKey.INTEREST,
    TransactionKey.PRINCIPAL_AMOUNT_TO_COVER_INTEREST,
    TransactionKey.PRINCIPAL_DUE,
    TransactionKey.PRINCIPAL,
    # TransactionKey.PRINCIPAL_TO_DISBURSE, # This should never have repayment waterfall applied to it
    TransactionKey.UNHANDLED_FUNDS,
]


def get_payment_waterfall_transaction_deltas(
    loan: Loan, amount: Decimal
) -> list[TransactionDelta]:
    deltas: list[TransactionDelta] = []

    for key in WATERFALL:
        balance = loan.get_balance_by_key(key)

        if key != TransactionKey.UNHANDLED_FUNDS:
            amount_to_apply = max(min(balance, amount), 0)
        else:
            amount_to_apply = max(amount, 0)

        delta = TransactionDelta(
            balance_delta_key=key, balance_delta_value=-amount_to_apply
        )

        amount -= amount_to_apply

        deltas += [delta]

        if amount < 0:
            raise ValueError("CRITICAL MISHANDLING")

    return deltas
