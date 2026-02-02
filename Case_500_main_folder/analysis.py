import pandas as pd

def load_data():
    """
    Loads, cleans, and aligns S&P 500 and Case-Shiller datasets.
    Resamples daily equity data to monthly to match housing index frequency.
    """

    sp500 = pd.read_csv("csv_data/sap500.csv")
    cs = pd.read_csv("csv_data/case_shiller.csv")

    sp500["Date"] = pd.to_datetime(sp500["Date"])
    cs["Date"] = pd.to_datetime(cs["observation_date"])

    #Using monthly averages to align daily S&P 500 data with monthly Case-Shiller data
    sap_df = (sp500.set_index("Date")["Close"].resample("MS").mean().rename("SP500")) #s&p500 monthly
    case_shiller_df = (cs.set_index("Date")["CaseShiller"].resample("MS").mean()) #caseshiller monthly

    #Merge data using pd.merge
    df = pd.merge(
        sap_df,
        case_shiller_df,
        left_index=True,
        right_index=True,
        how="inner"
    )

    return df

"""Returns raw price/index levels for historical trend visualization."""
def trend_report(df):
    return df[["SP500", "CaseShiller"]]

"""
Scales data to a base of 100 at the start of the time series.
Essential for comparing assets with vastly different price points (e.g., 4000 vs 250).
"""
def normalize_report(df):
    return df / df.iloc[0] * 100

"""
Calculates the 12-month rolling Pearson correlation.
Used to observe how the relationship strength changes during economic cycles.
"""
def rolling_correlation_report(df, window = 12):
    return df["SP500"].rolling(window).corr(df["CaseShiller"])
