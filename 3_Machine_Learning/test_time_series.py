#Requirements

import pandas as pd
import matplotlib.pyplot as plt
import io
import os
import numpy as np
from datetime import timedelta
import seaborn as sns
import matplotlib.dates as mdates
import s3fs




#Download the files from leoacpr by typing your SSP Cloud username
#This can take a while because the files are heavy

fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})

MY_BUCKET = "leoacpr"
source_folder = f"{MY_BUCKET}/diffusion/Pre-processing"
files_in_source = fs.ls(source_folder)


#Downloading the dataframes
dataframes = {}

for files in fs.ls(f"{MY_BUCKET}/diffusion/Pre-processed_data"):
    with fs.open(files, "r") as file_in:
            df_imported = pd.read_csv(file_in)
            print(f"Downloading {files}")
    # Dictionnary of dataframes with the name of the file as a key
    dataframes[f"{files.split('/')[-1]}"] = df_imported

print(dataframes['plane_weather.csv'])


#Load the data
plane_weather = dataframes['plane_weather.csv']
plane_weather_for_ML = dataframes['plane_weather_for_ML.csv']
JFK_2017_number = dataframes['JFK_2017_number.csv']
weather_2017 = dataframes['weather_2017.csv']
plane_weather.drop(columns=['Unnamed: 0'], inplace=True)
plane_weather_for_ML.drop(columns=['Unnamed: 0'], inplace=True)
JFK_2017_number.drop(columns=['Unnamed: 0'], inplace=True)
weather_2017.drop(columns=['Unnamed: 0'], inplace=True)

print(plane_weather)
plane_weather.to_csv('Avions-Retard-et-Meteo/3_Machine_Learning/plane_weather.csv')