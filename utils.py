"""
utils.py
Utility functions
"""
import yfinance as yf
import pandas as pd
import numpy as np
import requests
import io


def download_stocks(tickers: list[str], start = str, end = str):
    """
    Extension of download_stock but for multiple
    tickers
    """
    pnls = []
    for t in tickers:
        df = download_stock(t, start, end)
        pnls.append(df)
    
    df = pnls[0]
    for d in pnls[1:]:
        df = df.merge(d, on='Date')
    
    return df 

def download_stock(ticker : str, start = str, end = str):
    """
    Downloads a stocks PnL from start to end, attempting 
    various sources
    """

    try: #try yfinance
        df = yf.download(ticker, start=start, end=end)["Close"]
        if not df.empty():
            return df
    except:
        pass
    
    #try stooq
    stooq_ticker = ticker + ".us"
    stooq_url = "https://stooq.com/q/d/l/" "?s=hes.us&f=20050225&t=20250317&i=d"
    #TODO : Make the correct url call, load into pandas from csv
