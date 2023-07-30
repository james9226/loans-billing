from datetime import datetime

from fastapi.responses import JSONResponse
from fastapi import status

from common.models.loan_creation import LoanCreationRequest
from common.enums.event import LoanEventType
from common.models.pubsub_schemas.creation_schema import LoanCreationSchema
from common.services.firestore.asynchronous.transactional.lock import lock_document
from common.services.firestore.firestore import get_async_firestore
from common.services.firestore.format import format_dict
from common.services.firestore.lock import release_lock
from loans_billing.domain.balances_initializer.initializer import initialize_balances
from loans_billing.domain.creation.builder import build_balance_deltas, build_loan
from loans_billing.domain.loan_events.publish import publish_loan_event


async def create_loan(loan_to_create: LoanCreationSchema):
    firestore = get_async_firestore()
    customer_ref = firestore.collection("customers").document(
        str(loan_to_create.customer_id)
    )
    existing_customer = await customer_ref.get()
    if not existing_customer.exists:
        print(
            f"Refusing to create loan {loan_to_create.loan_id}, customer does not exist"
        )
        return JSONResponse(
            content={
                "Message": f"Refusing to create loan {loan_to_create.loan_id}, customer does not exist"
            },
            status_code=status.HTTP_409_CONFLICT,
        )

    loan_ref = firestore.collection("loans").document(str(loan_to_create.loan_id))
    existing_loan = await lock_document(loan_ref)
    if existing_loan.exists:
        print(f"Skipping creating loan {loan_to_create.loan_id}, existing loan found")
        await release_lock(loan_ref)
        return JSONResponse(
            content={
                "Message": f"Skipping creating loan {loan_to_create.loan_id}, existing loan found"
            },
            status_code=status.HTTP_200_OK,
        )

    loan = build_loan(loan_to_create)

    loan = initialize_balances(loan, loan_to_create.amount, loan_to_create.event_id)

    doc_data = format_dict(loan.dict())
    await loan_ref.set(doc_data, merge=True)

    await release_lock(loan_ref)

    # publish_loan_event(
    #     loan=loan,
    #     event_id=loan_to_create.event_id,
    #     event_type=LoanEventType.LOAN_CREATED,
    # )
    return JSONResponse(
        content={"Message": f"Created Loan {loan_to_create.loan_id}"},
        status_code=status.HTTP_201_CREATED,
    )
