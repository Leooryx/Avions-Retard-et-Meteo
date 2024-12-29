#Modules to download to enable the usage of pre-processing.py, Exploraotory_stat.py, ML.py

import pandas as pd
import matplotlib.pyplot as plt
import io
import os
import numpy as np
from datetime import timedelta
import s3fs
import seaborn as sns
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
from math import sqrt
import joblib

#See notebook to download these two modules or copy-paste into the bash terminal
# pip install openpyxl
# pip install scikit-learn==1.5.2