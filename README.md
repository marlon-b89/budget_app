# 🧮 Braga Budget App
# Python Backend + Debt Repayment Simulator

![Python Version](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Repo Size](https://img.shields.io/github/repo-size/marlon-b89/budget_app)
![Last Commit](https://img.shields.io/github/last-commit/marlon-b89/budget_app)
![Issues](https://img.shields.io/github/issues/marlon-b89/budget_app)

A modular budgeting engine built in Python to help users organize their finances, calculate net income, analyze spending across budgeting buckets, and simulate debt repayment timelines.  

---
## 🚀 Features

### ✔ **Income Normalization**
Convert income from:
- yearly  
- monthly  
- weekly  
→ into a standardized monthly value.

### ✔ **Bucket-Based Budgeting**
Supports modern budgeting categories:
- Essentials  
- Lifestyle  
- Savings  
- Emergency Fund  
- Debt Payments  
- Giving  

### ✔ **Debt Repayment Simulator**
A full amortization engine that computes:
- monthly interest  
- principal paid  
- payoff timeline  
- updated balances  
- full payment schedule  

### ✔ **Clean Modular Architecture**
budget_app/
│
├── app.py # ready for Streamlit UI integration
├── sample_run.py # manual test harness
├── modules/
│ ├── income.py # income conversion logic
│ ├── expenses.py # budgeting buckets
│ ├── debt.py # debt payoff logic
│ ├── calculator.py # core budget aggregation
│ └── recommendations.py # (future) budgeting suggestions

---
## 📊 Example Output (from `sample_run.py`)
Monthly Income: $10833.33

Bucket Totals:
Essentials: $2500.00
Savings: $200.00
Lifestyle: $200.00
Giving: $500.00
Debt Repayments: $385.00

Total Expenses: $3585.00
Net Remaining: $7248.33

--- Debt Payoff Example ---
Chase Card will be paid off in 64 months.

---

## 🧱 Roadmap

### 🎨 **Streamlit Frontend (next major milestone)**
Interactive features coming soon:
- Enter income, expenses, and debts  
- Visualize budgets using charts (Plotly)  
- Compare Snowball vs Avalanche  
- Export payoff schedules  
- Save/load user profiles  

### 🧪 **Testing Suite (pytest)**
Unit tests for:
- income conversion  
- bucket calculations  
- debt amortization  
- recommendations  

### 📂 **CSV Import**
Upload bank transactions → auto categorize → budget instantly.

---

## 🧰 Tech Stack
- Python 3.11+  
- Object-Oriented Backend  
- Git + GitHub  
- (Upcoming) Streamlit  
- (Upcoming) Pandas & Plotly  

---

## 💼 Purpose of This Project
This project was built for:
1. **Education** — strengthening Python, finance, and modular design skills  
2. **Portfolio** — creating a real, demonstrable budgeting engine  
3. **Real-World Use** — helping individuals understand and visualize their finances  

---

## 🤝 Contributions
Issues and PRs are welcome.  

---

## 📜 License
Licensed under the MIT License.  

