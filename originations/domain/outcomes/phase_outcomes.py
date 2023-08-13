from datetime import datetime
from originations.enums.policy import PolicyOutcome
from originations.services.logging import log_handler
from originations.services.pubsub.async_publisher import publish_message


async def phase_outcome_decider(application_id, policy_outcome, phase):
    declined_outcomes = [
        PolicyOutcome.DECLINED,
        PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR,
        PolicyOutcome.DECLINED_WITH_REAPPLICATION_ALLOWED,
    ]

    await publish_message(
        {
            "reference_id": str(application_id),
            "phase": phase,
            "outcome": policy_outcome,
        },
        "phase_outcomes_topic",
    )

    if policy_outcome in declined_outcomes:
        log_handler.info(
            f"Evaluated a {policy_outcome} outcome at phase {phase} - stopping application"
        )
        return True
    log_handler.info(f"Evaluated a pass outcome at phase {phase}")
    return False
