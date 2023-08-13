from originations.enums.policy import PolicyOutcome, PolicyRuleResult
from originations.services.logging import log_handler


class PolicyRuleComplete:
    def __init__(
        self,
        rule_name: str,
        result: PolicyRuleResult,
        reason: str,
        triggered_outcome: PolicyOutcome,
        errored_outcome: PolicyOutcome,
    ):
        self.rule_name = rule_name
        self.result = result
        self.reason = reason
        self.triggered_outcome = triggered_outcome
        self.errored_outcome = errored_outcome
        self.outcome = self.get_policy_outcome()
        log_handler.info(
            f"rule={rule_name}, result={result} reason={reason} outcome={self.outcome}"
        )

    def get_policy_outcome(self):
        if self.result == PolicyRuleResult.TRIGGERED:
            return self.triggered_outcome
        elif self.result == PolicyRuleResult.ERRORED:
            return self.errored_outcome
        elif self.result == PolicyRuleResult.NOT_TRIGGERED:
            return PolicyOutcome.PASSED
        else:
            log_handler.critical("Policy rule completed without result!")
            return PolicyOutcome.DECLINED_DUE_TO_TECHNCAL_ERROR
