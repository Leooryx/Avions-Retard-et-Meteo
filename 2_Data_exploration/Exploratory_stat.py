#Data-exploration

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

#Load the data and remove useless columns
plane_weather = dataframes['plane_weather.csv']
plane_weather_for_ML = dataframes['plane_weather_for_ML.csv']
JFK_2017_number = dataframes['JFK_2017_number.csv']
weather_2017 = dataframes['weather_2017.csv']
plane_weather.drop(columns=['Unnamed: 0'], inplace=True)
plane_weather_for_ML.drop(columns=['Unnamed: 0'], inplace=True)
JFK_2017_number.drop(columns=['Unnamed: 0'], inplace=True)
weather_2017.drop(columns=['Unnamed: 0'], inplace=True)


#STEP 1: Exploring the plane and weather datasets

plane_weather['Full_Departure_Datetime'] = pd.to_datetime(plane_weather['Full_Departure_Datetime'])
plane_weather['DATE_weather'] = pd.to_datetime(plane_weather['DATE_weather'])

# Mean delays per month
plane_weather['Month'] = plane_weather['Full_Departure_Datetime'].dt.month
monthly_delays = plane_weather.groupby('Month')[['DEP_DELAY', 'ARR_DELAY']].mean()
plt.figure(figsize=(10, 6))
monthly_delays.plot(kind='bar', figsize=(12, 6))
plt.title("Mean delays per month", fontsize=16)
plt.ylabel("Mean delay (minutes)", fontsize=12)
plt.xlabel("Month", fontsize=12)
plt.xticks(range(0, 12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
plt.legend(["Departure delay", "Arrival delay"])
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('Avions-Retard-et-Meteo/2_Data_exploration/pictures/1_mean_delays.png')


# Distribution of departure delays
plt.figure(figsize=(10, 6))
sns.histplot(plane_weather['DEP_DELAY'], bins=50, kde=True, color='blue', edgecolor='black')
plt.title("Distribution of departure delays", fontsize=16)
plt.xlabel("Departure delay (minutes)", fontsize=12)
plt.ylabel("Number of flights", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('Avions-Retard-et-Meteo/2_Data_exploration/pictures/2_distribution_delays.png')

# Distribution of weather delays
plt.figure(figsize=(10, 6))
sns.histplot(plane_weather['WEATHER_DELAY'], bins=50, kde=True, color='orange', edgecolor='black')
plt.title("Distribution of weather delays", fontsize=16)
plt.xlabel("Weather delays (minutes)", fontsize=12)
plt.ylabel("Numbers of flights", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
plt.savefig('Avions-Retard-et-Meteo/2_Data_exploration/pictures/3_Distrib_weather_delays.png')
#upload_to_s3("Pictures", "3_Distrib_retard_météo.png")

# Sum of weather delays per months
weather_delay_monthly = plane_weather.groupby('Month')['WEATHER_DELAY'].sum()
plt.figure(figsize=(10, 6))
weather_delay_monthly.plot(kind='bar', color='teal', alpha=0.8, edgecolor='black')
plt.title("Sum of weather delays per month", fontsize=16)
plt.ylabel("Sum delays (minutes)", fontsize=12)
plt.xlabel("Month", fontsize=12)
plt.xticks(range(0, 12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('Avions-Retard-et-Meteo/2_Data_exploration/pictures/4_sum_weather_delays.png')

plane_weather.drop(columns=['Month'], inplace=True)


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
plt.savefig('Avions-Retard-et-Meteo/2_Data_exploration/pictures/5_Proportions_of_delays.png')
plane_weather = plane_weather.drop(columns=['carrier_delay_ratio', 'weather_delay_ratio', 'unexplained_delay_ratio'])


#Weather trends for the year 2017
plt.figure(figsize=(8.27, 11.69))  # A4 size (in inches)
plt.suptitle('Weather Characterization Throughout 2017', fontsize=16, fontweight='bold')

# Function to format subplots
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
plt.grid(axis='y', linestyle='--', alpha=0.7)
ax2 = plt.subplot(4, 1, 2)
format_subplot(ax2, plane_weather, 'Full_Departure_Datetime', 'DAILYPrecip', 'Daily Precip', 'black', 'Precipitation')
plt.grid(axis='y', linestyle='--', alpha=0.7)
ax3 = plt.subplot(4, 1, 3)
format_subplot(ax3, plane_weather, 'Full_Departure_Datetime', 'DAILYSnowDepth', 'Daily Snow', 'blue', 'Snow Depth')
plt.grid(axis='y', linestyle='--', alpha=0.7)
ax4 = plt.subplot(4, 1, 4)
format_subplot(ax4, plane_weather, 'Full_Departure_Datetime', 'HOURLYStationPressure', 'Pressure', 'gray', 'Pressure (in Hg)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to avoid title overlap
plt.savefig('Avions-Retard-et-Meteo/2_Data_exploration/pictures/6_weather_2017_summary.png', dpi=300)



#Plot month by month weather

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
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
plt.suptitle('Weather Month by Month', fontsize=16, fontweight='bold')

plt.legend(loc='center', bbox_to_anchor=(-1.2, -0.09), ncol=4) 
plt.tight_layout(rect=[0, 0, 1, 0.95]) # Adjust layout for title

plt.savefig('Avions-Retard-et-Meteo/2_Data_exploration/pictures/7_month_by_month.png', dpi=300)

plane_weather['DAILYPrecip'] = plane_weather['DAILYPrecip']/10 #to remove the modification




#STEP 2: finding relations between the variables
plane_weather_for_ML = plane_weather_for_ML.drop(columns=['CANCELLED'])
corr_matrix = plane_weather_for_ML.corr()
plt.figure(figsize=(13, 11))
sns.heatmap(corr_matrix, annot=False, cmap='RdYlGn', center=0, cbar_kws={'label': 'Correlation Coefficient'}, linewidths=0.4, linecolor='black')
ticks = np.arange(len(plane_weather_for_ML.columns))

plt.xticks(ticks=np.arange(len(plane_weather_for_ML.columns)), labels=plane_weather_for_ML.columns, rotation=90)
plt.yticks(ticks=np.arange(len(plane_weather_for_ML.columns)), labels=plane_weather_for_ML.columns, rotation=0)

plt.title('Correlation Matrix of Variables')
plt.savefig('Avions-Retard-et-Meteo/2_Data_exploration/pictures/8_Corr_matrix.png', dpi=300)

#Isolating the variables with a strong correlation
threshold = 0.7
strongly_correlated_pairs = []
variables_to_remove = set()
for i in range(len(corr_matrix.columns)):
    for j in range(i):
        if abs(corr_matrix.iloc[i, j]) > threshold:  # Si la corrélation est au-dessus du seuil
            strongly_correlated_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_matrix.iloc[i, j]))
            variables_to_remove.add(corr_matrix.columns[j])

for pair in strongly_correlated_pairs:
    print(f'Variables: {pair[0]} & {pair[1]}, Corrélation: {pair[2]:.2f}')



#We remove some strongly correlated variables
#We remove cancel because it doesnt add any insight
variables_to_keep = [var for var in corr_matrix.columns if var not in variables_to_remove and var != 'CANCELLED']
variables_to_keep.append('DEP_DELAY') #we keep DEP_DELAY because this is the variable with the most information about delays
print("\nVariables to keep :", variables_to_keep)



# We delete the useless variables in the dataframe
plane_weather_no_corr = plane_weather[variables_to_keep]
print(plane_weather_no_corr) #18 variables


#looking for temporal relations --> machine learning / time series
plane_weather_reduced = pd.concat([plane_weather[['Full_Departure_Datetime']], plane_weather_no_corr], axis=1)
print(plane_weather_reduced.info())



#Scatter plots:

# Variables of interest
variables_of_interest = ['DEP_DELAY', 'WEATHER_DELAY']

# Calculations for the grid
n_vars = len(variables_to_keep)
n_cols = 8  # Adjust as needed for better visualization
n_rows = 4
fig, axes = plt.subplots(n_rows, n_cols, figsize=(20, 10))

# Flatten axes for easier indexing
axes = axes.flatten()

# Counter for axes index
ax_idx = 0

# Generate scatter plots for DEP_DELAY and WEATHER_DELAY against other variables
for var in variables_of_interest:
    for other_var in [v for v in plane_weather_no_corr.columns if v != var]:
        sns.scatterplot(x=plane_weather_no_corr[other_var], 
                        y=plane_weather_no_corr[var], 
                        ax=axes[ax_idx], 
                        color='blue', s=5)
        
        axes[ax_idx].set_xlabel(other_var, fontsize=8)
        axes[ax_idx].set_ylabel(var, fontsize=8)
        axes[ax_idx].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        axes[ax_idx].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
        
        # Move to next axis
        ax_idx += 1

# Mask any remaining empty axes
for i in range(ax_idx, len(axes)):
    axes[i].axis('off')

plt.tight_layout()



plt.savefig('Avions-Retard-et-Meteo/2_Data_exploration/pictures/9_Scatter_plot.png', dpi=300)
#plt.show()












