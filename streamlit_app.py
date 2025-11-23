import io
import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

from modules.income import convert_income
from modules.expenses import create_empty_budget, add_expense
from modules.debt import Debt
from modules.calculator import calculate_budget


# -----------------------------------------------------------
# PAGE CONFIG & HEADER
# -----------------------------------------------------------

st.set_page_config(
    page_title="Budget App",
    page_icon="🧮",
    layout="wide",
)

st.title("🧮 Budget App 📱")
st.write("Itemized budgeting and debt payoff visualizer built with Python + Streamlit by Marlon R. Braga")
st.write("The plans of the diligent lead surely to abundance, but those of everyone who is hasty surely to poverty. — Proverbs 21:5")

st.markdown("---")


# -----------------------------------------------------------
# INCOME INPUT (MAIN PAGE)
# -----------------------------------------------------------

st.subheader("💵 Income Information")

col_income_1, col_income_2 = st.columns([1, 1])

with col_income_1:
    income_amount = st.number_input(
        "Income Amount",
        min_value=0.0,
        value=130000.0,
        step=1000.0,
    )

with col_income_2:
    income_period = st.selectbox(
        "Income Period",
        ["yearly", "monthly", "weekly", "semi-monthly"],
        index=0,
    )

monthly_income = convert_income(income_amount, income_period)
st.markdown(f"### 📅 Monthly Income (Calculated): **${monthly_income:,.2f}**")

st.markdown("---")

# -----------------------------------------------------------
# SIDEBAR INPUT SECTIONS
# -----------------------------------------------------------

st.sidebar.title("⚙️ Budget Inputs")
st.sidebar.subheader("Use this section to input your budget details into the respective buckets and debts.")

# Predefined buckets
BUCKET_NAMES = [
    "Essentials",
    "Lifestyle",
    "Savings",
    "Investments",
    "Emergency Fund",
    "Giving",
]

# Collect bucket inputs
manual_bucket_totals = {name: 0.0 for name in BUCKET_NAMES}

with st.sidebar.expander("📦 Budget Buckets (Itemized)", expanded=False):

    for bucket in BUCKET_NAMES:

        st.markdown(f"### {bucket}")

        num_items = st.number_input(
            f"Number of items for {bucket}",
            min_value=0,
            max_value=30,
            value=0,
            step=1,
            key=f"{bucket}_count",
        )

        bucket_total = 0.0

        for i in range(int(num_items)):
            col1, col2 = st.columns([2, 1])

            with col1:
                item_name = st.text_input(
                    f"{bucket} Item #{i+1}",
                    key=f"{bucket}_name_{i}",
                )

            with col2:
                amount = st.number_input(
                    f"{bucket} Amount #{i+1}",
                    min_value=0.0,
                    step=10.0,
                    key=f"{bucket}_amount_{i}",
                )

            bucket_total += amount

        manual_bucket_totals[bucket] = bucket_total
        st.markdown(f"Subtotal: **${bucket_total:,.2f}**")
        st.markdown("---")


# -----------------------------------------------------------
# SIDEBAR — DEBT SECTION
# -----------------------------------------------------------

debts: list[Debt] = []
payoff_rows = []

with st.sidebar.expander("💳 Debts", expanded=False):
    num_debts = st.number_input(
        "How many debts?",
        min_value=0,
        max_value=20,
        value=0,
    )

    for i in range(int(num_debts)):
        st.markdown(f"### Debt #{i+1}")

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            name = st.text_input(
                f"Debt #{i+1} Name",
                value=f"Debt {i+1}",
                key=f"debt_name_{i}",
            )

        with c2:
            balance = st.number_input(
                f"Balance #{i+1}",
                min_value=0.0,
                step=50.0,
                key=f"debt_balance_{i}",
            )

        with c3:
            apr = st.number_input(
                f"APR % #{i+1}",
                min_value=0.0,
                max_value=100.0,
                step=0.1,
                key=f"debt_apr_{i}",
            )

        with c4:
            min_payment = st.number_input(
                f"Min Pay #{i+1}",
                min_value=0.0,
                step=10.0,
                key=f"debt_min_{i}",
            )

        with c5:
            extra_payment = st.number_input(
                f"Extra Pay #{i+1}",
                min_value=0.0,
                step=10.0,
                key=f"debt_extra_{i}",
            )

        if balance > 0 and (min_payment > 0 or extra_payment > 0):
            debts.append(
                Debt(
                    name=name,
                    balance=balance,
                    interest_rate=apr,
                    min_payment=min_payment,
                    extra_payment=extra_payment,
                )
            )


# -----------------------------------------------------------
# CALCULATION
# -----------------------------------------------------------

budget = create_empty_budget()

for bucket, total in manual_bucket_totals.items():
    if total > 0:
        add_expense(bucket, "Total", total, budget)

totals, total_expenses, net = calculate_budget(
    monthly_income=monthly_income,
    budget=budget,
    debts=debts,
)

