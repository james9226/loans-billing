import calendar
from datetime import timedelta
from decimal import Decimal
from common.enums.tx_keys import TransactionKey
from common.models.cloudsql_sqlmodel_models import Loan
from dateutil.relativedelta import relativedelta


def calculate_daily_interest_rate(loan: Loan) -> Decimal:
    monthly_interest_rate = loan.apr / 12

    days_in_period = (loan.first_repayment_date - loan.previous_repayment_date).days
    next_month_same_day = loan.previous_repayment_date + relativedelta(months=1)

    # Check if next month on the same day is exactly the first_repayment_date
    if next_month_same_day == loan.first_repayment_date:
        # Use the actual number of days in the previous_repayment_date's month
        _, days_in_actual_month = calendar.monthrange(
            loan.previous_repayment_date.year, loan.previous_repayment_date.month
        )
        daily_interest_rate = monthly_interest_rate / days_in_actual_month
    else:
        # Otherwise, use the standard (1/365) rate
        daily_interest_rate = loan.apr / 365

    return daily_interest_rate


def calculate_interest_to_accrue(loan: Loan, daily_interest_rate: Decimal) -> Decimal:
    principal_balance = (
        loan.get_balance_by_key(TransactionKey.PRINCIPAL)
        + loan.get_balance_by_key(TransactionKey.PRINCIPAL_AMOUNT_TO_COVER_INTEREST)
        + loan.get_balance_by_key(TransactionKey.PRINCIPAL_DUE)
    )

    return max(0, principal_balance * daily_interest_rate)
