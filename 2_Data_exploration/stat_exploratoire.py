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






import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

# Crée une figure de taille A4
plt.figure(figsize=(8.27, 11.69))  # A4 size (in inches)
plt.suptitle('Weather Characterization Throughout 2017', fontsize=16, fontweight='bold')

# Fonction pour formater les axes de chaque sous-graphique
def format_subplot(ax, data, x_column, y_column, label, color, ylabel):
    sns.lineplot(data=data, x=x_column, y=y_column, label=label, color=color, ax=ax)
    ax.set_xlabel('Date')
    ax.set_ylabel(ylabel)
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))  # Display months
    ax.xaxis.set_major_locator(mdates.MonthLocator())  # Tick every month
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels

# Plot 1: Daily maximum and minimum temperatures
ax1 = plt.subplot(4, 1, 1)
format_subplot(ax1, plane_weather, 'Full_Departure_Datetime', 'DAILYMaximumDryBulbTemp', 'Max Temp', 'orange', 'Temperature (°F)')
sns.lineplot(data=plane_weather, x='Full_Departure_Datetime', y='DAILYMinimumDryBulbTemp', label='Min Temp', color='blue', ax=ax1)

# Plot 2: Daily Precipitation
ax2 = plt.subplot(4, 1, 2)
format_subplot(ax2, plane_weather, 'Full_Departure_Datetime', 'DAILYPrecip', 'Daily Precip', 'black', 'Precipitation')

# Plot 3: Daily Snow Depth
ax3 = plt.subplot(4, 1, 3)
format_subplot(ax3, plane_weather, 'Full_Departure_Datetime', 'DAILYSnowDepth', 'Daily Snow', 'blue', 'Snow Depth')

# Plot 4: Hourly Station Pressure
ax4 = plt.subplot(4, 1, 4)
format_subplot(ax4, plane_weather, 'Full_Departure_Datetime', 'HOURLYStationPressure', 'Pressure', 'gray', 'Pressure (in Hg)')

# Ajuster les espaces et enregistrer le graphique
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to avoid title overlap
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/weather_2017_summary.png', dpi=300)
plt.show()






'''# 2. Plotting for the monthly weather characterization
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
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])'''

# Save the plot as a PNG file
plt.tight_layout()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/weather_2017_summary.png', dpi=300)







import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# Set the figure size and style for aesthetics
plt.figure(figsize=(12, 9))

# Function to format subplots
def format_subplot(ax, data, x_column, y_columns, labels, colors, ylabel):
    for y_col, label, color in zip(y_columns, labels, colors):
        sns.lineplot(data=data, x=x_column, y=y_col, label=label, color=color, ax=ax, linewidth=1)
    ax.set_ylabel(ylabel)
    ax.legend(False)
    ax.set_xticklabels([])  # Hide x-axis labels

# List of months and corresponding colors
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
colors = ['green', 'blue', 'grey', 'black']
labels = ['Hourly Precipitation * 10', 'Daily Snow Depth', 'Hourly Station Pressure', 'Average Dry Bulb Temp']

# Loop over each month to create the subplots
for i, month in enumerate(months):
    month_data = plane_weather[plane_weather['DATE_weather'].dt.month == i + 1]
    ax = plt.subplot(3, 4, i+1)
    format_subplot(ax, month_data, 'DATE_weather', ['DAILYPrecip', 'DAILYSnowDepth', 'HOURLYStationPressure', 'DAILYAverageDryBulbTemp'], labels, colors, 'Values')
    ax.set_title(f'{month}')

# Add main title for the entire figure
plt.suptitle('Weather Month by Month', fontsize=16, fontweight='bold')

# Adjust the layout to avoid overlap and place the legend horizontally at the bottom
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout for title

# Adjust the position of the legend (at the bottom horizontally)
plt.legend(loc='center', bbox_to_anchor=(-0.5, -0.1), ncol=4)

plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/month_by_month.png', dpi=300)




