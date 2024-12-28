# Motivation
# Even though there seems to be very few delays due to weather, as shown by the data exploration,
# It could be possible that the variable weather delay don't include all of them, and maybe there
# is a way to predict them

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

# Select features and target
exclude_columns = ['DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 'WEATHER_DELAY', 'CANCELLED'] # We can't use these variables in our model because they depend on whether or not the plane has been late or not
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
lin_reg = LinearRegression()
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
        mean_squared_error(y, y_pred_lin, squared=False),
        mean_squared_error(y, y_pred_rf, squared=False),
        mean_squared_error(y, y_pred_xgb, squared=False)
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
        mean_squared_error(y, y_pred_lin, squared=False),
        mean_squared_error(y, y_pred_rf, squared=False),
        mean_squared_error(y, y_pred_xgb, squared=False)
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

# Linear Regression performs better with Feature Importance (MAE: 26.72 vs 34.95, RMSE: 74.06 vs 81.80, R^2: 0.006 vs -0.212)
# Random Forest improves slightly with Feature Importance (MAE: 30.49 vs 40.73, RMSE: 85.26 vs 90.50, R^2: -0.317 vs -0.484)
# XGBoost shows better results with Feature Importance but still underperforms (MAE: 33.35 vs 55.20, RMSE: 94.35 vs 136.75, R^2: -0.613 vs -2.387)
# Feature Importance provides more relevant features for all models compared to PCA


# Using Feature Importance, model performance remains limited, with all models showing weak predictive power.
# Linear Regression has a modest MAE (26.72) and RMSE (74.06) but offers almost no explanatory strength (R^2: 0.006).
# Random Forest improves slightly (MAE: 30.49, RMSE: 85.26), but its R^2 (-0.317) indicates poor generalization.
# XGBoost, despite reducing MAE (33.35), still struggles with high RMSE (94.35) and very low R^2 (-0.613).
# Overall, while Feature Importance improves focus on relevant features, the results suggest that the models lack strong predictive and explanatory power.


# This was predictable, because there are really few delays due to weather,

# The feature importance plot provides insights into the factors contributing to departure delays.
# HOURLYWindSpeed stands out as the most important feature, aligning with expectations since wind speed directly impacts flight schedules.
# Other weather-related variables like HOURLYRelativeHumidity, HOURLYStationPressure, and HOURLYSeaLevelPressure also have notable contributions.
# Interestingly, DAILYAverageStationPressure and HOURLYWETBULBTEMPF indicate that both daily and hourly weather metrics are relevant.
# Even though our predictive power is limited, the feature importance highlights key weather variables, offering valuable insights into the relationship between weather conditions and delays.


# The feature importance highlights key weather variables like wind speed and humidity, and the
# minimal delays caused by weather reflect the technological advancements and robustness of modern 
# aircraft in handling adverse conditions.