import pandas as pd
import os

# Read datasets
users = pd.read_csv("data/users.csv")
expenses = pd.read_csv("data/expenses.csv")

# Convert date
expenses["date"] = pd.to_datetime(expenses["date"])

# Extract month
expenses["month"] = expenses["date"].dt.to_period("M")

# Monthly expense per user
monthly = (
    expenses.groupby(["user_id", "month"])["amount"]
    .sum()
    .reset_index()
)

# Merge with users
summary = monthly.merge(users, on="user_id")

# Savings
summary["savings"] = (
    summary["monthly_income"] -
    summary["amount"]
)

# Alert

def check_alert(row):
    if row["amount"] > row["monthly_income"] * 0.30:
        return "High Spending"
    return "Normal"

summary["alert"] = summary.apply(check_alert, axis=1)

summary.rename(columns={
    "amount":"monthly_expense"
}, inplace=True)

os.makedirs("output", exist_ok=True)

summary.to_csv(
    "output/monthly_report.csv",
    index=False
)

print(summary)

print("\nExpense Analysis Completed Successfully\n")

# Print Alerts

alerts = summary[
    summary["alert"]=="High Spending"
]

if len(alerts)>0:

    print("Savings Alerts")

    for _,row in alerts.iterrows():

        print(
            f"{row['user_name']} exceeded spending threshold."
        )

else:

    print("No alerts generated.")