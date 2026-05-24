# ============================================================
# PROJECT 2: A/B Testing & Hypothesis Testing
# Rhombix Technologies Internship
# ============================================================

import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

np.random.seed(42)

# ============================================================
# STEP 1: Dataset Banana (Campaign A vs Campaign B)
# ============================================================

n = 100  # har campaign mein 100 users

campaign_a = {
    'user_id': range(1, n + 1),
    'campaign': 'Campaign A',
    'age': np.random.randint(18, 55, n),
    'clicks': np.random.poisson(5, n),
    'time_spent_min': np.random.normal(8, 2, n).round(2),
    'purchase_amount': np.random.normal(3000, 500, n).round(2),
    'converted': np.random.choice([0, 1], n, p=[0.55, 0.45])  # 45% conversion
}

campaign_b = {
    'user_id': range(n + 1, 2 * n + 1),
    'campaign': 'Campaign B',
    'age': np.random.randint(18, 55, n),
    'clicks': np.random.poisson(7, n),
    'time_spent_min': np.random.normal(10, 2, n).round(2),
    'purchase_amount': np.random.normal(3500, 500, n).round(2),
    'converted': np.random.choice([0, 1], n, p=[0.40, 0.60])  # 60% conversion
}

df_a = pd.DataFrame(campaign_a)
df_b = pd.DataFrame(campaign_b)
df = pd.concat([df_a, df_b], ignore_index=True)

print("=" * 60)
print("STEP 1: Dataset Overview")
print("=" * 60)
print(f"\nTotal Records: {len(df)}")
print(f"Campaign A Users: {len(df_a)}")
print(f"Campaign B Users: {len(df_b)}")
print("\nSample Data (first 5 rows):")
print(df.head().to_string(index=False))

# ============================================================
# STEP 2: Descriptive Statistics
# ============================================================

print("\n" + "=" * 60)
print("STEP 2: Descriptive Statistics")
print("=" * 60)

summary = df.groupby('campaign').agg(
    avg_clicks=('clicks', 'mean'),
    avg_time_spent=('time_spent_min', 'mean'),
    avg_purchase=('purchase_amount', 'mean'),
    conversion_rate=('converted', 'mean'),
    total_users=('user_id', 'count')
).round(3)

summary['conversion_rate'] = (summary['conversion_rate'] * 100).round(2)
summary = summary.rename(columns={'conversion_rate': 'conversion_rate_%'})
print(summary.to_string())

# ============================================================
# STEP 3: T-Test (Purchase Amount compare karna)
# ============================================================

print("\n" + "=" * 60)
print("STEP 3: Independent T-Test")
print("(Campaign A vs B - Purchase Amount)")
print("=" * 60)

t_stat, p_value = stats.ttest_ind(
    df_a['purchase_amount'],
    df_b['purchase_amount']
)

print(f"\n  H0 (Null Hypothesis):        Dono campaigns ka avg purchase same hai")
print(f"  H1 (Alternate Hypothesis):   Campaigns ka avg purchase alag hai")
print(f"\n  T-Statistic:  {t_stat:.4f}")
print(f"  P-Value:      {p_value:.4f}")

if p_value < 0.05:
    print(f"\n   Result: P < 0.05 → Null Hypothesis REJECT")
    print(f"   Conclusion: Dono campaigns ka purchase amount significantly alag hai!")
else:
    print(f"\n   Result: P > 0.05 → Null Hypothesis ACCEPT")
    print(f"   Conclusion: Koi significant difference nahi hai.")

# ============================================================
# STEP 4: Chi-Square Test (Conversion Rate compare karna)
# ============================================================

print("\n" + "=" * 60)
print("STEP 4: Chi-Square Test")
print("(Campaign A vs B - Conversion Rate)")
print("=" * 60)

# Contingency table banana
converted_a = df_a['converted'].sum()
not_converted_a = len(df_a) - converted_a
converted_b = df_b['converted'].sum()
not_converted_b = len(df_b) - converted_b

contingency_table = np.array([
    [converted_a, not_converted_a],
    [converted_b, not_converted_b]
])

