import asyncio
from loans_billing_legacy.models.credit_variables import CreditVariables
from loans_billing_legacy.models.application import ApplicationRequest
from loans_billing_legacy.services.logging import log_handler


async def mock_risk_model_service(
    request: ApplicationRequest, credit_variables: CreditVariables
):
    await asyncio.sleep(0.2)

    risk_score = (750 - credit_variables.credit_score) / 3000

    log_handler.info(f"Scored application with a risk score of {risk_score}")

    return risk_score
