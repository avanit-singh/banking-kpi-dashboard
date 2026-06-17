# ================================================================
# Banking KPI Dashboard & Executive Reporting
# Author  : Avanit Singh
# Stack   : Python (Pandas) | SQL | Power BI | Excel
# Purpose : Track CASA growth, loan KPIs, branch performance
# ================================================================

import pandas as pd
warnings.filterwarnings('ignore')
import warnings

# ── 1. Load Data ─────────────────────────────────────────────
df = pd.read_csv('data/banking_kpi.csv')
df['month'] = pd.to_datetime(df['month'])

print(f"✅ Data loaded: {len(df)} records across {df['branch_name'].nunique()} branches")
print(f"\n📋 Preview:")
print(df.head())

# ── 2. CASA Growth Analysis ──────────────────────────────────
df['casa_growth']     = df['casa_closing_bal'] - df['casa_opening_bal']
df['casa_growth_pct'] = (df['casa_growth'] / df['casa_opening_bal'] * 100).round(2)

total_casa_growth = df['casa_growth'].sum()
avg_growth_rate   = df['casa_growth_pct'].mean()

print(f"\n{'='*55}")
print(f"📊 CASA GROWTH ANALYSIS")
print(f"{'='*55}")
print(f"Total CASA Growth (All Branches, 3 months) : INR {total_casa_growth:>15,.0f}")
print(f"Average Monthly CASA Growth Rate           : {avg_growth_rate:.2f}%")

branch_casa = df.groupby('branch_name').agg(
    Total_CASA_Growth=('casa_growth', 'sum'),
    Avg_Growth_Rate=('casa_growth_pct', 'mean')
).reset_index()
branch_casa['Avg_Growth_Rate'] = branch_casa['Avg_Growth_Rate'].round(2)
print(f"\nCASA Growth by Branch:")
print(branch_casa.sort_values('Total_CASA_Growth', ascending=False).to_string(index=False))

# ── 3. Loan Disbursement KPIs ─────────────────────────────
df['approval_rate'] = (df['loan_approvals'] / df['loan_applications'] * 100).round(1)

total_apps      = df['loan_applications'].sum()
total_approvals = df['loan_approvals'].sum()
total_disbursed = df['loan_disbursed_amt'].sum()
avg_approval    = df['approval_rate'].mean()

print(f"\n{'='*55}")
print(f"📊 LOAN DISBURSEMENT KPIs")
print(f"{'='*55}")
print(f"Total Applications    : {total_apps:,}")
print(f"Total Approvals       : {total_approvals:,}")
print(f"Average Approval Rate : {avg_approval:.1f}%")
print(f"Total Disbursed       : INR {total_disbursed:>15,.0f}")

loan_branch = df.groupby('branch_name').agg(
    Applications=('loan_applications', 'sum'),
    Approvals=('loan_approvals', 'sum'),
    Disbursed=('loan_disbursed_amt', 'sum'),
    Approval_Rate=('approval_rate', 'mean')
).reset_index()
loan_branch['Approval_Rate'] = loan_branch['Approval_Rate'].round(1)
print(f"\nLoan KPIs by Branch:")
print(loan_branch.sort_values('Disbursed', ascending=False).to_string(index=False))

# ── 4. Customer Acquisition & Cross-Sell ────────────────────
total_acq       = df['customer_acquisitions'].sum()
total_new_accts = df['new_accounts'].sum()
total_crosssell = df['cross_sell_count'].sum()
df['cross_sell_rate'] = (df['cross_sell_count'] / df['customer_acquisitions'] * 100).round(1)
avg_cross_rate  = df['cross_sell_rate'].mean()

print(f"\n{'='*55}")
print(f"📊 CUSTOMER ACQUISITION & PRODUCT PENETRATION")
print(f"{'='*55}")
print(f"Total New Accounts Opened  : {total_new_accts:,}")
print(f"Total Customer Acquisitions: {total_acq:,}")
print(f"Total Cross-Sell Count     : {total_crosssell:,}")
print(f"Average Cross-Sell Rate    : {avg_cross_rate:.1f}%")

# ── 5. Revenue Analysis ──────────────────────────────────────
total_revenue    = df['revenue'].sum()
monthly_rev      = df.groupby('month')['revenue'].sum().reset_index()
monthly_rev.columns = ['Month', 'Revenue']
monthly_rev['Revenue'] = monthly_rev['Revenue'].apply(lambda x: f"INR {x:,.0f}")

print(f"\n{'='*55}")
print(f"📊 REVENUE ANALYSIS")
print(f"{'='*55}")
print(f"Total Revenue (All Branches, 3 months) : INR {total_revenue:>12,.0f}")
print(f"\nMonthly Revenue Trend:")
print(monthly_rev.to_string(index=False))

# ── 6. Branch Performance Scorecard ─────────────────────────
branch_score = df.groupby('branch_name').agg(
    CASA_Growth=('casa_growth', 'sum'),
    Loans_Disbursed=('loan_disbursed_amt', 'sum'),
    Customers_Acquired=('customer_acquisitions', 'sum'),
    Cross_Sells=('cross_sell_count', 'sum'),
    Total_Revenue=('revenue', 'sum')
).reset_index()

print(f"\n{'='*55}")
print(f"📊 BRANCH PERFORMANCE SCORECARD")
print(f"{'='*55}")
print(branch_score.sort_values('Total_Revenue', ascending=False).to_string(index=False))

top_branch = branch_score.loc[branch_score['Total_Revenue'].idxmax(), 'branch_name']
print(f"\n🏆 Top Performing Branch : {top_branch}")
print(f"\n✅ Banking KPI Analysis completed successfully.")
