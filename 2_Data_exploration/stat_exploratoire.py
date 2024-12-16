#Data-exploration

#Requirements


#pas nécessairement utile de télécharger AMZ CLI
#curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#unzip awscliv2.zip
#sudo ./aws/install

#aws configure
#keys, region and default output format (txt)

#pip install boto3
import boto3
import pandas as pd
import matplotlib.pyplot as plt
import io
import os
import numpy as np
from datetime import timedelta


#Opening and reading the .env file
with open('/home/onyxia/work/Avions-Retard-et-Meteo/.env') as f:
    for line in f:
        line = line.strip()
        # Ignorer les lignes vides ou les commentaires
        if not line or line.startswith('#'):
            continue
        # Séparer la clé de la valeur (en supposant un format key=value)
        key, value = line.split('=', 1)
        os.environ[key] = value

#We can now use the keys
s3_access_key_id = os.environ["S3_ACCESS_KEY_ID"]
s3_secret_access_key = os.environ["S3_SECRET_ACCESS_KEY"]

bucket_name = "avion-et-meteo"

# Create a session and S3 client
session = boto3.session.Session()
s3_client = session.client(service_name='s3',
    aws_access_key_id=s3_access_key_id,
    aws_secret_access_key=s3_secret_access_key,
)

# List objects in the specific bucket
print(f"Listing objects in bucket '{bucket_name}':")
response = s3_client.list_objects_v2(Bucket=bucket_name)
if 'Contents' in response:
    for obj in response['Contents']:
        print(f"{obj['Key']}")
else:
    print("Bucket is empty.")



#Download the files from S3
if 'Contents' in response:
    for obj in response['Contents']:
        key = obj['Key']
        if 'Pre-Processed_data/' in key:
            print(f"Processing: {key}")
    
            #Create folders
            if '/' in key:  
                local_path = os.path.dirname(key)  
                if not os.path.exists(local_path):
                    os.makedirs(local_path)  
            
            # Download only files
            if not key.endswith('/'):
                s3_client.download_file(bucket_name, key, key)
else:
    print("Bucket is empty.")


#Defining functions to be used later

def upload_to_s3(folder, file_name):
    """
    Upload a document to S3 bucket

    Args:
        folder (str): folder name
        file_name (str): file name
    """

    #For pictures from matplotlib, works also if not a picture
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)  # Remettre le pointeur du buffer au début

    try:
        s3_client.upload_fileobj(buffer, bucket_name, f"{folder}/{file_name}")
        print(f"Le document a été chargé avec succès dans le bucket S3 '{bucket_name}' sous le nom '{file_name}'.")
    except Exception as e:
        print(f"Une erreur s'est produite lors du chargement : {e}")

    buffer.close()


#PARTIE 2 : Analyse exploratoire


weather = pd.read_csv('Data-preprocessing/jfk_weather.csv')
print(weather)
#plane_weather = pd.read_csv('Pre-Processed_data/plane_weather.csv')
#plane_weather = pd.read_csv('/home/onyxia/work/Pre-Processed_data/plane_weather.csv')
plane_weather_ML = pd.read_csv('/home/onyxia/work/Pre-Processed_data/plane_weather_for_ML.csv')



print("\nRésumé statistique des vols et de la météo :")
print(plane_weather.describe())


# Retards moyens par mois
JFK_2017['Month'] = JFK_2017['FL_DATE'].dt.month
monthly_delays = JFK_2017.groupby('Month')[['DEP_DELAY_NEW', 'ARR_DELAY_NEW']].mean()

# Visualisation des retards moyens par mois
file_name = 'Retards_moyens.png'
plt.figure(figsize=(10, 6))
monthly_delays.plot(kind='bar', figsize=(12, 6))
plt.title("Retards moyens par mois", fontsize=16)
plt.ylabel("Retard moyen (minutes)", fontsize=12)
plt.xlabel("Mois", fontsize=12)
plt.xticks(range(0, 12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
plt.legend(["Retard au départ", "Retard à l'arrivée"])
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()

#Chargement "local" pour visualisation rapide
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/Data_cleaning/pictures/Retards_moyens.png')
#Chargement le fichier vers S3 et enregistrement le graphique dans un buffer en mémoire
upload_to_s3("Pictures", "Retards_moyens.png")

# Distribution des retards au départ
plt.figure(figsize=(10, 6))
sns.histplot(JFK_2017['DEP_DELAY_NEW'], bins=50, kde=True, color='blue', edgecolor='black')
plt.title("Distribution des retards au départ", fontsize=16)
plt.xlabel("Retard au départ (minutes)", fontsize=12)
plt.ylabel("Nombre de vols", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/Data_cleaning/pictures/Distrib_retard_départ.png')
upload_to_s3("Pictures", "Distrib_retard_départ.png")

# Distribution des retards dus aux conditions météorologiques
plt.figure(figsize=(10, 6))
sns.histplot(JFK_2017['WEATHER_DELAY'], bins=50, kde=True, color='orange', edgecolor='black')
plt.title("Distribution des retards dus aux conditions météorologiques", fontsize=16)
plt.xlabel("Retard dû à la météo (minutes)", fontsize=12)
plt.ylabel("Nombre de vols", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/Data_cleaning/pictures/Distrib_retard_météo.png')
upload_to_s3("Pictures", "Distrib_retard_météo.png")

# Moyenne des retards dus aux conditions météorologiques par mois
weather_delay_monthly = JFK_2017.groupby('Month')['WEATHER_DELAY'].mean()

plt.figure(figsize=(10, 6))
weather_delay_monthly.plot(kind='bar', color='teal', alpha=0.8, edgecolor='black')
plt.title("Retards moyens dus à la météo par mois", fontsize=16)
plt.ylabel("Retard moyen (minutes)", fontsize=12)
plt.xlabel("Mois", fontsize=12)
plt.xticks(range(0, 12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/Data_cleaning/pictures/Retard_météo_moyen.png')
upload_to_s3("Pictures", "Retard_météo_moyen.png")

# Pourcentage de vols annulés
cancelled_percentage = JFK_2017['CANCELLED'].mean() * 100
print(f"Pourcentage de vols annulés : {cancelled_percentage:.2f}%")

# Visualisation des vols annulés
cancelled_counts = JFK_2017['CANCELLED'].value_counts(normalize=True) * 100
plt.figure(figsize=(8, 6))
cancelled_counts.plot(kind='bar', color=['green', 'red'], alpha=0.8, edgecolor='black')
plt.title("Pourcentage de vols annulés", fontsize=16)
plt.ylabel("Pourcentage", fontsize=12)
plt.xlabel("Annulé (0 = Non, 1 = Oui)", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/Data_cleaning/pictures/Vols_annulés.png')
upload_to_s3("Pictures", "Vols_annulés.png")

#Conclusion de l'analyse exploratoire
