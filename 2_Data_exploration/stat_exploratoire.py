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
import seaborn as sns

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


#weather_2017 = pd.read_csv('Pre-Processed_data/weather_2017.csv')
#plane_weather = pd.read_csv('Pre-Processed_data/plane_weather.csv') #problem of encoding
#TODO problem of encoding when i try to read files directly from S3



plane_weather = pd.read_csv('/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/plane_weather.csv')
plane_weather_for_ML = pd.read_csv('/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/plane_weather_for_ML.csv')
JFK_numbers = pd.read_csv('/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/JFK_numbers.csv')
weather_2017 = pd.read_csv('/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/weather_2017.csv')

print("\nRésumé statistique des vols et de la météo :")
plane_weather.describe().to_csv('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/plane_weather_summary.csv')
#est-ce que je peux en faire une image ?
#TODO : comment rendre la lisibilité meilleure ?


plane_weather['Full_Departure_Datetime'] = pd.to_datetime(plane_weather['Full_Departure_Datetime'])
plane_weather['DATE_weather'] = pd.to_datetime(plane_weather['DATE_weather'])
print(plane_weather.info())


# Retards moyens par mois
plane_weather['Month'] = plane_weather['Full_Departure_Datetime'].dt.month
monthly_delays = plane_weather.groupby('Month')[['DEP_DELAY', 'ARR_DELAY']].mean()

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
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/Retards_moyens.png')
#Chargement le fichier vers S3 et enregistrement le graphique dans un buffer en mémoire
upload_to_s3("Pictures", "Retards_moyens.png")

