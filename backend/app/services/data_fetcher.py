import yfinance as yf
import pandas as pd
from datetime import datetime


# ~100 Indian listed companies

STOCKS = [

    # Nifty 50

    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "HINDUNILVR.NS",
    "ITC.NS",
    "LT.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
    "KOTAKBANK.NS",
    "AXISBANK.NS",
    "BAJFINANCE.NS",
    "ASIANPAINT.NS",
    "MARUTI.NS",
    "SUNPHARMA.NS",
    "HCLTECH.NS",
    "TITAN.NS",
    "NESTLEIND.NS",
    "ULTRACEMCO.NS",
    "POWERGRID.NS",
    "NTPC.NS",
    "WIPRO.NS",
    "TECHM.NS",
    "ONGC.NS",
    "JSWSTEEL.NS",
    "TATASTEEL.NS",
    "COALINDIA.NS",
    "INDUSINDBK.NS",
    "BAJAJFINSV.NS",
    "ADANIPORTS.NS",
    "M&M.NS",
    "HDFCLIFE.NS",
    "SBILIFE.NS",
    "DRREDDY.NS",
    "CIPLA.NS",
    "GRASIM.NS",
    "HEROMOTOCO.NS",
    "EICHERMOT.NS",
    "BRITANNIA.NS",
    "APOLLOHOSP.NS",
    "DIVISLAB.NS",
    "TATACONSUM.NS",
    "BAJAJ-AUTO.NS",
    "SHRIRAMFIN.NS",
    "BEL.NS",
    "TRENT.NS",
    "ADANIENT.NS",
    "BPCL.NS",
    "HINDALCO.NS",

    # Additional stocks

    "PIDILITIND.NS",
    "DABUR.NS",
    "GODREJCP.NS",
    "SIEMENS.NS",
    "ABB.NS",
    "BOSCHLTD.NS",
    "MCDOWELL-N.NS",
    "COLPAL.NS",
    "LUPIN.NS",
    "TORNTPHARM.NS",
    "AUROPHARMA.NS",
    "ZYDUSLIFE.NS",
    "BANKBARODA.NS",
    "CANBK.NS",
    "PNB.NS",
    "IDFCFIRSTB.NS",
    "FEDERALBNK.NS",
    "INDIGO.NS",
    "IRCTC.NS",
    "DMART.NS",
    "DLF.NS",
    "LODHA.NS",
    "GAIL.NS",
    "IOC.NS",
    "HAVELLS.NS",
    "POLYCAB.NS",
    "CGPOWER.NS",
    "PAGEIND.NS",
    "MOTHERSON.NS",
    "TVSMOTOR.NS",
    "ASHOKLEY.NS",
    "SAIL.NS",
    "VEDL.NS",
    "AMBUJACEM.NS",
    "ACC.NS",
    "ICICIPRULI.NS",
    "CHOLAFIN.NS",
    "PERSISTENT.NS",
    "NAUKRI.NS",
    "MPHASIS.NS",
    "LTIM.NS",
    "COFORGE.NS",
    "INDUSTOWER.NS",
    "BIOCON.NS",
    "JUBLFOOD.NS",
    "TATAPOWER.NS",
    "UNIONBANK.NS"
]


def fetch_stock_data():

    all_data = []

    start_date = "2020-01-01"

    end_date = datetime.today().strftime("%Y-%m-%d")

    for stock in STOCKS:

        try:

            print(f"Fetching {stock}")

            df = yf.download(

                stock,

                start=start_date,

                end=end_date,

                auto_adjust=True,

                progress=False

            )

            if df.empty:

                print(f"No data found for {stock}")

                continue

            df.reset_index(inplace=True)

            # Remove MultiIndex if present

            if isinstance(df.columns, pd.MultiIndex):

                df.columns = df.columns.get_level_values(0)

            df["symbol"] = stock

            all_data.append(df)

        except Exception as e:

            print(f"Failed: {stock}")

            print(e)

            continue

    combined_df = pd.concat(

        all_data,

        ignore_index=True

    )

    return combined_df