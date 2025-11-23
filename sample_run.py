# app.py

from modules.income import convert_income
from modules.expenses import BUDGET_BUCKETS, add_expense
from modules.debt import Debt
from modules.calculator import calculate_budget

# To run the sample, execute: python budget_app.py
def run_sample():
    """Runs test routine for learning + validation."""
    monthly_income = convert_income(130000, "yearly")
    print(f"Monthly Income: ${monthly_income:.2f}")

    budget = BUDGET_BUCKETS.copy()
    add_expense("Essentials", "Rent", 2000, budget)
    add_expense("Essentials", "Groceries", 500, budget)
    add_expense("Savings", "IRA Account", 200, budget)
    add_expense("Giving", "Church", 500, budget)

    debts = [
        Debt("Chase Card", balance=4200, interest_rate=24.99, min_payment=120),
        Debt("Car Loan", balance=8500, interest_rate=7.25, min_payment=265),
    ]

    totals, total_expenses, net = calculate_budget(monthly_income, budget, debts)

    print("\nBucket Totals:")
    for k, v in totals.items():
        print(f"{k}: ${v:.2f}")

    print(f"\nTotal Expenses: ${total_expenses:.2f}")
    print(f"Net Remaining: ${net:.2f}")

    print("\n--- Debt Payoff Example ---")
    schedule = debts[0].simulate_payoff()
    print(f"{debts[0].name} will be paid off in {len(schedule)} months.")


if __name__ == "__main__":
    run_sample()
