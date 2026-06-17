-- ============================================================
-- Banking KPI Dashboard — SQL Queries
-- Author: Avanit Singh
-- ============================================================

-- 1. CASA Growth by Branch
SELECT
    branch_name,
    SUM(casa_closing_bal - casa_opening_bal)                            AS total_casa_growth,
    ROUND(AVG((casa_closing_bal - casa_opening_bal)
          * 100.0 / casa_opening_bal), 2)                               AS avg_growth_rate_pct
FROM banking_kpi
GROUP BY branch_id, branch_name
ORDER BY total_casa_growth DESC;

-- 2. Loan Disbursement KPIs
SELECT
    branch_name,
    SUM(loan_applications)                                              AS total_applications,
    SUM(loan_approvals)                                                 AS total_approvals,
    ROUND(SUM(loan_approvals) * 100.0 / SUM(loan_applications), 1)     AS approval_rate_pct,
    SUM(loan_disbursed_amt)                                             AS total_disbursed_amt
FROM banking_kpi
GROUP BY branch_id, branch_name
ORDER BY total_disbursed_amt DESC;

-- 3. Customer Acquisition & Product Penetration
SELECT
    branch_name,
    SUM(new_accounts)                                                   AS new_accounts_opened,
    SUM(customer_acquisitions)                                          AS total_acquisitions,
    SUM(cross_sell_count)                                               AS total_cross_sells,
    ROUND(SUM(cross_sell_count) * 100.0
          / SUM(customer_acquisitions), 1)                              AS cross_sell_rate_pct
FROM banking_kpi
GROUP BY branch_id, branch_name
ORDER BY total_acquisitions DESC;

-- 4. Monthly Performance Trend (All Branches)
SELECT
    month,
    SUM(casa_closing_bal - casa_opening_bal)                            AS total_casa_growth,
    SUM(loan_disbursed_amt)                                             AS total_loans_disbursed,
    SUM(customer_acquisitions)                                          AS new_customers,
    SUM(revenue)                                                        AS total_revenue
FROM banking_kpi
GROUP BY month
ORDER BY month;

-- 5. Branch Performance Scorecard
SELECT
    branch_name,
    SUM(casa_closing_bal - casa_opening_bal)                            AS casa_growth,
    SUM(loan_disbursed_amt)                                             AS loans_disbursed,
    SUM(customer_acquisitions)                                          AS customers_acquired,
    SUM(cross_sell_count)                                               AS cross_sells,
    SUM(revenue)                                                        AS total_revenue
FROM banking_kpi
GROUP BY branch_id, branch_name
ORDER BY total_revenue DESC;

-- 6. Revenue Growth Month-on-Month
SELECT
    branch_name,
    month,
    revenue,
    LAG(revenue) OVER (PARTITION BY branch_id ORDER BY month)           AS prev_month_revenue,
    ROUND((revenue - LAG(revenue) OVER (PARTITION BY branch_id ORDER BY month))
          * 100.0
          / LAG(revenue) OVER (PARTITION BY branch_id ORDER BY month), 1) AS mom_growth_pct
FROM banking_kpi
ORDER BY branch_name, month;
