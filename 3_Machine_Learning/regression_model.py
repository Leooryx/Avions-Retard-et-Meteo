#Import the packages and load the data
#pip install openpyxl
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_predict
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import StackingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from catboost import CatBoostRegressor
import numpy as np

# Load the data
file_path = 'Avions-Retard-et-Meteo/1_Data_cleaning/plane_weather_for_ML.csv'
df = pd.read_csv(file_path)

# Select features and target
exclude_columns = ['DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 'WEATHER_DELAY', 'CANCELLED'] # We can't use these variables in our model because they depend on whether or not the plane has been late or not
feature_columns = [col for col in df.columns if col not in exclude_columns]
target_column = 'DEP_DELAY' # The variable we want to predict

X = df[feature_columns]
y = df[target_column]

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Prepare data for the PCA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA
pca = PCA(n_components=0.8)  # Keep 80% of the variance
X_pca = pca.fit_transform(X_scaled)

print(f"Nombre de composantes principales retenues : {X_pca.shape[1]}")


# Modèle Linear Regression
lin_reg = LinearRegression()
y_pred_lin = cross_val_predict(lin_reg, X_pca, y, cv=5)  # 5-fold cross-validation

# Modèle Random Forest
rf_reg = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
y_pred_rf = cross_val_predict(rf_reg, X_pca, y, cv=5)

# Modèle XGBoost
xgb_reg = XGBRegressor(n_estimators=50, learning_rate=0.1, max_depth=5, random_state=42)
y_pred_xgb = cross_val_predict(xgb_reg, X_pca, y, cv=5)

# Calcul des métriques
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("\nLinear Regression:")
print(f"MAE: {mean_absolute_error(y, y_pred_lin):.2f}, RMSE: {mean_squared_error(y, y_pred_lin, squared=False):.2f}, R²: {r2_score(y, y_pred_lin):.2f}")

print("\nRandom Forest:")
print(f"MAE: {mean_absolute_error(y, y_pred_rf):.2f}, RMSE: {mean_squared_error(y, y_pred_rf, squared=False):.2f}, R²: {r2_score(y, y_pred_rf):.2f}")

print("\nXGBoost:")
print(f"MAE: {mean_absolute_error(y, y_pred_xgb):.2f}, RMSE: {mean_squared_error(y, y_pred_xgb, squared=False):.2f}, R²: {r2_score(y, y_pred_xgb):.2f}")

# Compare models
results = {
    'Model': ['Linear Regression', 'Random Forest', 'XGBoost'],
    'MAE': [mae_lin, mae_rf, mae_xgb],
    'RMSE': [rmse_lin, rmse_rf, rmse_xgb],
    'R^2': [r2_lin, r2_rf, r2_xgb]
}

results_df = pd.DataFrame(results)
print("\nComparison of Model Performance:")
print(results_df)

# Visualize feature importance for Random Forest
print("\nFeature Importances from Random Forest:")
importances = rf_reg.feature_importances_
sorted_indices = importances.argsort()[::-1]

plt.figure(figsize=(10, 6))
plt.bar(range(len(importances)), importances[sorted_indices], align='center')
plt.xticks(range(len(importances)), [feature_columns[i] for i in sorted_indices], rotation=90)
plt.title("Feature Importances - Random Forest")
plt.show()


