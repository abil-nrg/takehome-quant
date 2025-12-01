"""
utils.py
Utility functions
"""
import yfinance as yf
import pandas as pd
import requests
import io


def download_stock(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Downlaod the stocks daily closing price from 
    start to end. Attempts with yfiance, then stooq.  
    """

    try:
        df = yf.download(ticker, start=start, end=end)["Close"]
        if not df.empty:
            #df = df.rename(columns={"Close": ticker})
            df.index = df.index.rename("Date")
            return df
    except Exception:
        pass

    #if not stooq
    try:
        stooq_ticker = ticker.lower() + ".us"
        url = f"https://stooq.com/q/d/l/?s={stooq_ticker}&i=d"
        response = requests.get(url)
        
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.set_index("Date")[[ "Close" ]]
            df = df.rename(columns={"Close": ticker})
            df = df.loc[start:end]
            return df
    except Exception:
        pass

    raise ValueError(f"Unable to download data for ticker: {ticker}")


def download_stocks(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """
    Download multiple tickers
    """
    dfs = [download_stock(t, start, end) for t in tickers]
    df_merged = pd.concat(dfs, axis=1).dropna()
    return df_merged
