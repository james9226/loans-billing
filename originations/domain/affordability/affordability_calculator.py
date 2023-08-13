from typing import Optional
from originations.domain.affordability.tax.tax_calculator import (
    net_monthly_to_gross_annual_income,
)
from originations.models.application import ApplicationRequest
from originations.models.credit_variables import CreditVariables


async def affordability_calculator(
    credit_variables: CreditVariables,
    request: ApplicationRequest,
    price: Optional[float],
) -> Optional[float]:
    DI_THRESHOLD = 600
    DTI_THRESHOLD = 0.6
    MIN_INCOME = 12570

    if price is None:
        return None

    minimum_monthly_net_income_by_di = (
        DI_THRESHOLD
        + credit_variables.monthly_fixed_term_payments_excluding_mortgage
        + credit_variables.outstanding_revolving_balance * 0.06
        + max(credit_variables.monthly_mortgage_cost, request.monthly_housing_costs)
        # + monthly_quote_price
    )

    minimum_annual_gross_income_by_dti = (
        credit_variables.outstanding_balance + request.loan_amount
    ) / DTI_THRESHOLD

    min_income = max(
        MIN_INCOME,
        net_monthly_to_gross_annual_income(minimum_monthly_net_income_by_di),
        minimum_annual_gross_income_by_dti,
    )

    return min_income
