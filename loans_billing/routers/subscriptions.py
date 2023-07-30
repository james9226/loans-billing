from fastapi import APIRouter, Depends
from common.models.pubsub_schemas.creation_schema import LoanCreationSchema

from loans_billing.dependancies.pubsub_authentication import verify_pubsub_token
from loans_billing.dependancies.pubsub_decode import MessageDecoder
from loans_billing.domain.creation.consumer import create_loan


loan_command_events_router = APIRouter(
    prefix="/consumer",
    tags=["consumer"],
    dependencies=[Depends(verify_pubsub_token)],
    responses={404: {"description": "Not found"}},
)


@loan_command_events_router.post("/creation")
async def consume_loan_creation_event(
    request: LoanCreationSchema = Depends(MessageDecoder(LoanCreationSchema)),
):
    return await create_loan(request)
