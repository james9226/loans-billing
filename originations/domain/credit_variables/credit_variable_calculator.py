import uuid
from originations.models.credit_variables import CreditVariables


async def calculate_credit_variables(credit_file) -> CreditVariables:
    credit_variables = CreditVariables(
        profile_id=uuid.uuid4(),
        document_id=credit_file["document_id"],
        outstanding_balance=credit_file["outstanding_balance"],
        outstanding_revolving_balance=credit_file["outstanding_revolving_balance"],
        num_missed_payments_last_12m=credit_file["num_missed_payments_last_12m"],
        monthly_fixed_term_payments_excluding_mortgage=credit_file[
            "monthly_fixed_term_payments_excluding_mortgage"
        ],
        monthly_mortgage_cost=credit_file["monthly_mortgage_cost"],
        credit_score=credit_file["credit_score"],
    )

    return credit_variables
