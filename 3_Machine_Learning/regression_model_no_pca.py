#pip install openpyxl
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import matplotlib.pyplot as plt

# Load the data
file_path = '/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/plane_weather_for_ML.csv'
df = pd.read_csv(file_path)

# Inspect the data - REMOVE THIS PART WHEN FINISHED
print("Data preview:")
print(df.head())
print("\nData information:")
print(df.info())

# Select relevant features and target column
# We make sure the model doesn't use variables that are calculated after the flight because we won't have them as an input
exclude_columns = ['DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 'WEATHER_DELAY', 'CANCELLED']
feature_columns = [col for col in df.columns if col not in exclude_columns]
target_column = 'DEP_DELAY'  # Column that we want to predict

X = df[feature_columns]
y = df[target_column]

# Split the data into train and test sets 80/20
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Verify split
print(f"\nTraining set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")

# Baseline model: Linear Regression
print("\nFitting Linear Regression model...")
lin_reg = LinearRegression() 
lin_reg.fit(X_train, y_train)

# Make predictions
y_pred_lin = lin_reg.predict(X_test)

# Evaluate performance
mae_lin = mean_absolute_error(y_test, y_pred_lin)
rmse_lin = mean_squared_error(y_test, y_pred_lin, squared=False)
r2_lin = r2_score(y_test, y_pred_lin)
print(f"\nLinear Regression Results:\nMAE: {mae_lin:.2f}, RMSE: {rmse_lin:.2f}, R^2: {r2_lin:.2f}")

# Intermediate model: Random Forest Regressor
print("\nFitting Random Forest model...")
rf_reg = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=5)
rf_reg.fit(X_train, y_train)

# Make predictions
y_pred_rf = rf_reg.predict(X_test)

# Evaluate performance
mae_rf = mean_absolute_error(y_test, y_pred_rf)
rmse_rf = mean_squared_error(y_test, y_pred_rf, squared=False)
r2_rf = r2_score(y_test, y_pred_rf)
print(f"\nRandom Forest Results:\nMAE: {mae_rf:.2f}, RMSE: {rmse_rf:.2f}, R^2: {r2_rf:.2f}")

# Advanced model: XGBoost Regressor
print("\nFitting XGBoost model...")
xgb_reg = xgb.XGBRegressor(n_estimators=50, learning_rate=0.1, random_state=42, max_depth=5)
xgb_reg.fit(X_train, y_train)

# Make predictions
y_pred_xgb = xgb_reg.predict(X_test)

# Evaluate performance
mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
rmse_xgb = mean_squared_error(y_test, y_pred_xgb, squared=False)
r2_xgb = r2_score(y_test, y_pred_xgb)
print(f"\nXGBoost Results:\nMAE: {mae_xgb:.2f}, RMSE: {rmse_xgb:.2f}, R^2: {r2_xgb:.2f}")

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