# Build summary df
bucket_data = []
for bucket_name, amount in totals.items():
    pct = (amount / monthly_income * 100) if monthly_income > 0 else 0
    bucket_data.append(
        {"Bucket": bucket_name, "Amount": amount, "% of Income": round(pct, 2)}
    )
df_summary = pd.DataFrame(bucket_data).sort_values("Amount", ascending=False)


# -----------------------------------------------------------
# PDF BUILDER
# -----------------------------------------------------------

def build_pdf(df_buckets: pd.DataFrame, df_debts: pd.DataFrame,
              monthly_income: float, total_expenses: float, net: float) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)

    # Page 1 — Summary
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Budget Summary", ln=1)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Monthly Income: ${monthly_income:,.2f}", ln=1)
    pdf.cell(0, 8, f"Total Expenses: ${total_expenses:,.2f}", ln=1)
    pdf.cell(0, 8, f"Net Remaining: ${net:,.2f}", ln=1)
    pdf.ln(4)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Bucket Breakdown", ln=1)
    pdf.set_font("Arial", "", 11)

    for _, row in df_buckets.iterrows():
        pdf.cell(
            0,
            6,
            f"{row['Bucket']}: ${row['Amount']:,.2f} ({row['% of Income']}%)",
            ln=1,
        )

    # Page 2 — Debts
    if len(df_debts) > 0:
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Debt Payoff Overview", ln=1)
        pdf.set_font("Arial", "", 11)

        for _, row in df_debts.iterrows():
            pdf.cell(0, 6, f"Debt: {row['Debt']}", ln=1)
            pdf.cell(
                0,
                6,
                f"  Balance: ${row['Balance']:,.2f} | APR: {row['APR %']}% | Min: ${row['Min Payment']:,.2f} | Extra: ${row['Extra Payment']:,.2f}",
                ln=1,
            )
            pdf.cell(
                0,
                6,
                f"  Months to Payoff: {row['Months to Payoff']} | Total Interest: ${row['Total Interest Paid']:,.2f}",
                ln=1,
            )
            pdf.ln(1)

    return pdf.output(dest='S').encode('latin-1')


# Debt payoff df
payoff_rows = []
for d in debts:
    schedule = d.simulate_payoff()
    total_interest = sum(m["interest"] for m in schedule)
    payoff_rows.append(
        {
            "Debt": d.name,
            "Balance": d.balance,
            "APR %": d.interest_rate,
            "Min Payment": d.min_payment,
            "Extra Payment": d.extra_payment,
            "Months to Payoff": len(schedule),
            "Total Interest Paid": round(total_interest, 2),
        }
    )
df_payoff = pd.DataFrame(payoff_rows)

pdf_bytes = build_pdf(df_summary, df_payoff, monthly_income, total_expenses, net)


# -----------------------------------------------------------
# DASHBOARD (MAIN PAGE)
# -----------------------------------------------------------

st.header("📊 Full Budget Summary")

dash_col1, dash_col2, dash_col3, dash_col4 = st.columns([1.3, 1.3, 1.3, 1])

# Colored metric helper
def colored_metric(label, value, style):
    colors = {
        "good": "#28a745",
        "warn": "#ffc107",
        "bad": "#dc3545",
        "neutral": "#212529",
    }
    color = colors[style]
    st.markdown(
        f"""
        <div style="padding:3px">
            <div style="font-size:0.8rem; color:#6c757d">{label}</div>
            <div style="font-size:1.5rem; font-weight:bold; color:{color}">
                ${value:,.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with dash_col1:
    colored_metric("Monthly Income", monthly_income, "neutral")

with dash_col2:
    exp_style = (
        "bad" if total_expenses > monthly_income else
        "warn" if total_expenses > monthly_income * 0.9 else
        "neutral"
    )
    colored_metric("Total Expenses", total_expenses, exp_style)

with dash_col3:
    if net < 0:
        net_style = "bad"
    elif monthly_income > 0 and net < monthly_income * 0.1:
        net_style = "warn"
    else:
        net_style = "good"
    colored_metric("Net Remaining", net, net_style)

with dash_col4:
    st.download_button(
        label="📥 Download PDF",
        data=pdf_bytes,
        file_name="budget_summary.pdf",
        mime="application/pdf",
    )


# -----------------------------------------------------------
# BUCKET BREAKDOWN & CHART
# -----------------------------------------------------------

st.subheader("📦 Bucket Breakdown")
st.dataframe(df_summary.reset_index(drop=True), use_container_width=True)

# Bar chart with readable labels
fig = px.bar(df_summary, x="Bucket", y="Amount")
fig.update_layout(
    xaxis_title="Bucket",
    yaxis_title="Amount",
    xaxis_tickangle=-30,
    margin=dict(l=10, r=10, t=10, b=10),
)
st.plotly_chart(fig, use_container_width=True)


# -----------------------------------------------------------
# DEBT PAYOFF SUMMARY (OPTIONAL)
# -----------------------------------------------------------

if len(df_payoff) > 0:
    st.subheader("💳 Debt Payoff Overview")
    st.dataframe(df_payoff.reset_index(drop=True), use_container_width=True)