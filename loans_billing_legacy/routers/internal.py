from uuid import UUID
from fastapi import APIRouter, Depends
from loans_billing_legacy.domain.creation.create_new_loan import create_new_loan
from loans_billing_legacy.domain.loan_lookup.lookup import get_loan_by_loan_id
from loans_billing_legacy.domain.repayment.repayment import process_repayment
from loans_billing_legacy.middleware.machine_authentication import get_token_header
from loans_billing_legacy.models.loan_creation import LoanCreationRequest

internal_loans_router = APIRouter(
    prefix="/internal",
    tags=["internal"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@internal_loans_router.get("/loan/{loan_id}")
async def read_items(loan_id: UUID):
    return await get_loan_by_loan_id(loan_id)


@internal_loans_router.post("/repayment")
async def handle_repayment():
    return await process_repayment()


@internal_loans_router.post("/loan")
async def create_loan(loan_to_create: LoanCreationRequest):
    return await create_new_loan(loan_to_create)
