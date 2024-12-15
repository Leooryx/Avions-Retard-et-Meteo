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


from catboost import CatBoostRegressor

# Top 10 features based on importance
top_10_features = [
    'HOURLYWindSpeed', 'HOURLYRelativeHumidity', 'DAILYDeptFromNormalAverageTemp',
    'DAILYAverageWindSpeed', 'HOURLYStationPressure', 'HOURLYSeaLevelPressure',
    'HOURLYDRYBULBTEMPF', 'HOURLYAltimeterSetting', 'HOURLYDewPointTempF', 'HOURLYVISIBILITY'
]

exclude_columns = ['DEP_DELAY', 'ARR_DELAY', 'CARRIER_DELAY', 'WEATHER_DELAY', 'CANCELLED']
feature_columns = [col for col in df.columns if col not in exclude_columns]

X = df[feature_columns]

# Prepare data
X_top10 = X[top_10_features]
y = df['DEP_DELAY']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_top10, y, test_size=0.2, random_state=42)

# Train CatBoost model
catboost_model = CatBoostRegressor(iterations=1000, learning_rate=0.05, depth=6, verbose=100)
catboost_model.fit(X_train, y_train)

# Predictions
y_pred = catboost_model.predict(X_test)

# Evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)

print(f"\nCatBoost with Top 10 Features Results:")
print(f"MAE: {mae:.2f}, RMSE: {rmse:.2f}, R^2: {r2:.2f}")

#Worse