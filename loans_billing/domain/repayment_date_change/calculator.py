from datetime import date
from uuid import UUID
from common.models.loan import Loan
from common.utils.repayment_day_calculator import add_month


def validate_first_repayment_date_change(loan: Loan, proposed_date: date) -> bool:
    if (proposed_date - loan.previous_repayment_day).days > 56:
        return False

    if (loan.first_repayment_date - proposed_date).days > 7:
        return True
    return False


def validate_second_repayment_date_change(loan: Loan, proposed_date: date) -> bool:
    if (proposed_date - loan.first_repayment_date).days < 20:
        return False

    if (proposed_date - loan.first_repayment_date).days > 56:
        return False

    return True


def calculate_new_repayment_day(loan: Loan, new_day: int, event_id: UUID) -> Loan:
    for i in range(0, 2):
        # TODO - messy logic here

        proposed_date = date(
            loan.first_repayment_date.year,
            loan.first_repayment_date.month + i,
            new_day,
        )

        if (loan.first_repayment_date - proposed_date).days > 7:
            loan.first_repayment_date = proposed_date
            loan.second_next_repayment_date = add_month(proposed_date, 1)