print(f"\n  Contingency Table:")
print(f"  {'':15} {'Converted':>12} {'Not Converted':>15}")
print(f"  {'Campaign A':15} {converted_a:>12} {not_converted_a:>15}")
print(f"  {'Campaign B':15} {converted_b:>12} {not_converted_b:>15}")

chi2, p_chi, dof, expected = stats.chi2_contingency(contingency_table)

print(f"\n  H0: Conversion rate dono campaigns mein same hai")
print(f"  H1: Conversion rate mein significant difference hai")
print(f"\n  Chi2 Statistic: {chi2:.4f}")
print(f"  P-Value:        {p_chi:.4f}")
print(f"  Degrees of Freedom: {dof}")

if p_chi < 0.05:
    print(f"\n   Result: P < 0.05 → Null Hypothesis REJECT")
    print(f"   Conclusion: Conversion rate mein significant difference hai!")
else:
    print(f"\n   Result: P > 0.05 → Null Hypothesis ACCEPT")
    print(f"   Conclusion: Conversion rate mein koi significant difference nahi.")

# ============================================================
# STEP 5: ANOVA Test (Time Spent - Age Groups)
# ============================================================

print("\n" + "=" * 60)
print("STEP 5: ANOVA Test")
print("(Time Spent - Age Groups compare karna)")
print("=" * 60)

# Age groups banana
def age_group(age):
    if age < 25:
        return 'Young (18-24)'
    elif age < 35:
        return 'Adult (25-34)'
    elif age < 45:
        return 'Middle (35-44)'
    else:
        return 'Senior (45+)'

df['age_group'] = df['age'].apply(age_group)

groups = [group['time_spent_min'].values
          for name, group in df.groupby('age_group')]

f_stat, p_anova = stats.f_oneway(*groups)

age_summary = df.groupby('age_group')['time_spent_min'].mean().round(2)
print(f"\n  Avg Time Spent per Age Group:")
for group, val in age_summary.items():
    print(f"  {group:20}: {val} mins")

print(f"\n  H0: Sab age groups ka avg time spent same hai")
print(f"  H1: Kam az kam ek group alag hai")
print(f"\n  F-Statistic: {f_stat:.4f}")
print(f"  P-Value:     {p_anova:.4f}")

if p_anova < 0.05:
    print(f"\n   Result: P < 0.05 → Null Hypothesis REJECT")
    print(f"   Conclusion: Age groups mein time spent significantly alag hai!")
else:
    print(f"\n   Result: P > 0.05 → Null Hypothesis ACCEPT")
    print(f"   Conclusion: Age groups mein time spent same hai.")

# ============================================================
# STEP 6: Final Recommendation
# ============================================================

print("\n" + "=" * 60)
print("STEP 6: Final Business Recommendation")
print("=" * 60)

avg_purchase_a = df_a['purchase_amount'].mean()
avg_purchase_b = df_b['purchase_amount'].mean()
conv_a = df_a['converted'].mean() * 100
conv_b = df_b['converted'].mean() * 100

print(f"""
  Campaign A:
    → Avg Purchase:     Rs. {avg_purchase_a:,.2f}
    → Conversion Rate:  {conv_a:.1f}%

  Campaign B:
    → Avg Purchase:     Rs. {avg_purchase_b:,.2f}
    → Conversion Rate:  {conv_b:.1f}%
""")

if avg_purchase_b > avg_purchase_a and conv_b > conv_a:
    print("   WINNER: Campaign B")
    print("   Campaign B ka purchase amount aur conversion rate")
    print("     dono Campaign A se behtar hain.")
    print("     Business ko Campaign B adopt karna chahiye!")
else:
    print("   WINNER: Campaign A")
    print("   Campaign A better perform kar raha hai.")

# ============================================================
# STEP 7: Results Save Karna
# ============================================================

df.to_csv('ab_testing_full_data.csv', index=False)
summary.to_csv('campaign_summary.csv')

print("\n\n Files save ho gayi hain:")
print("   → ab_testing_full_data.csv")
print("   → campaign_summary.csv")
print("\n" + "=" * 60)
