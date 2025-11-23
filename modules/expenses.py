# Organization of expense categories into budget buckets
BUDGET_BUCKETS = {
    "Essentials": {},
    "Lifestyle": {},
    "Savings": {},
    "Investments": {},
    "Emergency Fund": {},
    "Giving": {},
    "Debt Repayments": {}
}

def create_empty_budget() -> dict:

    return {bucket: {} for bucket in BUDGET_BUCKETS.keys()}


# Function to add an expense to a specific budget bucket
def add_expense(bucket: str, name: str, amount: float, budget: dict):
    """
    Adds an expense entry into the *given* budget dict,
    not the global BUDGET_BUCKETS template.
    """
    if bucket not in budget:
        raise ValueError(f"Bucket '{bucket}' does not exist in this budget.")

    budget[bucket][name] = amount

# Returns a dictionary with summed totals for each budget bucket
def bucket_totals(budget: dict) -> dict:
    """
    Summarize the total amount per bucket in the given budget.
    """
    return {bucket: sum(items.values()) for bucket, items in budget.items()}