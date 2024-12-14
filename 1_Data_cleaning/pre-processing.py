#Requirements

#pip install boto3


#pas nécessairement utile de télécharger AMZ CLI
#curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#unzip awscliv2.zip
#sudo ./aws/install

#aws configure
#keys, region and default output format (txt)

import boto3
import pandas as pd
import matplotlib.pyplot as plt
import io
import os
import numpy as np

'''
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

#s3://avion-et-meteo/Data-preprocessing/

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

#Defining functions to be used later

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
        print(f"Le document a été chargé avec succès dans le bucket S3 '{bucket_name}' sous le nom '{file_name}'.")
    except Exception as e:
        print(f"Une erreur s'est produite lors du chargement : {e}")

    buffer.close()

def check_nan_columns(df):
    nan_columns = df.columns[df.isna().any()].tolist()
    for col in nan_columns:
        nan_count = df[col].isna().sum()
        print(f"Colonne '{col}' contient {nan_count} valeurs NaN.")

#Part 1: Cleaning data (pre-processing)

#Part 1.1 : Pre-processing the planes data

#Hypothèse de travail : les avions sont similairement sensibles aux mêmes variations de météo sur leur retard --> on peut généraliser la situation d'un aéroports aux autres
#On décide de se concentrer sur l'aéroport JFK dont le code est : 10135
#Merging the monthly datasets to obtain a dataset for 2017
january_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_january.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(january_JFK)) #191
february_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_february.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(february_JFK)) #128
march_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_march.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(march_JFK)) #167
april_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_april.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(april_JFK)) #139
may_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_may.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(may_JFK)) #160
june_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_june.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(june_JFK)) #134
july_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_july.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(july_JFK)) #192
september_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_september.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(september_JFK)) #206
october_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_october.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(october_JFK)) #253
november_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_november.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(november_JFK)) #220
december_JFK = pd.read_csv('Data-preprocessing/T_ONTIME_REPORTING_december.csv')[lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] #maybe too slow
print(len(december_JFK)) #168
#Total = 1958
year = [january_JFK, february_JFK, march_JFK, april_JFK, may_JFK, june_JFK, july_JFK, september_JFK, october_JFK, november_JFK, december_JFK]
JFK_2017 = pd.concat(year, ignore_index=True)
#print(len(JFK_2017))
print(JFK_2017.info())




#Mettre dans le bon format
JFK_2017['FL_DATE'] = pd.to_datetime(JFK_2017['FL_DATE'])
#Hypothèse : on remplace les valeurs manquantes de WEATHER_DELAY dans JFK_2017 par 0 car on suppose qu'un retard cause beaucoup de colère et donc sera noté plus fréquemment qu'une absence de retard
JFK_2017['WEATHER_DELAY'] = JFK_2017['WEATHER_DELAY'].fillna(0)
JFK_2017['DEP_DELAY'] = JFK_2017['DEP_DELAY'].fillna(0)
JFK_2017['CARRIER_DELAY'] = JFK_2017['CARRIER_DELAY'].fillna(0)
JFK_2017['WEATHER_DELAY'] = JFK_2017['WEATHER_DELAY'].fillna(0)
JFK_2017['ARR_DELAY'] = JFK_2017['ARR_DELAY'].fillna(0)

#Removing NaN per rows
check_nan_columns(JFK_2017)
#Colonne 'DEP_TIME' contient 36 valeurs NaN.
#Colonne 'ARR_TIME' contient 39 valeurs NaN.
JFK_2017 = JFK_2017.dropna(axis=0)
check_nan_columns(JFK_2017) #nothing
print(len(JFK_2017)) #1919


#Combining departure time information to obtain a column with year, month, day, hour, minute for departure

# Step 1: Convert 'Actual Departure Time' from string (hhmm) to a timedelta
JFK_2017['DEP_TIME'] = JFK_2017['DEP_TIME'].astype(str).str.replace(r'\.0$', '', regex=True)
JFK_2017['DEP_TIME'] = JFK_2017['DEP_TIME'].astype(str).str.zfill(4)  # Ensure it's 4 digits
JFK_2017['Hours'] = JFK_2017['DEP_TIME'].str[:2].astype(int)  # Get hours as integer
JFK_2017['Minutes'] = JFK_2017['DEP_TIME'].str[2:].astype(int)  # Get minutes as integer

# Create a timedelta object from the hours and minutes
JFK_2017['departure_time'] = pd.to_timedelta(JFK_2017['Hours'], unit='h') + pd.to_timedelta(JFK_2017['Minutes'], unit='m')

# Step 2: Combine 'FL_DATE' (which is already in datetime) with 'departure_time' to get the full datetime
JFK_2017['Full_Departure_Datetime'] = JFK_2017['FL_DATE'] + JFK_2017['departure_time']

# Step 3: Drop intermediary columns if not needed
JFK_2017.drop(['Hours', 'Minutes', 'departure_time'], axis=1, inplace=True)

# Show the resulting DataFrame with the combined datetime
print(JFK_2017[['FL_DATE', 'DEP_TIME', 'Full_Departure_Datetime']].head())

#Isolating the data not to be used for machine learning 
JKF_no_number_data = JFK_2017[['Full_Departure_Datetime', 'FL_DATE','OP_UNIQUE_CARRIER','OP_CARRIER_AIRLINE_ID','OP_CARRIER','TAIL_NUM','OP_CARRIER_FL_NUM','ORIGIN_AIRPORT_ID','ORIGIN_AIRPORT_SEQ_ID','ORIGIN_CITY_MARKET_ID','DEST_AIRPORT_ID','DEST_CITY_MARKET_ID','DEST', 'DEP_TIME','ARR_TIME']]
JFK_numbers = JFK_2017[['DEP_DELAY','ARR_DELAY','CANCELLED','CARRIER_DELAY','WEATHER_DELAY','Full_Departure_Datetime']]
JFK_numbers['CANCELLED'] = JFK_numbers['CANCELLED'].astype(int)
print(JFK_numbers.info())


#Exporting the datasets
JFK_2017.to_csv("/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/JFK_2017.xlsx", index=False)
upload_to_s3("Pre-Processed_data", "JFK_2017.xlsx")
JKF_no_number_data.to_csv("/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/JKF_no_number_data.xlsx", index=False)
upload_to_s3("Pre-Processed_data", "JKF_no_number_data.xlsx")
JFK_numbers.to_csv("/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/JFK_numbers.xlsx", index=False)
upload_to_s3("Pre-Processed_data", "JFK_numbers.xlsx")



#Partie 1.2 : Pre-processing the weather data

weather = pd.read_csv('Data-preprocessing/jfk_weather.csv')
print(weather.info()) #beaucoup de type ne sont pas bien définis
#90 colonnes
weather['DATE'] = pd.to_datetime(weather['DATE'])

weather_2017 = weather[weather['DATE'].dt.year == 2017]
#print(weather_2017.head())
#print(weather_2017.tail())


# Conversion des types des colonnes
for col, col_type in column_types.items():
    if col in weather_2017.columns:
        try:
            weather_2017[col] = weather_2017[col].astype(col_type)
        except ValueError:
            print(f"Erreur de conversion pour la colonne {col} vers {col_type}. Utilisation de valeurs NaN pour les valeurs non compatibles.")
            if col_type == 'float64':
                weather_2017[col] = pd.to_numeric(weather_2017[col], errors='coerce')
            elif col_type == 'int64':
                weather_2017[col] = pd.to_numeric(weather_2017[col], errors='coerce').astype('Int64')

# Afficher les types des colonnes pour vérifier
print(weather_2017.dtypes)
print(weather_2017.head())
local_path = "/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/weather_2017.xlsx"






# Extraire les colonnes qui contiennent "Monthly", "Hourly" ou "Daily"
monthly_columns = [col for col in weather_2017.columns if 'Monthly' in col]
hourly_columns = [col for col in weather_2017.columns if 'HOURLY' in col]
daily_columns = [col for col in weather_2017.columns if 'DAILY' in col]

# Convertir la colonne DATE en datetime pour faciliter la gestion des périodes
weather_2017['DATE'] = pd.to_datetime(weather_2017['DATE'])
weather_2017['YearMonth'] = weather_2017['DATE'].dt.to_period('M')  # Extraire l'année et le mois
weather_2017['YearDayHour'] = weather_2017['DATE'].dt.to_period('H')  # Extraire l'année, jour et heure
weather_2017['YearDay'] = weather_2017['DATE'].dt.to_period('D')  # Extraire l'année et jour

# Fonction pour remplir les valeurs par mois / jour / heure
def fill_periodic_values(df, columns, period_key):
    for col in columns:
        if col in df.columns:
            # Utiliser les groupes par période pour remplir les NaN avec ffill et bfill
            df[col] = df.groupby(period_key)[col].transform(lambda group: group.ffill().bfill())

fill_periodic_values(weather_2017, monthly_columns, 'YearMonth')
fill_periodic_values(weather_2017, daily_columns, 'YearDay')
fill_periodic_values(weather_2017, hourly_columns, 'YearDayHour')

# Supprimer les colonnes temporaires
weather_2017.drop(columns=['YearMonth', 'YearDayHour', 'YearDay'], inplace=True)

# Vérifier les colonnes contenant des NaN dans weather_2017
     
#Some variables have value -9999 instead of NaN
#We replace them by NaN to remove them later
weather_2017 = weather_2017.replace(-9999, np.nan)


# Appliquer la vérification
check_nan_columns(weather_2017)

#Eliminer les colonnes ou les lignes avec trop de valeurs Nan au cas par cas
# Supprimer les colonnes avec plus de 1000 valeurs NaN
weather_2017 = weather_2017.dropna(axis=1, thresh=len(weather_2017) - 1000)
print("Vérification : ")
check_nan_columns(weather_2017)

# Afficher les premiers résultats pour validation
print(weather_2017.head())
print(len(weather_2017)) #13201

weather_2017 = weather_2017.dropna(axis=0)
check_nan_columns(weather_2017) #nothing

print(len(weather_2017)) #13027


#Deletion of useless columns (because of weather encoding standards (str whose meaning is not easily retrievable), complex units like angles, no variance, etc...)
inutile = ['STATION','STATION_NAME','ELEVATION','LATITUDE','LONGITUDE', 'REPORTTPYE', 'HOURLYSKYCONDITIONS', 'HOURLYWindDirection', 'MonthlyDaysWithLT0Temp', 'DAILYSustainedWindDirection']
weather_2017.drop(columns=inutile, inplace=True)

#Hyptohesis: T is used to indicate a quantity observed was too low to be measured, we assume it is equal to zero
weather_2017 = weather_2017.replace('T', 0)

#Some variables have values equal to a number followed by a character, we keep only the number by using regex
for col in weather_2017.columns:
    weather_2017[col] = weather_2017[col].replace(r'(\d+(\.\d+)?)([^\d\s]+)$', r'\1', regex=True)





print(weather_2017.head())

#we delete columns that represents the same thing but with different units (like celsius VS Farenheit)
#we keep Fahrenheit because some variables do not have the celsius equivalent (American weather)
Celsius = ['HOURLYDRYBULBTEMPC', 'HOURLYWETBULBTEMPC', 'HOURLYDewPointTempC']
weather_2017.drop(columns=Celsius, inplace=True)

#deleting columns for which the unit is too complex to use
#Complex = ['DAILYSustainedWindDirection']
#weather_2017.drop(columns=Complex, inplace=True)

#We set all variables to be float, expect time
weather_2017 = pd.concat([weather_2017[['DATE']], weather_2017.iloc[:, 1:].astype(float)], axis=1)


#weather_2017 = weather_2017['DATE'] + weather_2017.iloc[:,1:].astype(float)
print(weather_2017.info())
print(weather_2017.head())
weather_2017.to_csv(local_path, index=False)

upload_to_s3("Pre-Processed_data", "weather_2017.xlsx")
'''



