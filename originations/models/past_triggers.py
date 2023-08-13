from datetime import datetime
from pydantic import BaseModel
from originations.enums.policy import PolicyPhase


class PastPolicyTrigger(BaseModel):
    rule: str
    phase: PolicyPhase
    event_time: datetime
