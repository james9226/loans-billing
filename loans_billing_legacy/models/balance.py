from pydantic import BaseModel


class LoanBalance(BaseModel):
    principal_: float
    interest: float

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
            self.principal_
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

    def apply_payment_waterfall(self, amount: float) -> float:
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
        amount_to_be_applied, self.principal = self.apply_to_balance(
            amount_to_be_applied, self.principal
        )