#Part 1.3: merging the two datasets

#JFK_2017.to_csv("/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/JFK_2017.xlsx", index=False)
path_JFK = "/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/JFK_numbers.xlsx"
path_weather = "/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/weather_2017.xlsx"

JFK_numbers = pd.read_csv(path_JFK)
weather_2017 = pd.read_csv(path_weather)

print(JFK_numbers)
print(weather_2017)
#nb of columns to be obtained: 6 + 45 - 1 = 50

#AUTRE SOLUTION : ne pas faire de merge sur les données exactes ????


#Are any time data equal?
exact_matches = pd.merge(JFK_numbers, weather_2017, how='inner', left_on='Full_Departure_Datetime', right_on='DATE')
print(exact_matches) #len 60

JFK_no_exact_match = JFK_numbers[~JFK_numbers['Full_Departure_Datetime'].isin(exact_matches['Full_Departure_Datetime'])]
print(JFK_no_exact_match) #len ok

'''
#be sure of the type
JFK_no_exact_match['Full_Departure_Datetime'] = pd.to_datetime(JFK_no_exact_match['Full_Departure_Datetime'])
weather_2017['DATE'] = pd.to_datetime(weather_2017['DATE'])

JFK_no_exact_match['rounded_datetime'] = JFK_no_exact_match['Full_Departure_Datetime'].dt.round('15min')
weather_2017['rounded_datetime'] = weather_2017['DATE'].dt.round('15min')'''

