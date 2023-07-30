from pydantic import BaseModel


class LoanBalance(BaseModel):
    principal: float
    principal_pending: float
    interest: float
    expected_interest: float

    principal_1mpd: float
    interest_1mpd: float

    principal_2mpd: float
    interest_2mpd: float

    principal_3mpd: float
    interest_3mpd: float

    principal_4mpd_plus: float
    interest_4mpd_plus: float

    def total_principal_balance(self) -> float:
        return (
            self.principal
            + self.principal_pending
            + self.principal_1mpd
            + self.principal_2mpd
            + self.principal_3mpd
            + self.principal_4mpd_plus
        )

    def total_interest_balance(self) -> float:
        return (
            self.interest
            + self.interest_1mpd
            + self.interest_2mpd
            + self.interest_3mpd
            + self.interest_4mpd_plus
        )

    def total_balance(self) -> float:
        return self.total_interest_balance() + self.total_principal_balance()

    def apply_to_balance(amount: float, balance: float) -> tuple[float, float]:
        balance = max(0, balance - amount)
        amount_remaining = max(amount - balance, 0)
        return amount_remaining, balance

    def apply_payment_waterfall(
        self, amount: float, apply_to_pending: bool = True
    ) -> float:
        amount_to_be_applied = amount

        amount_to_be_applied, self.interest_4mpd_plus = self.apply_to_balance(
            amount_to_be_applied, self.interest_4mpd_plus
        )
        amount_to_be_applied, self.interest_3mpd = self.apply_to_balance(
            amount_to_be_applied, self.interest_3mpd
        )
        amount_to_be_applied, self.interest_2mpd = self.apply_to_balance(
            amount_to_be_applied, self.interest_2mpd
        )
        amount_to_be_applied, self.interest_1mpd = self.apply_to_balance(
            amount_to_be_applied, self.interest_1mpd
        )
        amount_to_be_applied, self.interest = self.apply_to_balance(
            amount_to_be_applied, self.interest
        )

        amount_to_be_applied, self.principal_4mpd_plus = self.apply_to_balance(
            amount_to_be_applied, self.principal_4mpd_plus
        )
        amount_to_be_applied, self.principal_3mpd = self.apply_to_balance(
            amount_to_be_applied, self.principal_3mpd
        )
        amount_to_be_applied, self.principal_2mpd = self.apply_to_balance(
            amount_to_be_applied, self.principal_2mpd
        )
        amount_to_be_applied, self.principal_1mpd = self.apply_to_balance(
            amount_to_be_applied, self.principal_1mpd
        )

        if apply_to_pending:
            self.principal_pending -= amount_to_be_applied
        else:
            self.principal -= amount_to_be_applied  # TODO - handle when this goes -ve

    def __sub__(self, other):
        if isinstance(other, LoanBalance):
            return LoanBalance(
                principal=self.principal - other.principal,
                interest=self.interest - other.interest,
                principal_pending=self.principal_pending - other.principal_pending,
                expected_interest=self.expected_interest - other.expected_interest,
                principal_1mpd=self.principal_1mpd - other.principal_1mpd,
                interest_1mpd=self.interest_1mpd - other.interest_1mpd,
                principal_2mpd=self.principal_2mpd - other.principal_2mpd,
                interest_2mpd=self.interest_2mpd - other.interest_2mpd,
                principal_3mpd=self.principal_3mpd - other.principal_3mpd,
                interest_3mpd=self.interest_3mpd - other.interest_3mpd,
                principal_4mpd_plus=self.principal_4mpd_plus
                - other.principal_4mpd_plus,
                interest_4mpd_plus=self.interest_4mpd_plus - other.interest_4mpd_plus,
            )
        else:
            raise TypeError(
                "Subtraction can only be performed between two LoanBalance instances."
            )
