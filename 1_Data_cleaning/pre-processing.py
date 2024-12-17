#Data-preprocessing

#Requirements


#pas nécessairement utile de télécharger AMZ CLI
#curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#unzip awscliv2.zip
#sudo ./aws/install

#aws configure
#keys, region and default output format (txt)

#pip install boto3
#import boto3
import pandas as pd
import matplotlib.pyplot as plt
import io
import os
import numpy as np
from datetime import timedelta



#test without private S3

#Download the files from leoacpr by typing your SSP Cloud username
#This can take a while because the files are heavy

import s3fs

fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})

MY_BUCKET = "leoacpr"
print(fs.ls(MY_BUCKET))
source_folder = f"{MY_BUCKET}/diffusion/Pre-processing"
files_in_source = fs.ls(source_folder)

YOUR_BUCKET = str(input("Type your bucket: \n"))


source_folder = f"{MY_BUCKET}/diffusion/Pre-processing"
files_in_source = fs.ls(source_folder)

import s3fs
import pandas as pd

# Initialiser l'accès à MinIO avec s3fs
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})

# Définir le bucket source et le dossier source
MY_BUCKET = "leoacpr"
source_folder = f"{MY_BUCKET}/diffusion/Pre-processing"

# Liste tous les fichiers dans le dossier source
files_in_source = fs.ls(source_folder)

# Dictionnaire pour stocker les DataFrames


# Parcourir tous les fichiers du dossier source
for file_path_in_s3 in files_in_source:
    file_name = file_path_in_s3.split('/')[-1]  # Nom du fichier sans le chemin complet

    # Vérifier si le fichier n'existe pas déjà dans le dossier de destination
    if fs.ls(f"{MY_BUCKET}/diffusion/Pre-processing") != fs.ls(f"{YOUR_BUCKET}/diffusion/Pre-processing"):
        file_path_for_you = f"{YOUR_BUCKET}/diffusion/Pre-processing/{file_name}"

        # Importer le fichier depuis S3 dans un DataFrame
        with fs.open(file_path_in_s3, "r") as file_in:
            df_imported = pd.read_csv(file_in)
        
        # Sauvegarder le fichier dans YOUR_BUCKET
        with fs.open(file_path_for_you, "w") as file_out:
            df_imported.to_csv(file_out)
        
        print(f"File {file_name} has been successfully copied to {file_path_for_you}")

#Create folders inside S3
if not fs.exists(f"{YOUR_BUCKET}/diffusion/Pre-processed_data"):
    fs.touch(f"{YOUR_BUCKET}/diffusion/.{Pre-processed_data}]")

#Creating the variables
dataframes = {}

for files in fs.ls(f"{YOUR_BUCKET}/diffusion/Pre-processing"):
    with fs.open(files, "r") as file_in:
            df_imported = pd.read_csv(file_in)
            print(f"Downloading {files}")
    # Ajouter le DataFrame dans le dictionnaire en utilisant le nom du fichier comme clé
    dataframes[f"{files.split('/')[-1]}"] = df_imported

# Exemple : Accéder à un DataFrame spécifique
# Par exemple, pour accéder au DataFrame du fichier "january.csv"
print(dataframes['T_ONTIME_REPORTING_january.csv'])
#ok ça marche


