from datetime import datetime
from uuid import UUID
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select


from common.enums.product import ProductType
from common.enums.state import LoanState
from common.enums.transaction_type import TransactionType
from common.enums.tx_keys import TransactionKey
from common.models.cloudsql_sqlmodel_models import Loan
from common.models.transaction import TransactionDelta, TransactionRequest

from loans_event_processor.domain.transaction_service.service import TransactionService


async def disburse_loan(loan_id: UUID, db: AsyncSession):
    async with db.begin() as transaction:
        result = await transaction.session.execute(
            select(Loan)
            .options(selectinload(Loan.latest_balances))
            .options(selectinload(Loan.mandate))
            .where(Loan.id == loan_id)
            .with_for_update()
        )
        loan: Loan = result.scalar_one_or_none()

        # Very rudimentary validation
        if loan is None:
            await transaction.rollback()
            return JSONResponse(
                content={"Message": f"No Loan Found"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if loan.state != LoanState.PENDING:
            await transaction.rollback()
            return JSONResponse(
                content={"Message": f"Loan Has Already Been Recorded as Disbursed"},
                status_code=status.HTTP_200_OK,
            )

        loan.state = LoanState.LIVE
        loan.disbursal_time = datetime.now()

        balance_to_disburse = loan.get_balance_by_key(
            TransactionKey.PRINCIPAL_TO_DISBURSE
        )
        disbursal = TransactionRequest(
            product_id=loan_id,
            product_type=ProductType.UPL,
            event_type=TransactionType.LOAN_DISBURSED,
            event_source="Loans Billing Backend",
            funding_source="Lendotopia Corporate Account",
            funding_destination=f"Account: {loan.mandate.account_number}, Sort Code: {loan.mandate.sort_code}",
            balance_deltas=[
                TransactionDelta(
                    balance_delta_key=TransactionKey.PRINCIPAL_TO_DISBURSE,
                    balance_delta_value=-balance_to_disburse,
                ),
                TransactionDelta(
                    balance_delta_key=TransactionKey.PRINCIPAL,
                    balance_delta_value=balance_to_disburse,
                ),
            ],
        )
        txs = TransactionService(loan=loan, db_session=transaction.session)
        txs.add_transaction(disbursal)

        await transaction.commit()

    return JSONResponse(
        content={"Message": f"Recorded disbursal for loan {loan_id}"},
        status_code=status.HTTP_200_OK,
    )
