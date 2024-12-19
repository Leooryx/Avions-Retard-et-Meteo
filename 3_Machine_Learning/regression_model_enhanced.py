# This is approximately the same code as the first one, but we try to include new variables to
# enhance the model, thanks to te data exploration part (we refer to the images of this part by
# their number in the Avions-Retard-et-Meteo/2_Data_exploration/pictures folder)


# Import the packages and load the data
# pip install openpyxl
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import os


# Load the data
file_path = 'Avions-Retard-et-Meteo/1_Data_cleaning/plane_weather_for_ML.csv'
df = pd.read_csv(file_path)

# This variable seems important due to our previous conclusions
df['HeavyWind'] = (df['HOURLYWindSpeed'] > 30).astype(int)  # Threshold based on general aviation standards


# Image 4 highlights December as the month with the most weather-related delays.
# December typically has higher weather delays. Instead of months, we'll use average daily snowfall and snow depth.
df['HeavySnow'] = (df['DAILYSnowDepth'] > 5).astype(int)  # Snow depth > 5 inches indicates significant snow.



# Image 7: Add precipitation and snow-related aggregates
# Create rolling averages or monthly aggregates based on available daily or monthly precipitation and snow data.
df['RollingAvgPrecip'] = df['DAILYPrecip'].rolling(window=7, min_periods=1).mean()  # 7-day rolling avg for precipitation.
df['RollingSnowDepth'] = df['DAILYSnowDepth'].rolling(window=7, min_periods=1).mean()  # 7-day rolling avg for snow depth.


# Select features and target
exclude_columns = ['DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 'WEATHER_DELAY', 'CANCELLED'] # We can't use these variables in our model because they depend on whether or not the plane has been late or not
feature_columns = [col for col in df.columns if col not in exclude_columns]
target_column = 'DEP_DELAY' # The variable we want to predict

X = df[feature_columns]
y = df[target_column]


# Feature Importance (we get the feature importance by a random forest model)
rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg.fit(X, y)

# We get the most important features
importances = rf_reg.feature_importances_
feature_importance_df = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

# Then we select the most important features (example here the 10 most)
top_features = feature_importance_df.head(10)['Feature']
X_selected = X[top_features]


# This section is optionnal and only allows us to visualize the most important features
output_dir = 'Avions-Retard-et-Meteo/3_Machine_Learning/pictures'
os.makedirs(output_dir, exist_ok=True)
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'].head(10), feature_importance_df['Importance'].head(10))
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 10 Feature Importances")
plt.gca().invert_yaxis()  # Most important at the top
output_path = os.path.join(output_dir, "feature_importances_enhanced.png") # Save the image
plt.savefig(output_path, dpi=300, bbox_inches='tight')  # Haute qualité et marges ajustées
##################


# None of the variables created are in the feature importance, which seems to mean that they don't enhance the model