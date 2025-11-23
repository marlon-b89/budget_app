# Building debt management module

class Debt:
    def __init__(self, name: str, balance: float, interest_rate: float, min_payment: float, extra_payment: float = 0):
        self.name = name
        self.balance = balance
        self.interest_rate = interest_rate  # APR as a percentage, e.g. 24.99
        self.min_payment = min_payment
        self.extra_payment = extra_payment

    @property
    def monthly_interest_rate(self) -> float:
        """
        Convert APR (%) to a monthly rate as a decimal.
        Example: 24% APR -> 0.02 monthly rate
        """
        return self.interest_rate / 100 / 12

    def simulate_payoff(self):
        """
        Simulates a month-by-month payoff schedule until the balance is zero.
        Returns a list of dicts, one for each month.
        """
        payment_schedule = []
        month = 1
        balance = self.balance

        # Safety guard: avoid infinite loops
        while balance > 0 and month < 1000:
            interest = balance * self.monthly_interest_rate
            # Total payment this month, but not more than needed
            payment = min(self.min_payment + self.extra_payment, balance + interest)
            principal = payment - interest
            balance -= principal

            payment_schedule.append({
                "month": month,
                "payment": round(payment, 2),
                "interest": round(interest, 2),
                "principal": round(principal, 2),
                "balance": round(balance, 2),
            })

            month += 1

        return payment_schedule


# Sums the minimum payments for all debts
def total_min_payments(debts: list) -> float:
    return sum(d.min_payment for d in debts)
