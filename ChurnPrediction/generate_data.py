"""
generate_data.py
-----------------
Creates a realistic synthetic customer dataset for churn prediction.
Saves the output as 'customer_churn_data.csv' in the same directory.
"""

import os
import numpy as np
import pandas as pd

np.random.seed(42)

NUM_CUSTOMERS = 2000

# --- Helper functions --------------------------------------------------------

def _random_choice(options, size, probs=None):
    return np.random.choice(options, size=size, p=probs)


def generate_dataset(n: int = NUM_CUSTOMERS) -> pd.DataFrame:
    """Generate a synthetic customer churn dataset."""

    customer_id = [f"CUST-{i:05d}" for i in range(1, n + 1)]

    # Demographics
    age = np.random.randint(18, 70, size=n)
    gender = _random_choice(["Male", "Female"], n)

    # Subscription info
    tenure_months = np.random.randint(1, 72, size=n)
    contract_type = _random_choice(
        ["Month-to-Month", "One-Year", "Two-Year"], n, probs=[0.50, 0.30, 0.20]
    )
    monthly_charge = np.round(np.random.uniform(20, 120, size=n), 2)
    total_charges = np.round(monthly_charge * tenure_months + np.random.normal(0, 50, n), 2)
    total_charges = np.clip(total_charges, 0, None)

    # Usage & engagement
    num_support_tickets = np.random.poisson(lam=1.5, size=n)
    avg_monthly_usage_hrs = np.round(np.random.uniform(0.5, 300, size=n), 1)
    num_referrals = np.random.poisson(lam=0.8, size=n)

    # Service features
    has_premium_support = _random_choice([0, 1], n, probs=[0.65, 0.35])
    has_online_backup = _random_choice([0, 1], n, probs=[0.55, 0.45])
    payment_method = _random_choice(
        ["Credit Card", "Bank Transfer", "Digital Wallet", "Cash"],
        n,
        probs=[0.35, 0.25, 0.25, 0.15],
    )

    # --- Generate churn label (target) based on realistic rules ---------------
    churn_prob = np.zeros(n)

    # Higher churn for month-to-month contracts
    churn_prob += np.where(np.array(contract_type) == "Month-to-Month", 0.25, -0.10)

    # Short tenure -> higher churn
    churn_prob += np.where(tenure_months < 12, 0.15, -0.05)

    # High monthly charges -> more churn
    churn_prob += np.where(monthly_charge > 80, 0.10, -0.05)

    # Many support tickets -> frustrated customer
    churn_prob += np.where(num_support_tickets >= 3, 0.15, 0.0)

    # Low usage -> likely to churn
    churn_prob += np.where(avg_monthly_usage_hrs < 30, 0.12, -0.05)

    # Premium support reduces churn
    churn_prob += np.where(has_premium_support == 1, -0.10, 0.05)

    # Add noise
    churn_prob += np.random.normal(0, 0.08, n)

    # Clamp and convert to binary
    churn_prob = np.clip(churn_prob, 0.05, 0.95)
    churned = (np.random.rand(n) < churn_prob).astype(int)

    # --- Build DataFrame -------------------------------------------------------
    df = pd.DataFrame({
        "CustomerID": customer_id,
        "Age": age,
        "Gender": gender,
        "Tenure_Months": tenure_months,
        "Contract_Type": contract_type,
        "Monthly_Charge": monthly_charge,
        "Total_Charges": total_charges,
        "Num_Support_Tickets": num_support_tickets,
        "Avg_Monthly_Usage_Hrs": avg_monthly_usage_hrs,
        "Num_Referrals": num_referrals,
        "Has_Premium_Support": has_premium_support,
        "Has_Online_Backup": has_online_backup,
        "Payment_Method": payment_method,
        "Churned": churned,
    })

    return df


if __name__ == "__main__":
    df = generate_dataset()
    out_path = os.path.join(os.path.dirname(__file__), "customer_churn_data.csv")
    df.to_csv(out_path, index=False)
    print(f"Dataset saved to: {out_path}")
    print(f"Shape: {df.shape}")
    print(f"\nChurn distribution:\n{df['Churned'].value_counts()}")
    print(f"\nSample rows:\n{df.head()}")
