# av_data_logger
Code to get crypto pricing data from `Alpha-Vantage` and store it to `Google Cloud Storage (GXS)` using `Google Cloud Robn Jobs` and `Google CLoud Scheduler`.

# How to Use
1. Enable all required service permissions on your GCP account (`GCS`, `Cloud Run`, `Scheduler`),
2. create these following folders under your GCS bucket:
`['BTC', 'ETH', 'USDT', 'SOL', 'BNB', 'DOGE', 'XRP', 'USDC', 'ADA']`. These crypto tickers also you can modify on the `fetch_ethereum_data.py` in case youw ant to add the tickers.
3. Login to `gcloud CLI` by executing in terminal: `gcloud auth login`.
4. Build the docker image and register it in Google: `gcloud builds submit --tag=gcr.io/[your project name]/fetch-ethereum-data`.
5. Create Google Cloud Run Jobs: `gcloud run jobs create fetch-ethereum-data --image gcr.io/[project name]/fetch-ethereum-data --region [preferred region] --set-env-vars ALPHA_VANTAGE_API_KEY=[alpha-vantage API key] --set-env-vars GCS_BUCKET_NAME=[Bucket name]`.
6. Create a service account to invoke the job: `gcloud run jobs add-iam-policy-binding fetch-ethereum-data --member serviceAccount:process-identity@[project name].iam.gserviceaccount.com --role roles/run.invoker`.
7. Create a scheduler, easier to do it via GUI. Go to your dashboard, enter all details, including frequency in CRON format (`* * * * *`). In section: `Configure the execution`:
   * Put target type: `http`, method: `post`, and url: `https://asia-southeast1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/[project name]/jobs/fetch-ethereum-data:run`.
   * Auth header: `Add OAuth Token`, service account: `process_identity@[project name].iam.gserviceaccount.com`

This is a personal and open repo. Free to use, and provided as it is.
