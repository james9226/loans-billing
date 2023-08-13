from dataclasses import dataclass
from typing import Union


@dataclass
class TaxBands:
    basic_rate = 0.2
    basic_rate_threshold = 50_270

    higher_rate = 0.4
    higher_rate_threshold = 125_140

    additional_rate = 0.45

    personal_allowance = 12_570

    personal_allowance_lower_threshold = 100_000
    personal_allowance_upper_threshold = 125_140


def net_monthly_to_gross_annual_income(net_monthly_income: float) -> float:
    if net_monthly_income < 0:
        return 0

    annual_net_income = net_monthly_income * 12

    annual_gross_income = annual_net_income

    return annual_gross_income


def tax_calculator(gross_annual_income: int) -> float:
    tax = float(0)
    taxable_income = float(gross_annual_income)

    if gross_annual_income < 0:
        return tax

    personal_allowance = (
        TaxBands.personal_allowance
        * (
            TaxBands.personal_allowance_upper_threshold
            - min(
                max(gross_annual_income, TaxBands.personal_allowance_lower_threshold),
                TaxBands.personal_allowance_upper_threshold,
            )
        )
        / (
            TaxBands.personal_allowance_upper_threshold
            - TaxBands.personal_allowance_lower_threshold
        )
    )

    taxable_income -= personal_allowance

    if taxable_income <= 0:
        return tax

    tax += TaxBands.basic_rate * min(taxable_income, TaxBands.basic_rate_threshold)

    taxable_income -= min(taxable_income, TaxBands.basic_rate_threshold)

    if taxable_income <= 0:
        return tax

    tax += TaxBands.higher_rate * min(taxable_income, TaxBands.higher_rate_threshold)

    taxable_income -= min(taxable_income, TaxBands.higher_rate_threshold)

    if taxable_income <= 0:
        return tax

    tax += TaxBands.additional_rate * taxable_income

    return tax


def gross_annual_to_net_monthly_income(gross_annual_income: int) -> int:
    if gross_annual_income < 50_270:
        pass
    return gross_annual_income
