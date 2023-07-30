from fastapi.responses import JSONResponse
from fastapi import status
from loans_billing_legacy.enums.state import LoanState
from loans_billing_legacy.models.loan import Loan, LoanBalance
from loans_billing_legacy.models.loan_creation import LoanCreationRequest
from loans_billing_legacy.services.firestore.firestore import get_firestore
from loans_billing_legacy.services.firestore.format import format_dict
from loans_billing_legacy.services.firestore.transactional.lock_loan import (
    with_locked_loan,
)
from loans_billing_legacy.utils.repayment_date_calculator import add_month


async def create_new_loan(loan_to_create: LoanCreationRequest) -> JSONResponse:
    firestore = get_firestore()
    customer_ref = firestore.collection("customers").document(
        str(loan_to_create.customer_id)
    )
    existing_customer = await customer_ref.get()
    if not existing_customer.exists:
        return JSONResponse(
            {"outcome": "Attempted to create a loan for a non-existent customer!"},
            status_code=status.HTTP_409_CONFLICT,
        )

    @with_locked_loan(loan_to_create.loan_id)
    async def create_loan_in_transaction(
        loan, loan_ref, loan_to_create: LoanCreationRequest
    ) -> JSONResponse:
        if loan:
            print("Aborting creation - loan already exists!")
            return JSONResponse(
                {"outcome": "Attempted to create a loan that already exists!"},
                status_code=status.HTTP_409_CONFLICT,
            )
        print("Creating loan...")
        # await asyncio.sleep(2)

        loan = Loan(
            loan_id=loan_to_create.loan_id,
            customer_id=loan_to_create.customer_id,
            original_term=loan_to_create.term_in_months,
            remaining_term=loan_to_create.term_in_months,
            repayment_day=loan_to_create.first_repayment_date.day,
            first_repayment_date=loan_to_create.first_repayment_date,
            second_next_repayment_date=add_month(
                loan_to_create.first_repayment_date, 1
            ),
            state=LoanState.PENDING,
            balance=LoanBalance(
                principal_=loan_to_create.amount,
                interest=0,
                principal_1mpd=0,
                interest_1mpd=0,
                principal_2mpd=0,
                interest_2mpd=0,
                principal_3mpd=0,
                interest_3mpd=0,
                principal_4mpd_plus=0,
                interest_4mpd_plus=0,
            ),
            overrides=[],
            mandate=loan_to_create.mandate,
            dd_active=False,
        )
        doc_data = await format_dict(loan.dict())
        await loan_ref.set(doc_data, merge=True)
        print("Created Loan!")

        return JSONResponse(
            {"outcome": "success"},
            status_code=status.HTTP_200_OK,
        )

    return await create_loan_in_transaction(loan_to_create=loan_to_create)
    # Setup DD
    # Disburse Monies
