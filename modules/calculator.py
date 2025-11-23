# Calculation engine for budgeting application

from modules.expenses import bucket_totals
from modules.debt import total_min_payments

def calculate_budget(monthly_income: float, budget: dict, debts: list):
    totals = bucket_totals(budget)

    totals["Debt Repayments"] = total_min_payments(debts)

    total_expenses = sum(totals.values())
    net = monthly_income - total_expenses

    return totals, total_expenses, net
