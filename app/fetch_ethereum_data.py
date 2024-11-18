import os
import pandas as pd
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from datetime import datetime

# Load environment variables
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
SYMBOL = "ETH"
MARKET = "USD"
FILESTORE_DIR = os.getenv("FILESTORE_DIR", "/mnt/filestore/")

def fetch_and_store_ethereum_data():
    """
    Fetches Ethereum data with a 1-minute interval using the Alpha Vantage Python library,
    and stores it in Google Filestore as a Parquet file.
    """
    try:
        # Initialize Alpha Vantage client
        crypto = CryptoCurrencies(key=ALPHA_VANTAGE_API_KEY, output_format="pandas")
        
        # Fetch Ethereum data
        df, _ = crypto.get_digital_currency_intraday(symbol=SYMBOL, market=MARKET)
        
        # Rename columns for clarity
        df = df.rename(
            columns={
                "1. open": "open",
                "2. high": "high",
                "3. low": "low",
                "4. close": "close",
                "5. volume": "volume",
            }
        )
        df.index = pd.to_datetime(df.index)  # Ensure index is in datetime format
        df = df.sort_index()  # Sort data by timestamp
        
        # Generate filename based on the timestamp of the last data point
        last_timestamp = df.index[-1].strftime("%Y%m%d%H%M%S")
        file_name = f"eth_{last_timestamp}.parquet"
        file_path = os.path.join(FILESTORE_DIR, file_name)

        # Save DataFrame as a Parquet file
        df.to_parquet(file_path, engine="pyarrow", index=True)
        print(f"Data successfully saved to {file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_and_store_ethereum_data()
