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

# Split the data into train and test sets 90/10
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

#########
from sklearn.model_selection import RandomizedSearchCV

# Hyperparameter grid for XGBoost
param_grid = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'subsample': [0.7, 0.8, 1.0],
    'colsample_bytree': [0.7, 0.8, 1.0]
}

# Randomized search
xgb_model = xgb.XGBRegressor(random_state=42)
random_search = RandomizedSearchCV(
    xgb_model, param_distributions=param_grid,
    n_iter=10, scoring='neg_mean_squared_error',
    cv=3, verbose=2, random_state=42, n_jobs=-1
)
random_search.fit(X_train, y_train)

# Best model
best_xgb = random_search.best_estimator_

# Evaluate the best model
y_pred_best_xgb = best_xgb.predict(X_test)
mae_best_xgb = mean_absolute_error(y_test, y_pred_best_xgb)
rmse_best_xgb = mean_squared_error(y_test, y_pred_best_xgb, squared=False)
r2_best_xgb = r2_score(y_test, y_pred_best_xgb)

print("\nOptimized XGBoost Results:")
print(f"MAE: {mae_best_xgb:.2f}, RMSE: {rmse_best_xgb:.2f}, R^2: {r2_best_xgb:.2f}")



########################
#pip install lightgbm
import lightgbm as lgb

lgb_model = lgb.LGBMRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
lgb_model.fit(X_train, y_train)

y_pred_lgb = lgb_model.predict(X_test)
mae_lgb = mean_absolute_error(y_test, y_pred_lgb)
rmse_lgb = mean_squared_error(y_test, y_pred_lgb, squared=False)
r2_lgb = r2_score(y_test, y_pred_lgb)

print("\nLightGBM Results:")
print(f"MAE: {mae_lgb:.2f}, RMSE: {rmse_lgb:.2f}, R^2: {r2_lgb:.2f}")



########################################
########################################
# Attempt to remove extreme delay values
# Cap target at 99th percentile
upper_limit = y.quantile(0.99)
y_capped = y.clip(upper=upper_limit)

# Split the data into train and test sets 90/10
X_train, X_test, y_train, y_test = train_test_split(X, y_capped, test_size=0.1, random_state=42)

####Cat Boost#####
#pip install catboost
##conda install -c conda-forge catboost

from catboost import CatBoostRegressor

cat_model = CatBoostRegressor(iterations=500, learning_rate=0.1, depth=6, random_seed=42, verbose=0)
cat_model.fit(X_train, y_train)

y_pred_cat = cat_model.predict(X_test)
mae_cat = mean_absolute_error(y_test, y_pred_cat)
rmse_cat = mean_squared_error(y_test, y_pred_cat, squared=False)
r2_cat = r2_score(y_test, y_pred_cat)

print("\nCatBoost Results:")
print(f"MAE: {mae_cat:.2f}, RMSE: {rmse_cat:.2f}, R^2: {r2_cat:.2f}")

#######LightGBM########
import lightgbm as lgb

lgb_model = lgb.LGBMRegressor(n_estimators=500, learning_rate=0.1, max_depth=6, random_state=42)
lgb_model.fit(X_train, y_train)

y_pred_lgb = lgb_model.predict(X_test)
mae_lgb = mean_absolute_error(y_test, y_pred_lgb)
rmse_lgb = mean_squared_error(y_test, y_pred_lgb, squared=False)
r2_lgb = r2_score(y_test, y_pred_lgb)

print("\nLightGBM Results:")
print(f"MAE: {mae_lgb:.2f}, RMSE: {rmse_lgb:.2f}, R^2: {r2_lgb:.2f}")

######XGBoost#####
from xgboost import XGBRegressor

xgb_model = XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=6, subsample=0.8, colsample_bytree=0.8, random_state=42)
xgb_model.fit(X_train, y_train)

y_pred_xgb = xgb_model.predict(X_test)
mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
rmse_xgb = mean_squared_error(y_test, y_pred_xgb, squared=False)
r2_xgb = r2_score(y_test, y_pred_xgb)

print("\nXGBoost Results:")
print(f"MAE: {mae_xgb:.2f}, RMSE: {rmse_xgb:.2f}, R^2: {r2_xgb:.2f}")



#####Other parameters cat boost####
# from catboost import CatBoostRegressor

cat_model = CatBoostRegressor(iterations=500, learning_rate=0.1, depth=6, random_seed=42, verbose=0)
cat_model.fit(X_train, y_train)

y_pred_cat = cat_model.predict(X_test)
mae_cat = mean_absolute_error(y_test, y_pred_cat)
rmse_cat = mean_squared_error(y_test, y_pred_cat, squared=False)
r2_cat = r2_score(y_test, y_pred_cat)

print("\nCatBoost Results:")
print(f"MAE: {mae_cat:.2f}, RMSE: {rmse_cat:.2f}, R^2: {r2_cat:.2f}")


#####Other parameters cat boost####
# from catboost import CatBoostRegressor

cat_model = CatBoostRegressor(iterations=1000, learning_rate=0.03, depth=12, random_seed=42, verbose=0)
cat_model.fit(X_train, y_train)

y_pred_cat = cat_model.predict(X_test)
mae_cat = mean_absolute_error(y_test, y_pred_cat)
rmse_cat = mean_squared_error(y_test, y_pred_cat, squared=False)
r2_cat = r2_score(y_test, y_pred_cat)

print("\nCatBoost Results:")
print(f"MAE: {mae_cat:.2f}, RMSE: {rmse_cat:.2f}, R^2: {r2_cat:.2f}")



####Cross validation (before we just tested on 1 bloc of data)####
from sklearn.model_selection import cross_val_score

# CatBoost avec validation croisée
catboost_model = CatBoostRegressor(
    iterations=1000,
    depth=12,
    learning_rate=0.03,
    random_state=42
)

# Validation croisée (MAE)
cv_scores = cross_val_score(
    catboost_model, X_train, y_train, scoring='neg_mean_absolute_error', cv=5
)

# Résultats
mean_mae_cv = -cv_scores.mean()  # Scores négatifs, donc on prend l'opposé
std_mae_cv = cv_scores.std()

print(f"Cross-validated MAE: {mean_mae_cv:.2f} ± {std_mae_cv:.2f}")




###################Feature importance
# Feature Importance avec CatBoost
catboost_model.fit(X_train, y_train, verbose=0)

importances = catboost_model.feature_importances_
sorted_idx = importances.argsort()

# Visualiser les importances
plt.figure(figsize=(10, 6))
plt.barh(range(len(importances)), importances[sorted_idx])
plt.yticks(range(len(importances)), [X_train.columns[i] for i in sorted_idx])
plt.title("Feature Importance - CatBoost")
plt.xlabel("Importance Score")
plt.ylabel("Features")
plt.savefig('/home/onyxia/work/feature_importance_catboost.png', dpi=300, bbox_inches='tight')
plt.close()  # Fermer le graphique pour éviter un affichage inutile

# Afficher les importances des variables
feature_importances = catboost_model.get_feature_importance()
importance_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

print(importance_df.head(10))


####We have the importance of each feature. Thus, we select the 10 better to see if there any improvements in our model
#This is what we do in the regression_models_imp_feature.py doc
#--> bad model, we go back to this one