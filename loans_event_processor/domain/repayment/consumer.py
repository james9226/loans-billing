from logging import getLogger
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
from loans_event_processor.domain.waterfall.waterfall import (
    get_payment_waterfall_transaction_deltas,
)

logger = getLogger("loans_event_processor")


async def disburse_loan(loan_id: UUID, amount: int, source: str, db: AsyncSession):
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

        if loan.state == LoanState.CLOSED:
            logger.critical(f"Critical error, repayment applied to Closed Loan")
            await transaction.rollback()
            return JSONResponse(
                content={"Message": f"Critical - Loan has been Closed"},
                status_code=status.HTTP_200_OK,
            )

        if amount > loan.get_total_balance() + 100:
            logger.critical(f"Payment too large")
            await transaction.rollback()
            return JSONResponse(
                content={"Message": f"Critical - Payment too large"},
                status_code=status.HTTP_200_OK,
            )

        deltas_for_waterfall = get_payment_waterfall_transaction_deltas(loan, amount)

        repayment_applied = TransactionRequest(
            product_id=loan_id,
            product_type=ProductType.UPL,
            event_type=TransactionType.REPAYMENT_APPLIED,
            event_source="Loans Billing Backend",
            funding_source=f"Source : {source}",
            funding_destination="Lendotopia Corporate Account",
            balance_deltas=deltas_for_waterfall,
        )
        txs = TransactionService(loan=loan, db_session=transaction.session)
        txs.add_transaction(repayment_applied)

        await transaction.commit()

    return JSONResponse(
        content={"Message": f"Applied repayment for loan {loan_id}"},
        status_code=status.HTTP_200_OK,
    )
