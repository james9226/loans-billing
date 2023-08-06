from uuid import UUID
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from common.models.pubsub_schemas.creation_schema import LoanCreationSchema
from common.services.cloudsql.initialize import get_db

from loans_event_processor.dependancies.pubsub_authentication import verify_pubsub_token
from loans_event_processor.dependancies.pubsub_decode import MessageDecoder
from loans_event_processor.domain.creation.consumer import create_loan
from loans_event_processor.domain.disbursal.disbursal import disburse_loan


loan_command_events_router = APIRouter(
    prefix="/consumer",
    tags=["consumer"],
    dependencies=[Depends(verify_pubsub_token)],
    responses={404: {"description": "Not found"}},
)


@loan_command_events_router.post("/creation")
async def consume_loan_creation_event(
    request: LoanCreationSchema = Depends(MessageDecoder(LoanCreationSchema)),
    db: AsyncSession = Depends(get_db),
):
    return await create_loan(request, db)


@loan_command_events_router.post("/disbursal")
async def consume_disbursal_event(
    loan_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await disburse_loan(loan_id, db)
