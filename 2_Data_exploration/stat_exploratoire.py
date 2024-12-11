#pip install boto3
#curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#unzip awscliv2.zip
#sudo ./aws/install

#aws configure
#keys, region and default output format (txt)

import boto3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os

# PARTIE 1 : Récupération des données

bucket_name = "avion-et-meteo"
access_key = "NA"
secret_key = "NA"

#s3://avion-et-meteo/Data-preprocessing/

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
        print(f"{obj['Key']}")
else:
    print("Bucket is empty.")



#Création d'un répertoire local pour chaque dossier contenu dans S3
if 'Contents' in response:
    for obj in response['Contents']:
        key = obj['Key']
        print(f"Processing: {key}")
        
        # Créez les répertoires nécessaires localement
        if '/' in key:  # Si le chemin contient un "/", cela indique un dossier ou un chemin structuré
            local_path = os.path.dirname(key)  # Récupérer le chemin du répertoire
            if not os.path.exists(local_path):
                os.makedirs(local_path)  # Crée les dossiers si nécessaire
        
        # Télécharge uniquement si ce n'est pas un "dossier" (c'est-à-dire si Key ne se termine pas par "/")
        if not key.endswith('/'):
            s3_client.download_file(bucket_name, key, key)
else:
    print("Bucket is empty.")

def upload_to_s3(folder, file_name):
    """
    Sauvegarde un document un dossier spécifique d'un bucket S3.

    Args:
        folder (str): Le nom du dossier dans lequel enregistrer le document.
        file_name (str): Le nom du fichier à enregistrer.
    """

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)  # Remettre le pointeur du buffer au début

    try:
        s3_client.upload_fileobj(buffer, bucket_name, f"{folder}/{file_name}")
        print(f"Le graphique a été chargé avec succès dans le bucket S3 '{bucket_name}' sous le nom '{file_name}'.")
    except Exception as e:
        print(f"Une erreur s'est produite lors du chargement : {e}")

    buffer.close()



#PARTIE 2 : Analyse exploratoire



print("\nRésumé statistique des vols :")
print(JFK_2017.describe())
print("\nRésumé statistique de la météo :")
print(weather_2017.describe())

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
