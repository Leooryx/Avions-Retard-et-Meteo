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
import matplotlib.dates as mdates

'''#Opening and reading the .env file
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

    buffer.close()'''


#PARTIE 2 : Analyse exploratoire


#STEP 1: Exploring the plane and weather datasets


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
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/1_Retards_moyens.png')
#Chargement le fichier vers S3 et enregistrement le graphique dans un buffer en mémoire
#upload_to_s3("Pictures", "1_Retards_moyens.png")

# Distribution des retards au départ
plt.figure(figsize=(10, 6))
sns.histplot(plane_weather['DEP_DELAY'], bins=50, kde=True, color='blue', edgecolor='black')
plt.title("Distribution des retards au départ", fontsize=16)
plt.xlabel("Retard au départ (minutes)", fontsize=12)
plt.ylabel("Nombre de vols", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/2_Distrib_retard_départ.png')
#upload_to_s3("Pictures", "2_Distrib_retard_départ.png")

# Distribution des retards dus aux conditions météorologiques
plt.figure(figsize=(10, 6))
sns.histplot(plane_weather['WEATHER_DELAY'], bins=50, kde=True, color='orange', edgecolor='black')
plt.title("Distribution des retards dus aux conditions météorologiques", fontsize=16)
plt.xlabel("Retard dû à la météo (minutes)", fontsize=12)
plt.ylabel("Nombre de vols", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/3_Distrib_retard_météo.png')
#upload_to_s3("Pictures", "3_Distrib_retard_météo.png")

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
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/4_Retard_météo_moyen.png')
#upload_to_s3("Pictures", "4_Retard_météo_moyen.png")


#Proportions of delays
# Calculate the ratio of delays explained by CARRIER_DELAY, WEATHER_DELAY, and unexplained delays
plane_weather['carrier_delay_ratio'] = plane_weather['CARRIER_DELAY'] / plane_weather['DEP_DELAY']
plane_weather['weather_delay_ratio'] = plane_weather['WEATHER_DELAY'] / plane_weather['DEP_DELAY']
plane_weather['unexplained_delay_ratio'] = 1 - (plane_weather['carrier_delay_ratio'] + plane_weather['weather_delay_ratio'])

# Calculate the mean proportion of each type of delay
mean_carrier_delay = plane_weather['carrier_delay_ratio'].mean()
mean_weather_delay = plane_weather['weather_delay_ratio'].mean()
mean_unexplained_delay = plane_weather['unexplained_delay_ratio'].mean()

sizes = [mean_carrier_delay, mean_weather_delay, mean_unexplained_delay]
labels = ['Carrier Delay', 'Weather Delay', 'Unexplained Delay']
colors = ['orange', 'blue', 'gray']

plt.figure(figsize=(11, 7))
wedges, texts = plt.pie(sizes, colors=colors, startangle=90, wedgeprops={'edgecolor': 'black'}, labels=None)
percentages = [f'{size / sum(sizes) * 100:.1f}%' for size in sizes]
legend_labels = [f'{label} ({percentage})' for label, percentage in zip(labels, percentages)]
plt.title('Average Proportion of Delay Explanations')
plt.legend(wedges, legend_labels, title="Delay Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
plt.title('Average Proportion of Delay Explanations')

plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/5_Proportions_of_delays.png')
#upload_to_s3("Pictures", "5_Proportions_of_delay.png")

#deleting the new columns
plane_weather = plane_weather.drop(columns=['carrier_delay_ratio', 'weather_delay_ratio', 'unexplained_delay_ratio'])


#Weather trends for the year 2017
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

ax1 = plt.subplot(4, 1, 1)
format_subplot(ax1, plane_weather, 'Full_Departure_Datetime', 'DAILYMaximumDryBulbTemp', 'Max Temp', 'orange', 'Temperature (°F)')
sns.lineplot(data=plane_weather, x='Full_Departure_Datetime', y='DAILYMinimumDryBulbTemp', label='Min Temp', color='blue', ax=ax1)
ax2 = plt.subplot(4, 1, 2)
format_subplot(ax2, plane_weather, 'Full_Departure_Datetime', 'DAILYPrecip', 'Daily Precip', 'black', 'Precipitation')
ax3 = plt.subplot(4, 1, 3)
format_subplot(ax3, plane_weather, 'Full_Departure_Datetime', 'DAILYSnowDepth', 'Daily Snow', 'blue', 'Snow Depth')
ax4 = plt.subplot(4, 1, 4)
format_subplot(ax4, plane_weather, 'Full_Departure_Datetime', 'HOURLYStationPressure', 'Pressure', 'gray', 'Pressure (in Hg)')
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to avoid title overlap
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/6_weather_2017_summary.png', dpi=300)
plt.show()




#Plot month by month weather
# Set the figure size and style for aesthetics
plt.figure(figsize=(12, 9))

# Function to format subplots
def format_subplot(ax, data, x_column, y_columns, labels, colors, ylabel):
    for y_col, label, color in zip(y_columns, labels, colors):
        sns.lineplot(data=data, x=x_column, y=y_col, label=label, color=color, ax=ax, linewidth=1)
    ax.set_ylabel(ylabel).set_visible(False)
    ax.legend().set_visible(False)
    ax.set_xlabel('')  # Delete x-axis label
    ax.xaxis.set_ticks([])  # Hide x-axis ticks

plane_weather['DAILYPrecip'] = plane_weather['DAILYPrecip']*10 #to show it more visibly on the graph
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


# Adjust the position of the legend (at the bottom horizontally)
plt.legend(loc='center', bbox_to_anchor=(-1.2, -0.09), ncol=4)  # Légende centrée en bas
plt.tight_layout(rect=[0, 0, 1, 0.95]) # Adjust layout for title

plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/7_month_by_month.png', dpi=300)

plane_weather['DAILYPrecip'] = plane_weather['DAILYPrecip']/10 #to remove the modification


#STEP 2: finding relations between the variables
corr_matrix = plane_weather_for_ML.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='RdYlGn', center=0, cbar_kws={'label': 'Correlation Coefficient'}, linewidths=0.5, linecolor='black')
ticks = np.arange(len(plane_weather_for_ML.columns))
plt.xticks(ticks, np.arange(1, len(plane_weather_for_ML.columns) + 1), rotation=90)
plt.yticks(ticks, np.arange(1, len(plane_weather_for_ML.columns) + 1), rotation=0)
plt.title('Correlation Matrix of Variables')
plt.savefig('/home/onyxia/work/Avions-Retard-et-Meteo/2_Data_exploration/pictures/8_Corr_matrix.png', dpi=300)

