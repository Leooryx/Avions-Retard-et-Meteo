#In this program, we test out hybrid models and then an optimization of catboosts parameters
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import StackingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from catboost import CatBoostRegressor
import numpy as np
import matplotlib.pyplot as plt

# Load the data
file_path = '/home/onyxia/work/Avions-Retard-et-Meteo/1_Data_cleaning/plane_weather_for_ML.csv'
try:
    df = pd.read_csv(file_path)
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# Select features and target
exclude_columns = ['DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 'WEATHER_DELAY', 'CANCELLED']
feature_columns = [col for col in df.columns if col not in exclude_columns]
target_column = 'DEP_DELAY'

X = df[feature_columns]
y = df[target_column]


# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --------------------------- Step 3: Hybrid Model (Stacking) ---------------------------
print("\nFitting Stacking Model...")

# Base models
catboost = CatBoostRegressor(iterations=1000, depth=6, learning_rate=0.1, verbose=0, random_state=42)
lin_reg = LinearRegression()

# Stacking Regressor
estimators = [
    ('catboost', catboost),
    ('linear', lin_reg)
]
stacking_reg = StackingRegressor(estimators=estimators, final_estimator=LinearRegression())
stacking_reg.fit(X_train, y_train)

# Evaluate stacking
y_pred_stack = stacking_reg.predict(X_test)
mae_stack = mean_absolute_error(y_test, y_pred_stack)
rmse_stack = mean_squared_error(y_test, y_pred_stack, squared=False)
r2_stack = r2_score(y_test, y_pred_stack)

print(f"\nStacking Model Results:\nMAE: {mae_stack:.2f}, RMSE: {rmse_stack:.2f}, R^2: {r2_stack:.2f}")

# --------------------------- Step 4: Hyperparameter Tuning for CatBoost ---------------------------
print("\nOptimizing CatBoost Hyperparameters...")

# Define parameter grid
param_dist = {
    'iterations': [500, 1000, 1500],
    'depth': [4, 6, 8, 10],
    'learning_rate': np.linspace(0.01, 0.3, 10),
    'l2_leaf_reg': [1, 3, 5, 7, 9],
}

# Initialize CatBoostRegressor
catboost = CatBoostRegressor(verbose=0, random_state=42)

# Randomized Search
random_search = RandomizedSearchCV(estimator=catboost, param_distributions=param_dist, n_iter=20, cv=3, scoring='neg_mean_absolute_error', random_state=42)
random_search.fit(X_train, y_train)

# Best estimator
best_catboost = random_search.best_estimator_
print("Best Parameters for CatBoost:", random_search.best_params_)

# Evaluate tuned CatBoost
y_pred_best_cat = best_catboost.predict(X_test)
mae_best_cat = mean_absolute_error(y_test, y_pred_best_cat)
rmse_best_cat = mean_squared_error(y_test, y_pred_best_cat, squared=False)
r2_best_cat = r2_score(y_test, y_pred_best_cat)

print(f"\nOptimized CatBoost Results:\nMAE: {mae_best_cat:.2f}, RMSE: {rmse_best_cat:.2f}, R^2: {r2_best_cat:.2f}")

# --------------------------- Compare Results ---------------------------
results = {
    'Model': ['Stacking', 'Optimized CatBoost'],
    'MAE': [mae_stack, mae_best_cat],
    'RMSE': [rmse_stack, rmse_best_cat],
    'R^2': [r2_stack, r2_best_cat]
}

results_df = pd.DataFrame(results)
print("\nModel Comparison:\n", results_df)

# Save results to CSV
results_df.to_csv('model_comparison_results.csv', index=False)
print("\nResults saved to 'model_comparison_results.csv'")
