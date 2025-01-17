# Flight Delay Prediction Project

### Authors: *Léo LEROY, Léo DONZIL, Lisa CHARDON--DENIZOT*

---

## Introduction

Flight delays disrupt travel plans, increase costs, and reduce overall efficiency in the aviation industry. This project aims to create a predictive model for flight delays based on weather data. The goal is to provide a practical tool for anticipating delays, leveraging machine learning models, and integrating real-time data through APIs.
Our code is available on [main.ipynb](https://github.com/Leooryx/Avions-Retard-et-Meteo/blob/main/main.ipynb)

---

## Problem Statement

Can flight delays be predicted accurately using weather data? What is the reliability of such a model, and how can it be integrated into a practical application?

---

## Models Used

We tested several machine learning techniques to identify the best-performing model for this task, combined with PCA or Feature Importance to reduce the number of variables:

1. **Linear Regression**:
   - Selected as the final model for its consistent predictions, simplicity, and interpretability.
   - Enhanced with feature importance for better relevance and reduced noise.
2. **Random Forest**:
   - Explored for its ability to capture non-linear relationships, but the predictions lacked consistency.
3. **XGBoost**:
   - Known for its high performance in many contexts but yielded lower predictive power in this case. 


The final model, Linear Regression with feature importance, provided the best balance between accuracy and interpretability.

---

## Data Sources

To train and deploy our models, we used two datasets and two APIs:

### Datasets:
1. **Plane Data**:
   - **[Bureau of Transportation Statistics](https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ&QO_fu146_anzr=b0-gvzr)**:
     Dataset containing detailed flight information, including delays, departure/arrival times, and airport details. We focused on 2017 data due to its availability and manageable size.
2. **Weather Data**:
   - **[IBM Weather Data](https://developer.ibm.com/exchanges/data/all/jfk-weather-data/)**:
     Historical weather data from JFK airport in 2017.

### APIs:
1. **[Aerodatabox API](https://aerodatabox.com/)**:
   - Provides real-time flight information, including schedules, aircraft models, and statuses.
   - Essential for linking flight metadata to weather conditions.
2. **[Open-Meteo API](https://open-meteo.com/)**:
   - Supplies historical and forecasted weather data such as temperature, wind speed, visibility, and humidity.
   - Free and versatile, allowing precise alignment of weather data with flight details.

---

## Application

The project includes a **Streamlit web application** for real-time flight delay predictions, accessible here: [Flight Delay Prediction](https://flight-delay-prediction-2024.streamlit.app/)

### Usage
- Users input their Aerodatabox API token.
- Users input a flight number and date.
- The app fetches live data from APIs and predicts potential delays based on weather conditions.
- The predicted delay is visually highlighted (red for delays, green for early arrivals).

The app is seamlessly integrated into the project via a **notebook**, allowing users to launch it directly with an accessible Streamlit link.

Please note that the Open-Meteo API **doesn't require** a token, while the Aerodatabox **does** require one. For safety reason, this token is not saved in our repo. You can put the token in the application directly.
---

## Reproducibility

Reproducibility is ensured through the execution of the notebook, which integrates all components of the project:
- The main **notebook** ([main.ipynb](https://github.com/Leooryx/Avions-Retard-et-Meteo/blob/main/main.ipynb)) contains the complete workflow and integrates all Python modules coded throughout the project.
- The **Streamlit app** is created in a separate folder due to its unique structure but can be launched directly from the notebook.
