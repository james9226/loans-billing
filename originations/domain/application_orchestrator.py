import asyncio
from originations.domain.affordability.affordability_calculator import (
    affordability_calculator,
)
from originations.domain.policy.endpoints.quotation import quotation_endpoint
from originations.domain.pricing.pricing import get_pricing
from originations.middleware.context import get_request_datetime, get_request_id

from originations.models.request import ApplicationRequestInput
from originations.models.application import ApplicationRequest

from originations.domain.credit_variables.credit_variable_calculator import (
    calculate_credit_variables,
)
from originations.domain.policy.endpoints.prevetting import prevetting_endpoint
from originations.domain.applicant_hash.hasher import hash_application
from originations.domain.outcomes.phase_outcomes import phase_outcome_decider
from originations.domain.outcomes.result import application_result
from originations.domain.risk_segment_assigner.risk_segment_calculator import (
    risk_pricing_assigner,
    risk_segment_calculator,
)
from originations.services.logging import log_handler

from originations.services.scorecard.risk_model_service import mock_risk_model_service
from originations.services.bureau.equifax.load_file import mock_equifax_request
from originations.services.firestore.io import post_event
from originations.services.triggers_state_store.store import get_policy_triggers
from originations.services.pubsub.async_publisher import publish_message


async def application_orchestrator(raw_request: ApplicationRequestInput):
    """
    - Validate Inputs

    Async:
        - Log Request to DB
        - Run Prevetting

    Async:
        - Log Prevetting Results to DB
        - Pull External Data

    Async:
        - Run Models
        - Run Quote Policy

    Async:
        - Log Models/Quote Outcomes
        - Run Application Policy

    Async:
        - Log Application Policy
        - Log Final Outcome

    Return Outcome


    """
    hash = hash_application(raw_request)

    request = ApplicationRequest(
        application_id=get_request_id(),  # type: ignore[arg-type]
        event_time=get_request_datetime(),  # type: ignore
        applicant_hash=hash,
        **raw_request.dict()
    )

    past_triggers = await get_policy_triggers(hash)

    prevetting_policy_outcome, _, _ = await asyncio.gather(
        prevetting_endpoint(request, past_triggers),
        post_event("application_requests", str(request.application_id), request.dict()),
        publish_message(
            {
                "application_id": str(request.application_id),
                "applicant_hash": str(request.applicant_hash),
                "gross_annual_income": request.gross_annual_income,
                "monthly_housing_costs": request.monthly_housing_costs,
                "residential_status": request.residential_status.value,
                "marital_status": request.marital_status.value,
                "employment_status": request.employment_status.value,
                "employer_name": request.employer_name,
                "loan_amount": request.loan_amount,
                "loan_term_in_months": request.loan_term_in_months,
            },
            topic_id="application_request_topic",
        ),
    )

    if await phase_outcome_decider(
        request.application_id, prevetting_policy_outcome, "prevetting"
    ):
        return application_result(prevetting_policy_outcome)

    credit_file = await mock_equifax_request(request)

    credit_variables = await calculate_credit_variables(credit_file)

    price = await risk_pricing_assigner(request, credit_variables)

    # risk_segment = await risk_segment_calculator(risk_score)

    # price = await get_pricing(risk_segment)

    min_income_required = await affordability_calculator(
        credit_variables, request, price
    )

    quotation_policy_outcome = await quotation_endpoint(
        request, credit_variables, price, min_income_required
    )

    if await phase_outcome_decider(
        request.application_id, quotation_policy_outcome, "quotation"
    ):
        return application_result(quotation_policy_outcome)

    return application_result(quotation_policy_outcome)
