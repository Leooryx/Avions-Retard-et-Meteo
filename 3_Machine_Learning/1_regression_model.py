# Motivation
# Even though there seems to be very few delays due to weather, as shown by the data exploration,
# It could be possible that the variable weather delay don't include all of them, and maybe there
# is a way to predict them

# Import the packages and load the data
# pip install openpyxl
# pip install scikit-learn==1.5.2
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
from math import sqrt
import os
import s3fs
import joblib






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


#Load the data
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

df = plane_weather_for_ML





"""# Load the data
file_path = 'Avions-Retard-et-Meteo/1_Data_cleaning/plane_weather_for_ML.csv'
df = pd.read_csv(file_path)"""

# Select features and target
exclude_columns = ['DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 'WEATHER_DELAY', 'CANCELLED', 'HOURLYSeaLevelPressure', 'HOURLYAltimeterSetting']  # We can't use these variables in our model because they depend on whether or not the plane has been late or not, and we saw in the descriptive stats that the pressure at the station and at the sea level and the altimeter setting are really correlated
feature_columns = [col for col in df.columns if col not in exclude_columns]
target_column = 'DEP_DELAY' # The variable we want to predict

X = df[feature_columns]
y = df[target_column]


#### We have too much columns, which could cause overfitting. To avoid that, we have 2 options: PCA and Feature Importance
# The main difference between the PCA and Important Features is that the PCA creates linear
# combinations of our variables to explain the variance. The important features deals directly 
# with existing variables, which is easier to explain after that.
#### Option 1 : PCA
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Prepare data for the PCA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA
pca = PCA(n_components=0.95)  # Keep 95% of the variance
X_pca = pca.fit_transform(X_scaled)

print(f"Numbre of principle components : {X_pca.shape[1]}")


# Linear Regression
lin_reg = LinearRegression(fit_intercept=True)
y_pred_lin = cross_val_predict(lin_reg, X_pca, y, cv=5)  # 5-fold cross-validation

# Random Forest
rf_reg = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
y_pred_rf = cross_val_predict(rf_reg, X_pca, y, cv=5)

# XGBoost
xgb_reg = XGBRegressor(n_estimators=50, learning_rate=0.1, max_depth=5, random_state=42)
y_pred_xgb = cross_val_predict(xgb_reg, X_pca, y, cv=5)

# Metrics calculation
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

results = {
    'Model': ['Linear Regression', 'Random Forest', 'XGBoost'],
    'MAE': [
        mean_absolute_error(y, y_pred_lin),
        mean_absolute_error(y, y_pred_rf),
        mean_absolute_error(y, y_pred_xgb)
    ],
    'RMSE': [
        sqrt(mean_squared_error(y, y_pred_lin)),
        sqrt(mean_squared_error(y, y_pred_rf)),
        sqrt(mean_squared_error(y, y_pred_xgb))
    ],
    'R^2': [
        r2_score(y, y_pred_lin),
        r2_score(y, y_pred_rf),
        r2_score(y, y_pred_xgb)
    ]
}

results_df_PCA = pd.DataFrame(results)


# Option 2 : Feature Importance (we get the feature importance by a random forest model)
rf_reg = RandomForestRegressor(n_estimators=100, random_state=42)
rf_reg.fit(X, y)

# We get the most important features
importances = rf_reg.feature_importances_
feature_importance_df = pd.DataFrame({
    'Feature': feature_columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

# Then we select the most important features (example here the 8 most)
top_features = feature_importance_df.head(8)['Feature']
X_selected = X[top_features]


# This section is optionnal and only allows us to visualize the most important features
output_dir = 'Avions-Retard-et-Meteo/3_Machine_Learning/pictures'
os.makedirs(output_dir, exist_ok=True)
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'].head(8), feature_importance_df['Importance'].head(8))
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 10 Feature Importances")
plt.gca().invert_yaxis()  # Most important at the top
output_path = os.path.join(output_dir, "feature_importances.png") # Save the image
plt.savefig(output_path, dpi=300, bbox_inches='tight')  # Haute qualité et marges ajustées
##################


# Linear Regression
lin_reg = LinearRegression()
y_pred_lin = cross_val_predict(lin_reg, X_selected, y, cv=5)  # 5-fold cross-validation

# Random Forest
rf_reg = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
y_pred_rf = cross_val_predict(rf_reg, X_selected, y, cv=5)

# XGBoost
xgb_reg = XGBRegressor(n_estimators=50, learning_rate=0.1, max_depth=5, random_state=42)
y_pred_xgb = cross_val_predict(xgb_reg, X_selected, y, cv=5)

# Metrics calculation
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

results = {
    'Model': ['Linear Regression', 'Random Forest', 'XGBoost'],
    'MAE': [
        mean_absolute_error(y, y_pred_lin),
        mean_absolute_error(y, y_pred_rf),
        mean_absolute_error(y, y_pred_xgb)
    ],
    'RMSE': [
        sqrt(mean_squared_error(y, y_pred_lin)),
        sqrt(mean_squared_error(y, y_pred_rf)),
        sqrt(mean_squared_error(y, y_pred_xgb))
    ],
    'R^2': [
        r2_score(y, y_pred_lin),
        r2_score(y, y_pred_rf),
        r2_score(y, y_pred_xgb)
    ]
}


print("\nComparison of Model Performance (PCA):")
print(results_df_PCA)

results_df_FI = pd.DataFrame(results)
print("\nComparison of Model Performance (Feature Importance):")
print(results_df_FI)

"""
Linear Regression performs better with Feature Importance (MAE: 26.28 vs 34.90, RMSE: 74.72 vs 81.80, R^2: -0.011 vs -0.212)
Random Forest improves slightly with Feature Importance (MAE: 31.65 vs 52.45, RMSE: 88.32 vs 106.15, R^2: -0.413 vs -1.041)
XGBoost shows better results with Feature Importance but still underperforms (MAE: 32.88 vs 91.04, RMSE: 92.90 vs 211.86, R^2: -0.563 vs -7.131)
Feature Importance provides more relevant features for all models compared to PCA.


Using Feature Importance, model performance remains limited, with all models showing weak predictive power.
Linear Regression:
With Feature Importance, Linear Regression achieves a MAE of 26.28 and an RMSE of 74.72, both better than the PCA approach (MAE: 34.90, RMSE: 81.80). However, the R² remains slightly negative (-0.011), indicating that the model explains almost none of the variance in the data. Despite this, it still provides the most coherent predictions among all tested models.

Random Forest:
Random Forest improves with Feature Importance (MAE: 31.65, RMSE: 88.32) compared to PCA (MAE: 52.45, RMSE: 106.15). However, its R² score of -0.413 suggests poor generalization. While slightly better than PCA, Random Forest predictions are less consistent compared to Linear Regression.

XGBoost:
XGBoost shows the highest error with Feature Importance (MAE: 32.88, RMSE: 92.90) and the worst R² score (-0.563). While marginally better than the PCA-based approach (MAE: 91.04, RMSE: 211.86), its performance remains weak overall.
"""

# Overall, while Feature Importance improves focus on relevant features, the results suggest that the models lack strong predictive and explanatory power.


# This was predictable, because there are really few delays due to weather,

"""# The feature importance plot provides insights into the factors contributing to departure delays.
# HOURLYWindSpeed stands out as the most important feature, aligning with expectations since wind speed directly impacts flight schedules.
# Other weather-related variables like HOURLYRelativeHumidity, HOURLYStationPressure also have notable contributions.
# Interestingly, DAILYAverageStationPressure and HOURLYWETBULBTEMPF indicate that both daily and hourly weather metrics are relevant.
# Even though our predictive power is limited, the feature importance highlights key weather variables, offering valuable insights into the relationship between weather conditions and delays.

# The feature importance highlights key weather variables like wind speed and humidity, and the
# minimal delays caused by weather reflect the technological advancements and robustness of modern 
# aircraft in handling adverse conditions.
"""
"""
Key Observations:
Feature Importance provides better results across all models compared to PCA by focusing on relevant features, reducing noise, and ensuring better interpretability.
Linear Regression, while lacking strong explanatory power (as shown by the near-zero R²), offers the lowest MAE and RMSE, making it the best choice among the tested models for this dataset.
We are aware of the limited predictive power of our models due to the weak R² values. However, Linear Regression still generates the most coherent and realistic predictions, particularly when Feature Importance is used.
Experimentation Process and Rationale:
Initial Setup:
We initially included all available variables in our models, leading to overfitting and unrealistic predictions, such as planes always being very early or significantly delayed.

Feature Reduction:
Through successive adjustments and analysis, we reduced the features to the 8 most relevant variables based on Feature Importance.

Pressure Variables:
Initially, we included both HOURLYStationPressure and HOURLYSeaLevelPressure, which were highly correlated. This caused the model to predict unrealistic results, with planes often being far ahead of schedule. Removing one of the pressure variables improved prediction consistency.

Final Choice:
Linear Regression with Feature Importance, using 8 carefully selected features, achieved the best balance between low errors (MAE and RMSE) and realistic predictions.

Conclusion:
Although the predictive power of our models remains weak due to the low R² values (indicating that the models explain little variance in departure delays), the Linear Regression model with Feature Importance provides the most consistent and interpretable predictions. This is the result of iterative experimentation and careful adjustment of features, ensuring predictions align with realistic expectations while minimizing overfitting.
"""

# Entraîner le modèle sur les données sélectionnées
lin_reg.fit(X_selected, y)  # Ajouter cette ligne ici

# Sauvegarder le modèle entraîné
model_path = 'Avions-Retard-et-Meteo/3_Machine_Learning/linear_regression_model.pkl'
joblib.dump(lin_reg, model_path)


"""
# Afficher les coefficients
coefficients = lin_reg.coef_
features = X_selected.columns  # Les noms des colonnes sélectionnées

# Afficher les coefficients avec leurs noms
for feature, coef in zip(features, coefficients):
    print(f"{feature}: {coef}")
"""