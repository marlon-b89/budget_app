# Converts various income periods (yearly, weekly) into monthly income

def convert_income(amount: float, period: str) -> float:
    period = period.lower()

    if period == "yearly":
        return amount / 12
    elif period == "monthly":
        return amount  # already monthly
    elif period == "weekly":
        return amount * 4.345  # average weeks per month
    elif period == "semi-monthly":
        return amount * 2
    else:
        raise ValueError("Period must be 'yearly', 'monthly', 'semi-monthly', or 'weekly'")