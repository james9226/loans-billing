from datetime import date
from logging import getLogger
from uuid import UUID
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from common.enums.transaction_type import TransactionType


from common.models.cloudsql_sqlmodel_models import Loan
from loans_event_processor.domain.eod_processor.eod_marker import (
    generate_eod_transaction,
)
from loans_event_processor.domain.interest.interest import (
    generate_interest_applied_transaction,
)

from loans_event_processor.domain.transaction_service.service import TransactionService
from loans_event_processor.utils.uuid_generator import generate_uuid_from_seed


async def consume_eod_event(
    loan_id: UUID, event_id: UUID, eod_date: date, db: AsyncSession
):
    async with db.begin() as transaction:
        result = await transaction.session.execute(
            select(Loan)
            .options(selectinload(Loan.latest_balances))
            .options(selectinload(Loan.behaviour))
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

        correlation_id = generate_uuid_from_seed(
            f"{loan.id}{TransactionType.END_OF_DAY_PROCESSED}{eod_date}"
        )

        txs = TransactionService(loan=loan, db_session=db)

        interest_accrual = generate_interest_applied_transaction(
            loan, eod_date, correlation_id
        )

        txs.add_transaction(interest_accrual)

        # if (loan.first_repayment_date - eod_date).days == 7:
        #     request_autopay(loan)

        # if loan.first_repayment_date == eod_date:
        #     loan = statement_processor(loan, message.attributes.event_id)

        eod_marker = generate_eod_transaction(loan, eod_date, correlation_id)
        txs.add_transaction(eod_marker)

        await transaction.commit()

    return
