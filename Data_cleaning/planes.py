#pip install boto3
#curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#unzip awscliv2.zip
#sudo ./aws/install

#aws configure
#keys, region and default output format (txt)


import boto3

import pandas as pd

# Initialiser le client S3
s3 = boto3.client('s3')

# Paramètres du bucket et fichier
bucket_name = 'avion-et-meteo'
file_name = 'T_ONTIME_REPORTING_january.csv'

# Télécharger le fichier et le lire dans Pandas
s3.download_file(bucket_name, file_name, 'local_file.csv')
df = pd.read_csv('local_file.csv')
print(df.head())

'''#pip install smart_open
from smart_open import open
file_path = f's3://{bucket_name}/{file_name}'
df = pd.read_csv(open(file_path, 'rb'))
print(df.head())'''