'''# Fusion des données sur la colonne arrondie
merged_df = pd.merge(JFK_no_exact_match, weather_2017, how='left', left_on='rounded_datetime', right_on='rounded_datetime')

# Remplissage des valeurs manquantes avec les valeurs les plus proches (backfill ou nearest)
merged_df = merged_df.fillna(method='nearest')'''

import pandas as pd
import numpy as np
from scipy.spatial import cKDTree

# Convertir les colonnes en datetime (si ce n'est pas déjà fait)
JFK_no_exact_match['Full_Departure_Datetime'] = pd.to_datetime(JFK_no_exact_match['Full_Departure_Datetime'])
weather_2017['DATE'] = pd.to_datetime(weather_2017['DATE'])
print(len(JFK_no_exact_match))
print('ICICICICICICICIC')
# Arrondir les dates à 15 minutes
JFK_no_exact_match['rounded_datetime'] = JFK_no_exact_match['Full_Departure_Datetime'].dt.round('15min')
weather_2017['rounded_datetime'] = weather_2017['DATE'].dt.round('15min')
print(len(JFK_no_exact_match))

#jusque ici ok

# Fusion des données sur la colonne arrondie
#merged_df = pd.merge(JFK_no_exact_match, weather_2017, how='left', left_on='rounded_datetime', right_on='rounded_datetime')
merged_df = pd.merge(JFK_no_exact_match, weather_2017, how='left', left_on='rounded_datetime')
print(merged_df)
# Remplissage des valeurs manquantes avec la valeur la plus proche dans le temps en utilisant cKDTree


