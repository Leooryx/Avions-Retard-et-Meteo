#pip install boto3
#curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#unzip awscliv2.zip
#sudo ./aws/install

#aws configure
#keys, region and default output format (txt)


import boto3

import pandas as pd



bucket_name = "avion-et-meteo"
access_key = "cachée"
secret_key = "cachée"

# Create a session and S3 client
session = boto3.session.Session()
s3_client = session.client(
    service_name='s3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)


# List objects in the specific bucket
print(f"Listing objects in bucket '{bucket_name}':")
response = s3_client.list_objects_v2(Bucket=bucket_name)
if 'Contents' in response:
    for obj in response['Contents']:
        print(f"  {obj['Key']}")
else:
    print("  Bucket is empty.")




import pandas as pd

# Replace with the path to your CSV file
file_name = 'T_ONTIME_REPORTING_april.csv'
local_file_path = 'T_ONTIME_REPORTING_april.csv'

try:
    # Download the file from S3
    s3_client.download_file(bucket_name, file_name, local_file_path)
    print(f"File '{file_name}' downloaded successfully.")

    # Read the CSV file into a DataFrame
    data = pd.read_csv(local_file_path)
    print(data.head())  # Print the head of the DataFrame
except Exception as e:
    print(f"An error occurred: {e}")

