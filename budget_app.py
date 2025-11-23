"""
budget_app.py

Backend entry / integration point for the budgeting application.

All core logic lives in the modules/ package:
- income.py         (income normalization)
- expenses.py       (budget buckets)
- debt.py           (debt payoff simulation)
- calculator.py     (aggregates income, expenses, and debts)

This file intentionally does not contain any test/demo code or
user input handling. For manual testing, use sample_run.py.
For the UI, run streamlit_app.py.
"""

def main():
    print("Budget app backend ready. Use `streamlit run streamlit_app.py` for the UI, or `python sample_run.py` for tests.")


if __name__ == "__main__":
    main()