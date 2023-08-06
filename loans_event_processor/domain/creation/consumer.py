from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from common.enums.product import ProductType
from common.enums.transaction_type import TransactionType
from common.enums.tx_keys import TransactionKey

from common.models.pubsub_schemas.creation_schema import LoanCreationSchema
from common.models.transaction import TransactionDelta, TransactionRequest

from loans_event_processor.domain.creation.builder import (
    build_loan,
)
from loans_event_processor.domain.creation.delta_initializer import (
    build_disbursal_transaction_request,
)
from loans_event_processor.domain.transaction_service.service import TransactionService


async def create_loan(loan_to_create: LoanCreationSchema, db: AsyncSession):
    loan = build_loan(loan_to_create)

    db.add(loan)

    txs = TransactionService(loan=loan, db_session=db)
    txs.add_transaction(
        build_disbursal_transaction_request(
            loan_to_create=loan_to_create, amount=loan_to_create.amount
        )
    )

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        print(e)
        return JSONResponse(
            content={"Message": f"Loan with id {loan.id} already exists."},
            status_code=status.HTTP_200_OK,
        )

    # try:
    #     await db.commit()
    # except IntegrityError as e:
    #     await db.rollback()
    #     print(e)
    #     return JSONResponse(
    #         content={"Message": f"Disbursal Failed"},
    #         status_code=status.HTTP_200_OK,
    #     )

    return JSONResponse(
        content={"Message": f"Created Loan {loan_to_create.loan_id}"},
        status_code=status.HTTP_201_CREATED,
    )
