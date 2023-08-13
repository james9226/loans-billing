import asyncio
from originations.models.application import ApplicationRequest
from originations.domain.policy.phase_config.prevetting import PREVETTING_RULES
from originations.domain.policy.models.policy_rule_runner import (
    PolicyRuleRunner,
)
from originations.models.past_triggers import PastPolicyTrigger


async def prevetting_endpoint(
    request: ApplicationRequest, past_triggers: list[PastPolicyTrigger]
):
    policy_rules = PolicyRuleRunner(
        request.application_id, request.applicant_hash, PREVETTING_RULES, "prevetting"
    )

    policy_rules.run_policy_rules(
        application_request=request, past_triggers=past_triggers
    )

    _, _, outcome = await asyncio.gather(
        policy_rules.save_policy_outcomes(),
        policy_rules.save_policy_triggers(),
        policy_rules.get_final_policy_outcome(),
    )

    return outcome
