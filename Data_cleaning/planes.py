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


# PARTIE 1 : Récupération des données

bucket_name = "avion-et-meteo"
access_key = "NA"
secret_key = "NA"

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



# Download the file from S3 (take some time)
for obj in response["Contents"]:
    s3_client.download_file(bucket_name, obj['Key'], obj['Key'])


#Hypothèse de travail : les avions sont similairement sensibles aux mêmes variations de météo sur leur retard --> on peut généraliser la situation d'un aéroports aux autres
#On décide de se concentrer sur l'aéroport JFK dont le code est : 10135

january_JFK = pd.read_csv('T_ONTIME_REPORTING_january.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(january_JFK)) #191
february_JFK = pd.read_csv('T_ONTIME_REPORTING_february.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(february_JFK)) #128
march_JFK = pd.read_csv('T_ONTIME_REPORTING_march.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(march_JFK)) #167
april_JFK = pd.read_csv('T_ONTIME_REPORTING_april.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(april_JFK)) #139
may_JFK = pd.read_csv('T_ONTIME_REPORTING_may.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(may_JFK)) #160
june_JFK = pd.read_csv('T_ONTIME_REPORTING_june.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(june_JFK)) #134
july_JFK = pd.read_csv('T_ONTIME_REPORTING_july.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(july_JFK)) #192
september_JFK = pd.read_csv('T_ONTIME_REPORTING_september.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(september_JFK)) #206
october_JFK = pd.read_csv('T_ONTIME_REPORTING_october.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(october_JFK)) #253
november_JFK = pd.read_csv('T_ONTIME_REPORTING_november.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(november_JFK)) #220
december_JFK = pd.read_csv('T_ONTIME_REPORTING_december.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(december_JFK)) #168
#Total = 1958
year = [january_JFK, february_JFK, march_JFK, april_JFK, may_JFK, june_JFK, july_JFK, september_JFK, october_JFK, november_JFK, december_JFK]

JFK_2017 = pd.concat(year, ignore_index=True)
#print(len(JFK_2017))
JFK_2017['FL_DATE'] = pd.to_datetime(JFK_2017['FL_DATE'])
#Hypothèse : on remplace les valeurs manquantes de WEATHER_DELAY dans JFK_2017 par 0 car on suppose qu'un retard cause beaucoup de colère et donc sera noté plus fréquemment qu'une absence de retard
JFK_2017['WEATHER_DELAY'] = JFK_2017['WEATHER_DELAY'].fillna(0)

weather = pd.read_csv('jfk_weather.csv')
#print(weather.info()) #beaucoup de type ne sont pas bien définis
#90 colonnes
weather['DATE'] = pd.to_datetime(weather['DATE'])

weather_2017 = weather[weather['DATE'].dt.year == 2017]
#print(weather_2017.head())
#print(weather_2017.tail())




#PARTIE 2 : Analyse exploratoire

print("\nRésumé statistique des vols :")
print(JFK_2017.describe())

# Retards moyens par mois
JFK_2017['Month'] = JFK_2017['FL_DATE'].dt.month
monthly_delays = JFK_2017.groupby('Month')[['DEP_DELAY_NEW', 'ARR_DELAY_NEW']].mean()

# Visualisation des retards moyens par mois
file_name = 'Retard_moyen.png'
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
plt.savefig('/home/onyxia/work/Effects-Language-Diversity-1/Data_cleaning/pictures/Retard_moyen.png')


'''#Chargement le fichier vers S3 et enregistrement le graphique dans un buffer en mémoire
buffer = io.BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)  # Remettre le pointeur du buffer au début

try:
    s3_client.upload_fileobj(buffer, bucket_name, file_name)
    print(f"Le graphique a été chargé avec succès dans le bucket S3 '{bucket_name}' sous le nom '{file_name}'.")
except Exception as e:
    print(f"Une erreur s'est produite lors du chargement : {e}")

# Fermer le buffer
buffer.close()'''

# Distribution des retards au départ
plt.figure(figsize=(10, 6))
sns.histplot(JFK_2017['DEP_DELAY_NEW'], bins=50, kde=True, color='blue', edgecolor='black')
plt.title("Distribution des retards au départ", fontsize=16)
plt.xlabel("Retard au départ (minutes)", fontsize=12)
plt.ylabel("Nombre de vols", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
plt.savefig('/home/onyxia/work/Effects-Language-Diversity-1/Data_cleaning/pictures/Distrib_retard_départ.png')

# Distribution des retards dus aux conditions météorologiques
plt.figure(figsize=(10, 6))
sns.histplot(JFK_2017['WEATHER_DELAY'], bins=50, kde=True, color='orange', edgecolor='black')
plt.title("Distribution des retards dus aux conditions météorologiques", fontsize=16)
plt.xlabel("Retard dû à la météo (minutes)", fontsize=12)
plt.ylabel("Nombre de vols", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
plt.savefig('/home/onyxia/work/Effects-Language-Diversity-1/Data_cleaning/pictures/Distrib_retard_météo.png')

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
plt.savefig('/home/onyxia/work/Effects-Language-Diversity-1/Data_cleaning/pictures/Retard_météo_moyen.png')

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
plt.savefig('/home/onyxia/work/Effects-Language-Diversity-1/Data_cleaning/pictures/Vols_annulés.png')

#Conclusion de l'analyse explratoire