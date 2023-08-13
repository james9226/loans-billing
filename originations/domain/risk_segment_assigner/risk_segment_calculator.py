from originations.domain.risk_segment_assigner.config import RISK_SEGMENT_CUTOFFS
from originations.models.application import ApplicationRequest
from originations.models.credit_variables import CreditVariables
from originations.services.scorecard.risk_model_service import mock_risk_model_service
from originations.services.pubsub.async_publisher import publish_message, nullable
from originations.domain.pricing.pricing import get_pricing
from originations.services.logging import log_handler


async def risk_segment_calculator(risk_score: float) -> int:
    segment = max(
        (k for k, v in RISK_SEGMENT_CUTOFFS.items() if v > risk_score), default=1
    )
    log_handler.info(f"Assigned risk segment of {segment}")
    return segment


async def risk_pricing_assigner(
    request: ApplicationRequest, credit_variables: CreditVariables
) -> int:
    risk_score = await mock_risk_model_service(request, credit_variables)

    risk_segment = await risk_segment_calculator(risk_score)

    apr = await get_pricing(risk_segment)

    await publish_message(
        {
            "reference_id": str(request.application_id),
            "risk_score": risk_score,
            "risk_segment": risk_segment,
            "price": nullable("double", apr),
        },
        "risk_pricing_assigned_topic",
    )

    return apr
