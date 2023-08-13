from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession

from common.models.cloudsql_sqlmodel_models import (
    Balance,
    BalanceDelta,
    LatestBalance,
    Loan,
    TransactionContext,
    TransactionRecord,
)
from common.models.transaction import TransactionRequest


class TransactionService:
    def __init__(self, loan: Loan, db_session: AsyncSession):
        self.loan = loan
        self.existing_keys = [x.balance_key for x in self.loan.latest_balances]
        self.db_session = db_session

    def _create_missing_latest_balances(self, tx_update: TransactionRequest):
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

    def add_transaction(self, tx_update: TransactionRequest) -> None:
        transaction = TransactionRecord(
            id=tx_update.id,
            product_id=tx_update.product_id,
            product_type=tx_update.product_type,
            event_time=datetime.now(),
            event_type=tx_update.event_type,
            balances=[],
            balance_deltas=[],
            context=[],
            loan=self.loan,
        )

        self._create_missing_latest_balances(tx_update)

        for delta_to_apply in tx_update.balance_deltas:
            latest_balance = next(
                x
                for x in self.loan.latest_balances
                if x.balance_key == delta_to_apply.balance_delta_key
            )  # TODO - handle this error

            # Update Latest Balances
            latest_balance.balance_value = (
                latest_balance.balance_value + delta_to_apply.balance_delta_value
            )

            # Update Balance Delta Records
            balance_delta = BalanceDelta(
                transaction_id=tx_update.id,
                product_id=self.loan.id,
                balance_delta_key=delta_to_apply.balance_delta_key,
                balance_delta_value=delta_to_apply.balance_delta_value,
                # transaction=transaction,
            )

            transaction.balance_deltas += [balance_delta]

        for latest_balance in self.loan.latest_balances:
            # Update Balance Records
            balance = Balance(
                transaction_id=tx_update.id,
                product_id=self.loan.id,
                balance_key=latest_balance.balance_key,
                balance_value=latest_balance.balance_value,
                # transaction=transaction,
            )
            transaction.balances += [balance]

        for context in tx_update.context:
            transaction_context = TransactionContext(
                transaction_id=tx_update.id,
                product_id=self.loan.id,
                context_key=context.context_key,
                context_value=context.context_value,
            )
            transaction.context += [transaction_context]

        self.db_session.add(transaction)