# Distribution des retards au départ
plt.figure(figsize=(10, 6))
sns.histplot(plane_weather['DEP_DELAY'], bins=50, kde=True, color='blue', edgecolor='black')
plt.title("Distribution des retards au départ", fontsize=16)
plt.xlabel("Retard au départ (minutes)", fontsize=12)
plt.ylabel("Nombre de vols", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/Distrib_retard_départ.png')
upload_to_s3("Pictures", "Distrib_retard_départ.png")

# Distribution des retards dus aux conditions météorologiques
plt.figure(figsize=(10, 6))
sns.histplot(plane_weather['WEATHER_DELAY'], bins=50, kde=True, color='orange', edgecolor='black')
plt.title("Distribution des retards dus aux conditions météorologiques", fontsize=16)
plt.xlabel("Retard dû à la météo (minutes)", fontsize=12)
plt.ylabel("Nombre de vols", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/Distrib_retard_météo.png')
upload_to_s3("Pictures", "Distrib_retard_météo.png")

# Moyenne des retards dus aux conditions météorologiques par mois
weather_delay_monthly = plane_weather.groupby('Month')['WEATHER_DELAY'].mean()

plt.figure(figsize=(10, 6))
weather_delay_monthly.plot(kind='bar', color='teal', alpha=0.8, edgecolor='black')
plt.title("Retards moyens dus à la météo par mois", fontsize=16)
plt.ylabel("Retard moyen (minutes)", fontsize=12)
plt.xlabel("Mois", fontsize=12)
plt.xticks(range(0, 12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/Retard_météo_moyen.png')
upload_to_s3("Pictures", "Retard_météo_moyen.png")

# Pourcentage de vols annulés
cancelled_percentage = plane_weather['CANCELLED'].mean() * 100
print(f"Pourcentage de vols annulés : {cancelled_percentage:.2f}%")

# Visualisation des vols annulés
cancelled_counts = plane_weather['CANCELLED'].value_counts(normalize=True) * 100
plt.figure(figsize=(8, 6))
cancelled_counts.plot(kind='bar', color=['green', 'red'], alpha=0.8, edgecolor='black')
plt.title("Pourcentage de vols annulés", fontsize=16)
plt.ylabel("Pourcentage", fontsize=12)
plt.xlabel("Annulé (0 = Non, 1 = Oui)", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/Vols_annulés.png')
upload_to_s3("Pictures", "Vols_annulés.png")

#Conclusion de l'analyse exploratoire







'''import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Assuming the plane_weather DataFrame is already loaded
# For demonstration purposes, let's create a mock DataFrame with similar structure
# The actual data should be loaded from the 'plane_weather' CSV as per your setup.

# Loading the plane_weather DataFrame (mock data for now)
# plane_weather = pd.read_csv('path_to_your_data.csv')

# Let's generate the necessary data and mock some data for the example:
plane_weather = pd.DataFrame({
    'Full_Departure_Datetime': pd.date_range(start='1/1/2017', periods=365, freq='D'),
    'DAILYMaximumDryBulbTemp': [25 + (i % 30) for i in range(365)],
    'DAILYMinimumDryBulbTemp': [15 + (i % 25) for i in range(365)],
    'DAILYPrecip': [0 if i % 5 else 1 for i in range(365)],
})

# Ensuring that the Full_Departure_Datetime column is in datetime format
plane_weather['Full_Departure_Datetime'] = pd.to_datetime(plane_weather['Full_Departure_Datetime'])

# Create the plot
plt.figure(figsize=(8.27, 11.69))  # A4 size (in inches)

# 1. Plotting the characterization for the entire year of 2017
plt.subplot(2, 1, 1)

# Let's plot the maximum and minimum daily temperatures over the year
sns.lineplot(data=plane_weather, x='Full_Departure_Datetime', y='DAILYMaximumDryBulbTemp', label='Max Temp', color='orange')
sns.lineplot(data=plane_weather, x='Full_Departure_Datetime', y='DAILYMinimumDryBulbTemp', label='Min Temp', color='blue')

plt.title('Weather Characterization Throughout 2017')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.legend()

# Formatting x-axis for better readability
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))  # Display months
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Tick every month
plt.xticks(rotation=45)

# 2. Plotting for the monthly weather characterization
months = plane_weather['Full_Departure_Datetime'].dt.month
monthly_data = plane_weather.groupby(months).agg({
    'DAILYMaximumDryBulbTemp': 'mean',
    'DAILYMinimumDryBulbTemp': 'mean',
    'DAILYPrecip': 'mean',
}).reset_index()

plt.subplot(2, 1, 2)

# Monthly average temperatures and precipitation
sns.barplot(data=monthly_data, x='Full_Departure_Datetime', y='DAILYMaximumDryBulbTemp', color='orange', label='Max Temp')
sns.barplot(data=monthly_data, x='Full_Departure_Datetime', y='DAILYMinimumDryBulbTemp', color='blue', label='Min Temp')

plt.title('Monthly Weather Summary')
plt.xlabel('Month')
plt.ylabel('Average Temperature (°F)')
plt.legend()

# Customize the plot
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Save the plot as a PNG file
plt.tight_layout()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/weather_summary.png', dpi=300)

# Display the plot to the user
plt.show()'''





import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Let's simulate loading the plane_weather dataset with the provided data structure.
# We'll generate a sample dataframe from the data provided (it's a small sample, for illustration).



df = plane_weather
# Set the figure size and style for aesthetics
plt.figure(figsize=(12, 9))


# Create the main plot for 2017 weather trends (for simplicity, we use random values for now)
#plt.subplot(2, 1, 1)
'''
plt.plot(df['DATE_weather'], df['HOURLYWindSpeed'], label='Hourly Wind Speed', color='red', linewidth=1)
plt.plot(df['DATE_weather'], df['HOURLYPrecip'], label='Hourly Precipitation', color='green', linewidth=1)
plt.plot(df['DATE_weather'], df['DAILYSnowDepth'], label='DAILYSnowDepth', color='blue', linewidth=1)
plt.plot(df['DATE_weather'], df['HOURLYStationPressure'], label='HOURLYStationPressure', color='grey', linewidth=1)
plt.plot(df['DATE_weather'], df['HOURLYVISIBILITY'], label='HOURLYVISIBILITY', color='brown', linewidth=1)
plt.plot(df['DATE_weather'], df['HOURLYDRYBULBTEMPF'], label='HOURLYDRYBULBTEMPF', color='black', linewidth=1)


plt.xlabel('Date')
plt.ylabel('Values')
plt.title('Yearly Weather Trends (2017)')
plt.legend()'''


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# Create the monthly subplots (simplified for illustration with sample data)
for i, month in enumerate(months):
    month_data = df[df['DATE_weather'].dt.month == i + 1]
    plt.subplot(3, 4, i+1)
    plt.plot(month_data['DATE_weather'], month_data['HOURLYWindSpeed'], label='Hourly Wind Speed', color='red', linewidth=1)
    plt.plot(month_data['DATE_weather'], month_data['HOURLYPrecip'], label='Hourly Precipitation', color='green', linewidth=1)
    plt.plot(month_data['DATE_weather'], month_data['DAILYSnowDepth'], label='DAILYSnowDepth', color='blue', linewidth=1)
    plt.plot(month_data['DATE_weather'], month_data['HOURLYStationPressure'], label='HOURLYStationPressure', color='grey', linewidth=1)
    plt.plot(month_data['DATE_weather'], month_data['HOURLYVISIBILITY'], label='HOURLYVISIBILITY', color='brown', linewidth=1)
    plt.plot(month_data['DATE_weather'], month_data['HOURLYDRYBULBTEMPF'], label='HOURLYDRYBULBTEMPF', color='black', linewidth=1)
    
    plt.title(f'{month}')
    #plt.xlabel('Date')
    plt.ylabel('Values')
    #plt.xticks()
    

    plt.tight_layout()

plt.legend()
# Saving the figure to a PNG file
plt.tight_layout()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/weather_summary.png', dpi=300)


