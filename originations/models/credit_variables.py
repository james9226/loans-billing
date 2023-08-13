import uuid
from pydantic import BaseModel


class CreditVariables(BaseModel):
    profile_id: uuid.UUID
    document_id: uuid.UUID
    outstanding_balance: int
    outstanding_revolving_balance: int
    num_missed_payments_last_12m: int
    monthly_fixed_term_payments_excluding_mortgage: int
    monthly_mortgage_cost: int
    credit_score: int
