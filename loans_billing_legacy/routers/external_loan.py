from uuid import UUID
from fastapi import APIRouter, Depends
from loans_billing_legacy.domain.loan_lookup.lookup import get_loan_by_loan_id
from loans_billing_legacy.middleware.customer_authentication import verify_token


external_loan_engine_router = APIRouter(
    prefix="/external",
    tags=["external"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)


@external_loan_engine_router.get("/loan/{loan_id}")
async def read_items(loan_id: UUID):
    return await get_loan_by_loan_id(loan_id)


@external_loan_engine_router.get("/loan/customer/{customer_id}")
async def read_items(customer_id: UUID):
    return await get_loan_by_loan_id(customer_id)