# Créer un tableau des timestamps pour les valeurs non nulles de weather_2017
weather_tree = cKDTree(weather_2017['rounded_datetime'].values.astype(np.int64).reshape(-1, 1))

# Parcourir toutes les colonnes du dataframe fusionné
for column in merged_df.columns:
    # Si la colonne contient des valeurs manquantes (NaN), on va chercher la valeur la plus proche
    if merged_df[column].isna().any():
        # Trouver les lignes avec des valeurs manquantes dans la colonne
        missing_rows = merged_df[merged_df[column].isna()]
        if not missing_rows.empty:
            missing_times = missing_rows['rounded_datetime'].values.astype(np.int64).reshape(-1, 1)
            # Trouver les indices des valeurs les plus proches dans weather_2017
            dist, idx = weather_tree.query(missing_times, k=1)
            # Remplir les valeurs manquantes avec la valeur la plus proche pour cette colonne
            merged_df.loc[merged_df[column].isna(), column] = weather_2017.iloc[idx][column].values

# Afficher le dataframe fusionné avec les valeurs manquantes remplies
#Be careful for processing, they are three columns for time identification: Full_Departure_Datetime from JFK_numbers, rounded_datetime, and DATE from weather_2017
print(merged_df.columns)
#merged_df = pd.concat([exact_matches, merged_df])
print(merged_df)



#we replace the calculated values that coincide with exact matches by the real value found in exact matches
merged_df = merged_df[~merged_df['Full_Departure_Datetime'].isin(exact_matches['Full_Departure_Datetime'])]
print(merged_df)
merged_df = pd.concat([exact_matches, merged_df])
print(merged_df)







#merged_df = pd.merge(JFK_numbers, weather_2017, left_on='Full_Departure_Datetime', right_on='DATE', how='left')
#print(len(merged_df)) #goal 1919
#print(merged_df.head())

#for weather its DATE

#upload_to_s3("Pre-Processed_data", "merged_df.xlsx")





