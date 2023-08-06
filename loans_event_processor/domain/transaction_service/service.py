from datetime import datetime
from common.models.cloudsql_sqlmodel_models import (
    Balance,
    BalanceDelta,
    LatestBalance,
    Loan,
    TransactionRecord,
)
from common.models.transaction import TransactionDelta, TransactionRequest
from sqlmodel.ext.asyncio.session import AsyncSession


class TransactionService:
    def __init__(self, loan: Loan, db_session: AsyncSession):
        self.loan = loan
        self.existing_keys = [x.balance_key for x in self.loan.latest_balances]
        self.db_session = db_session

    def __create_missing_latest_balances(self, tx_update: TransactionRequest):
        update_keys = [x.balance_delta_key for x in tx_update.balance_deltas]

        missing_keys = [x for x in update_keys if x not in self.existing_keys]

        for key in missing_keys:
            latest_balance = LatestBalance(
                product_id=tx_update.product_id,
                transaction_id=tx_update.id,
                balance_key=key,
                balance_value=0,
                loan=self.loan,
            )
            self.db_session.add(latest_balance)

    def add_transaction(self, tx_update: TransactionRequest):
        transaction = TransactionRecord(
            id=tx_update.id,
            product_id=tx_update.product_id,
            product_type=tx_update.product_type,
            event_time=datetime.now(),
            event_type=tx_update.event_type,
            event_source=tx_update.event_source,
            funding_source=tx_update.funding_source,
            funding_destination=tx_update.funding_destination,
            event_notes=tx_update.event_notes,
            balances=[],
            balance_deltas=[],
            loan=self.loan,
        )

        self.__create_missing_latest_balances(tx_update)

        for latest_balance in self.loan.latest_balances:
            delta_to_apply: TransactionDelta = next(
                (
                    delta
                    for delta in tx_update.balance_deltas
                    if delta.balance_delta_key == latest_balance.balance_key
                ),
                TransactionDelta(
                    balance_delta_key=latest_balance.balance_key, balance_delta_value=0
                ),
            )

            latest_balance.balance_value = (
                latest_balance.balance_value + delta_to_apply.balance_delta_value
            )
            latest_balance.transaction_id = tx_update.id

            balance = Balance(
                transaction_id=tx_update.id,
                product_id=self.loan.id,
                balance_key=latest_balance.balance_key,
                balance_value=latest_balance.balance_value,
                # transaction=transaction,
            )
            transaction.balances += [balance]

            balance_delta = BalanceDelta(
                transaction_id=tx_update.id,
                product_id=self.loan.id,
                balance_delta_key=delta_to_apply.balance_delta_key,
                balance_delta_value=delta_to_apply.balance_delta_value,
                # transaction=transaction,
            )

            transaction.balance_deltas += [balance_delta]

        self.db_session.add(transaction)
