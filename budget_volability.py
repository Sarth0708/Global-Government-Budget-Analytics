from sqlalchemy import create_engine

import pandas as pd
from urllib.parse import quote_plus

username = "root"
password = quote_plus("Sarthak@12")

# password = quote_plus("Sarthak@12")

def analyze_budget_volatility(country_name):
    engine = create_engine(f"mysql+pymysql://{username}:{password}@localhost/global_budget_db")
    
    # Extract historical spending sequence
    query = """
        SELECT b.year, b.total_budget_billions_usd
        FROM budgets b
        JOIN countries c ON b.country_id = c.country_id
        WHERE c.country_name = %s ORDER BY b.year ASC;
    """
    df = pd.read_sql(query, engine, params=(country_name,))
    
    if df.empty:
        return
    
    # Calculate a 10-year rolling mean and standard deviation using Pandas.
    rolling_window = 10
    df['rolling_mean'] = df['total_budget_billions_usd'].rolling(window=rolling_window).mean()
    df['rolling_std'] = df['total_budget_billions_usd'].rolling(window=rolling_window).std()
    
    # Calculate the volatility index (coefficient of variation)
    df['volatility_index'] = (df['rolling_std'] / df['rolling_mean']) * 100
    
    print(f"\n--- ERA Volatility Index for {country_name} (Sample) ---")
    print(df.dropna().head(10))
    return df
if __name__ == "__main__":
    analyze_budget_volatility("USA") #or your country name