"""
Variables that we want to use     Description in the glossary                                                                               Hourly Equivalent in the OpenWeather API
HOURLYWindSpeed                   Speed of the wind at the time of observation given in miles per hour (mph).                               Hourly Wind Speed (10 m)
HOURLYRelativeHumidity            This is the relative humidity given to the nearest whole percentage.                                      Hourly Relative Humidity (2 m)
HOURLYStationPressure             Atmospheric pressure observed at the station  (in inches of Mercury)                                      Hourly Surface Pressure
XHOURLYSeaLevelPressure            Sea level pressure given in inches of Mercury (in Hg).                                                    Hourly Sealevel Pressure
DAILYAverageStationPressure       Daily average station pressure (in inches of mercury, to hundredths)                                      Not available, we will take the mean of Hourly Surface Pressure
HOURLYWETBULBTEMPF                This is the wet-bulb temperature. It is given here in whole degrees Fahrenheit                            Calculated with Stull Equation and Temp and DewPoint
XHOURLYAltimeterSetting            Atm pressure reduced to sea level using temp profile of the “standard” atmosphere (inches of Mercury)     Calculated with altitude (3m) and Station Pressure
HOURLYDRYBULBTEMPC                This is the dry-bulb temperature and is commonly used as the standard air temperature reported (in C°)    Temperature (2 m)
HOURLYDewPointTempF               This is the dew point temperature. It is given here in whole degrees Fahrenheit.                          Dewpoint (2 m)
HOURLYVISIBILITY                  The horizontal distance an object can be seen and identified given in whole miles.                        Visibility

Units of the weather API : Celsius, mph, mm
"""

import requests
import pandas as pd
from math import atan, sqrt


def fetch_weather_data(api_url):
    # Fetch data from the weather API
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        hourly_data = data.get('hourly', {})

        # Create a DataFrame with the hourly data
        df = pd.DataFrame(hourly_data)

        # Rename columns to match the variable names in the feature importance graph
        rename_mapping = {
            'temperature_2m': 'HOURLYDRYBULBTEMPF',
            'relative_humidity_2m': 'HOURLYRelativeHumidity',
            'dew_point_2m': 'HOURLYDewPointTempF',
            'pressure_msl': 'HOURLYSeaLevelPressure',
            'surface_pressure': 'HOURLYStationPressure',
            'wind_speed_10m': 'HOURLYWindSpeed',
            'visibility': 'HOURLYVISIBILITY'
        }

        df.rename(columns=rename_mapping, inplace=True)

        # Convert temperature from Celsius to Fahrenheit for relevant variables
        if 'HOURLYDRYBULBTEMPF' in df:
            df['HOURLYDRYBULBTEMPF'] = df['HOURLYDRYBULBTEMPF'] * 9 / 5 + 32

        if 'HOURLYDewPointTempF' in df:
            df['HOURLYDewPointTempF'] = df['HOURLYDewPointTempF'] * 9 / 5 + 32

        # Convert visibility from meters to miles
        if 'HOURLYVISIBILITY' in df:
            df['HOURLYVISIBILITY'] = df['HOURLYVISIBILITY'] * 0.000621371

        # Convert sea level pressure from hPa to inHg
        if 'HOURLYSeaLevelPressure' in df:
            df['HOURLYSeaLevelPressure'] = df['HOURLYSeaLevelPressure'] * 0.02953

        # Convert station pressure from hPa to inHg
        if 'HOURLYStationPressure' in df:
            df['HOURLYStationPressure'] = df['HOURLYStationPressure'] * 0.02953

        # Calculate additional variables
        if 'HOURLYStationPressure' in df:
            df['DAILYAverageStationPressure'] = df['HOURLYStationPressure'].mean()

        if 'HOURLYDRYBULBTEMPF' in df and 'HOURLYDewPointTempF' in df:
            df['HOURLYWETBULBTEMPF'] = df.apply(
                lambda row: row['HOURLYDRYBULBTEMPF'] * atan(0.151977 * sqrt(row['HOURLYRelativeHumidity'] + 8.313659))
                           + atan(row['HOURLYDRYBULBTEMPF'] + row['HOURLYDewPointTempF'])
                           - atan(row['HOURLYDewPointTempF'] - 1.676331)
                           + 0.00391838 * pow(row['HOURLYRelativeHumidity'], 1.5) * atan(0.023101 * row['HOURLYRelativeHumidity'])
                           - 4.686035,
                axis=1
            )

        if 'HOURLYStationPressure' in df:
            altitude_m = 3  # Altitude of the station in meters
            df['HOURLYAltimeterSetting'] = df['HOURLYStationPressure'] * pow(1 - (altitude_m / 44330.0), 5.255)

        # Keep only the variables shown in the feature importance graph
        selected_columns = [
            'HOURLYWindSpeed',
            'HOURLYRelativeHumidity',
            'HOURLYStationPressure',
            'HOURLYWETBULBTEMPF',
            'HOURLYDRYBULBTEMPF',
            'DAILYAverageStationPressure',
            'HOURLYDewPointTempF',
            'HOURLYVISIBILITY'
        ]
        df = df[selected_columns]

        return df
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
