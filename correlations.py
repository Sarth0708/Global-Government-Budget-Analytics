from sqlalchemy import create_engine
import pandas as pd
from urllib.parse import quote_plus

username = "root"
password = quote_plus("Sarthak@12")


def compute_sector_correlations(country_name):
    engine = create_engine(f"mysql+pymysql://{username}:{password}@localhost/global_budget_db")

    query = """
        SELECT b.year, sa.sector_name, sa.allocated_percentage
        FROM sector_allocations sa
        JOIN budgets b ON sa.budget_id = b.budget_id
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = %s
        ORDER BY b.year, sa.sector_name;
    """

    df = pd.read_sql(query, engine, params=(country_name,))

    if df.empty:
        print(f"No sector allocation data found for country: {country_name}")
        return None

    df = df.groupby(["year", "sector_name"], as_index=False)["allocated_percentage"].mean()
    wide_df = df.pivot(index="year", columns="sector_name", values="allocated_percentage")
    correlation_matrix = wide_df.corr()

    print(f"\n--- Cross-Sector Correlation Matrix for {country_name} ---")
    print(correlation_matrix.round(2))
    return correlation_matrix


if __name__ == "__main__":
    compute_sector_correlations("India")