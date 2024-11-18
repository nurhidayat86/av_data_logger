import os
import pandas as pd
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from datetime import datetime
from google.cloud import storage

# Load environment variables
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
SYMBOL = "ETH"
MARKET = "USD"
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
GCS_FOLDER = os.getenv("GCS_FOLDER", "ethereum_data/")

def upload_to_gcs(bucket_name, destination_blob_name, file_path):
    """
    Uploads a file to Google Cloud Storage and deletes the file locally.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file to GCS
    blob.upload_from_filename(file_path)
    print(f"File {file_path} uploaded to {destination_blob_name}.")

    # Delete the local file
    try:
        os.remove(file_path)
        print(f"Temporary file {file_path} deleted.")
    except Exception as e:
        print(f"Failed to delete temporary file {file_path}: {e}")

def fetch_and_store_ethereum_data():
    """
    Fetches Ethereum data with a 1-minute interval using the Alpha Vantage Python library,
    and stores it in Google Cloud Storage as a Parquet file.
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
        local_file_path = f"/tmp/{file_name}"
        gcs_blob_path = f"{GCS_FOLDER}{file_name}"

        # Save DataFrame as a Parquet file locally
        df.to_parquet(local_file_path, engine="pyarrow", index=True)
        print(f"Data successfully saved locally to {local_file_path}")

        # Upload to Google Cloud Storage and delete temp file
        upload_to_gcs(GCS_BUCKET_NAME, gcs_blob_path, local_file_path)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_and_store_ethereum_data()
