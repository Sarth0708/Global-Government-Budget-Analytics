import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

username = "root"
password = quote_plus("Sarthak@12")

def detect_budget_anomalies(country_name):
    engine = create_engine(
        f"mysql+pymysql://{username}:{password}@localhost/global_budget_db"
    )

    query = """
        SELECT b.year, b.total_budget_billions_usd
        FROM budgets b
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = %s
        ORDER BY b.year ASC
    """
    df = pd.read_sql_query(query, engine, params=(country_name,))
    engine.dispose()

    if df.empty:
        print(f"No budget data found for country: {country_name}")
        return pd.DataFrame()

    mean_val = df['total_budget_billions_usd'].mean()
    std_val = df['total_budget_billions_usd'].std()

    if pd.isna(std_val) or std_val == 0:
        print(f"No variability detected for {country_name}; no outlier analysis possible.")
        return df.assign(z_score=0)

    df['z_score'] = (df['total_budget_billions_usd'] - mean_val) / std_val
    anomalies = df[df['z_score'].abs() > 1.96]

    print(f"\n--- Flagged Fiscal Anomalies for {country_name} (Outlier Variance Analysis) ---")
    if anomalies.empty:
        print("No extreme statistical outliers identified.")
    else:
        print(anomalies)
    return anomalies


if __name__ == "__main__":
    detect_budget_anomalies("India")