'''

#Opening and reading the .env file
#JAMAIS DE CHEMIN ABSOLU !!!!!
#Avions-Retard-et-Meteo/.env
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

def check_nan_columns(df):
    """Checks and prints the columns containing NaN values

    Args:
        df (pd.dataframe): a dataframe
    """

    nan_columns = df.columns[df.isna().any()].tolist()
    for col in nan_columns:
        nan_count = df[col].isna().sum()
        print(f"Colonne '{col}' contient {nan_count} valeurs NaN.")







#Part 1: Cleaning data (pre-processing)

#Part 1.1 : Pre-processing the planes data

#Hypothesis: plane's delays are similarly sensitive to weather variations --> we can generalize the situation for an airpot to others
#We decide to focus on JFK airport, whose identification number is 10135

#Merging the monthly datasets to obtain a dataset for 2017
january_JFK = dataframes['T_ONTIME_REPORTING_january.csv'][lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] 
print(len(january_JFK)) #191
february_JFK = dataframes['T_ONTIME_REPORTING_february.csv'][lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] 
print(len(february_JFK)) #128
march_JFK = dataframes['T_ONTIME_REPORTING_march.csv'][lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] 
print(len(march_JFK)) #167
april_JFK = dataframes['T_ONTIME_REPORTING_april.csv'][lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] 
print(len(april_JFK)) #139
may_JFK = dataframes['T_ONTIME_REPORTING_may.csv'][lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] 
print(len(may_JFK)) #160
june_JFK = dataframes['T_ONTIME_REPORTING_june.csv'][lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] 
print(len(june_JFK)) #134
july_JFK = dataframes['T_ONTIME_REPORTING_july.csv'][lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] 
print(len(july_JFK)) #192
august_JFK = dataframes['T_ONTIME_REPORTING_august.csv'][lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] 
print(len(august_JFK)) #180
september_JFK = dataframes['T_ONTIME_REPORTING_september.csv'][lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] 
print(len(september_JFK)) #206
october_JFK = dataframes['T_ONTIME_REPORTING_october.csv'][lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] 
print(len(october_JFK)) #253
november_JFK = dataframes['T_ONTIME_REPORTING_november.csv'][lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] 
print(len(november_JFK)) #220
december_JFK = dataframes['T_ONTIME_REPORTING_december.csv'][lambda df: df["ORIGIN_AIRPORT_ID"] == 10135] 
print(len(december_JFK)) #168
#Total size = 2138
year = [january_JFK, february_JFK, march_JFK, april_JFK, may_JFK, june_JFK, july_JFK, august_JFK, september_JFK, october_JFK, november_JFK, december_JFK]
JFK_2017 = pd.concat(year, ignore_index=True)
print(JFK_2017)
#print(len(JFK_2017))


#Setting the rights data types
print(JFK_2017.info())
JFK_2017['FL_DATE'] = pd.to_datetime(JFK_2017['FL_DATE'])


#Hypothesis : we can replaces the missing values for delays by 0 because we suppose that a delay is more likely to be registered than no delay because it creates more frustration
JFK_2017['WEATHER_DELAY'] = JFK_2017['WEATHER_DELAY'].fillna(0)
JFK_2017['DEP_DELAY'] = JFK_2017['DEP_DELAY'].fillna(0)
JFK_2017['CARRIER_DELAY'] = JFK_2017['CARRIER_DELAY'].fillna(0)
JFK_2017['WEATHER_DELAY'] = JFK_2017['WEATHER_DELAY'].fillna(0)
JFK_2017['ARR_DELAY'] = JFK_2017['ARR_DELAY'].fillna(0)

#Removing NaN per rows
check_nan_columns(JFK_2017)
#'DEP_TIME' has 36  NaN.
#'ARR_TIME' has 39 valeurs NaN.
JFK_2017 = JFK_2017.dropna(axis=0)
check_nan_columns(JFK_2017) #nothing --> no more NaN
print(len(JFK_2017)) #1919


#Combining departure time information to obtain a column with year, month, day, hour, minute for departure
#'DEP_TIME' contains str with numbers indicating the hours and minutes through the format "hhmm"
JFK_2017['DEP_TIME'] = JFK_2017['DEP_TIME'].astype(str).str.replace(r'\.0$', '', regex=True)
JFK_2017['DEP_TIME'] = JFK_2017['DEP_TIME'].astype(str).str.zfill(4)  # Ensure it's 4 digits
JFK_2017['Hours'] = JFK_2017['DEP_TIME'].str[:2].astype(int)  # Get hours as integer
JFK_2017['Minutes'] = JFK_2017['DEP_TIME'].str[2:].astype(int)  # Get minutes as integer
JFK_2017['departure_time'] = pd.to_timedelta(JFK_2017['Hours'], unit='h') + pd.to_timedelta(JFK_2017['Minutes'], unit='m')
JFK_2017['Full_Departure_Datetime'] = JFK_2017['FL_DATE'] + JFK_2017['departure_time']
JFK_2017.drop(['Hours', 'Minutes', 'departure_time'], axis=1, inplace=True)
print(JFK_2017[['FL_DATE', 'DEP_TIME', 'Full_Departure_Datetime']].head())

#Isolating the data for machine learning 
JFK_2017_no_number = JFK_2017[['Full_Departure_Datetime', 'FL_DATE','OP_UNIQUE_CARRIER','OP_CARRIER_AIRLINE_ID','OP_CARRIER','TAIL_NUM','OP_CARRIER_FL_NUM','ORIGIN_AIRPORT_ID','ORIGIN_AIRPORT_SEQ_ID','ORIGIN_CITY_MARKET_ID','DEST_AIRPORT_ID','DEST_CITY_MARKET_ID','DEST', 'DEP_TIME','ARR_TIME']]
JFK_2017_number = JFK_2017[['DEP_DELAY','ARR_DELAY','CANCELLED','CARRIER_DELAY','WEATHER_DELAY','Full_Departure_Datetime']]
JFK_2017_number['CANCELLED'] = JFK_2017_number['CANCELLED'].astype(int)
print(JFK_2017_number.info())

#Exporting the dataset for JFK planes
JFK_2017.to_csv("/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/JFK_2017.csv", index=False)
with fs.open(f"{YOUR_BUCKET}/diffusion/Pre-processed_data/JFK_2017.csv", "w") as path:
    JFK_2017.to_csv(path)

JFK_2017_no_number.to_csv("/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/JFK_2017_no_number.csv", index=False)
with fs.open(f"{YOUR_BUCKET}/diffusion/Pre-processed_data/JFK_2017_no_number.csv", "w") as path:
    JFK_2017_no_number.to_csv(path)

JFK_2017_number.to_csv("/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/JFK_2017_number.csv", index=False)
with fs.open(f"{YOUR_BUCKET}/diffusion/Pre-processed_data/JFK_2017_number.csv", "w") as path:
    JFK_2017_number.to_csv(path)




#Part 1.2 : Pre-processing the weather data

#We take only the data for the year 2017
weather = dataframes['jfk_weather.csv']
weather['DATE'] = pd.to_datetime(weather['DATE'])
weather_2017 = weather[weather['DATE'].dt.year == 2017]
#print(weather_2017.head())
#print(weather_2017.tail())
print(weather.info()) 
#90 columns



#Columns with "Monthly", "Hourly" ou "Daily" contains only one value for the unit they represent.
# for example for a montlhy columns, only the last day of the corresponding month contains a value
# We need to extend this

# Extracting the columns "Monthly", "Hourly" ou "Daily"
monthly_columns = [col for col in weather_2017.columns if 'Monthly' in col]
hourly_columns = [col for col in weather_2017.columns if 'HOURLY' in col]
daily_columns = [col for col in weather_2017.columns if 'DAILY' in col]

# Conversion in datetime type
weather_2017['YearMonth'] = weather_2017['DATE'].dt.to_period('M')  # Extraire l'année et le mois
weather_2017['YearDayHour'] = weather_2017['DATE'].dt.to_period('H')  # Extraire l'année, jour et heure
weather_2017['YearDay'] = weather_2017['DATE'].dt.to_period('D')  # Extraire l'année et jour

# Filling the NaN values
def fill_periodic_values(df, columns, period_key):
    for col in columns:
        if col in df.columns:
            # Utiliser les groupes par période pour remplir les NaN avec ffill et bfill
            df[col] = df.groupby(period_key)[col].transform(lambda group: group.ffill().bfill())

fill_periodic_values(weather_2017, monthly_columns, 'YearMonth')
fill_periodic_values(weather_2017, daily_columns, 'YearDay')
fill_periodic_values(weather_2017, hourly_columns, 'YearDayHour')

# Deleting the temporary columns
weather_2017.drop(columns=['YearMonth', 'YearDayHour', 'YearDay'], inplace=True)


# Veryfying other columns with NaN
     
# Some variables have value -9999 instead of NaN
# We replace them by NaN to remove them later
weather_2017 = weather_2017.replace(-9999, np.nan)

check_nan_columns(weather_2017)

# We remove the columns containg more than 1000 NaN values
weather_2017 = weather_2017.dropna(axis=1, thresh=len(weather_2017) - 1000)
check_nan_columns(weather_2017)
#print(len(weather_2017)) #13201
weather_2017 = weather_2017.dropna(axis=0)
check_nan_columns(weather_2017) #nothing
#print(len(weather_2017)) #13027


#Deletion of useless columns (because of weather encoding standards (str whose meaning is not easily retrievable), complex units like angles, no variance, etc...)
inutile = ['STATION','STATION_NAME','ELEVATION','LATITUDE','LONGITUDE', 'REPORTTPYE', 'HOURLYSKYCONDITIONS', 'HOURLYWindDirection', 'MonthlyDaysWithLT0Temp', 'DAILYSustainedWindDirection']
weather_2017.drop(columns=inutile, inplace=True)

#Hyptohesis: 'T' is used to indicate a quantity observed was too low to be measured, we assume it is equal to zero
weather_2017 = weather_2017.replace('T', 0)

#Some variables have values equal to a number followed by a character, we keep only the number by using regex
for col in weather_2017.columns:
    weather_2017[col] = weather_2017[col].replace(r'(\d+(\.\d+)?)([^\d\s]+)$', r'\1', regex=True)

#print(weather_2017.head())

# We delete columns that represents the same thing but with different units (like celsius VS Farenheit)
# we keep Fahrenheit because some variables do not have the celsius equivalent (American weather)
Celsius = ['HOURLYDRYBULBTEMPC', 'HOURLYWETBULBTEMPC', 'HOURLYDewPointTempC']
weather_2017.drop(columns=Celsius, inplace=True)

#We set all variables to be float, expect time
weather_2017 = pd.concat([weather_2017[['DATE']], weather_2017.iloc[:, 1:].astype(float)], axis=1)

print(weather_2017.info())
print(weather_2017.head())
weather_2017.to_csv("/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/weather_2017.csv", index=False)
with fs.open(f"{YOUR_BUCKET}/diffusion/Pre-processed_data/weather_2017.csv", "w") as path:
    weather_2017.to_csv(path)




#Part 1.3: merging the two datasets




# Convertir les colonnes de dates en format datetime
#JFK_numbers['Full_Departure_Datetime'] = pd.to_datetime(JFK_numbers['Full_Departure_Datetime'])
#weather_2017['DATE'] = pd.to_datetime(weather_2017['DATE'])

# Conversion of data time to numpy.datetime64 type to accelerate comparisons 
departure_times = JFK_numbers['Full_Departure_Datetime'].values.astype('datetime64[m]')  # minutes
weather_times = weather_2017['DATE'].values.astype('datetime64[m]')  # minutes

#Hypothesis: the weather is the same for each 30-min interval of time
tolerance = np.timedelta64(30, 'm')

merged_rows = []

#we want to find the minimum time difference between the plane departure and the measured weather
for departure_time in departure_times:
    time_differences = np.abs(departure_time - weather_times)
    closest_index = np.argmin(time_differences)
    
    # If the time difference is beow the tolerance, we combine the information from JFK_numbers and weather_2017
    if time_differences[closest_index] <= tolerance:
        closest_weather_row = weather_2017.iloc[closest_index]
        jfk_row = JFK_numbers.iloc[np.where(departure_times == departure_time)[0][0]]  # find the corresponding row
        merged_row = pd.concat([jfk_row, closest_weather_row], axis=0)
        merged_rows.append(merged_row)

# Combining all the rows that were accepted
merged_df = pd.DataFrame(merged_rows, columns=np.concatenate([JFK_numbers.columns, weather_2017.columns]))

print(merged_df['Full_Departure_Datetime'])
#only about 10 rows were lost for a tolerance of 31min: acceptable 

# Uploading the data
merged_df.rename(columns={'DATE': 'DATE_weather'}, inplace=True)
merged_df.to_csv("/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/plane_weather.csv", index=False)
upload_to_s3("Pre-Processed_data", "plane_weather.csv")
print(merged_df.info())

plane_weather_for_ML = merged_df.drop(columns=['Full_Departure_Datetime', 'DATE_weather'])
plane_weather_for_ML.to_csv("/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/plane_weather_for_ML.csv", index=False)
upload_to_s3("Pre-Processed_data", "plane_weather_for_ML.csv")
check_nan_columns(merged_df)



