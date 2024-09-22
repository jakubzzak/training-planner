import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# from data.open_meteo_weather_codes import weather_codes


class OpenMeteoService():
    url = "https://api.open-meteo.com/v1/forecast"
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    params = {
        "hourly": ["temperature_2m", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "weather_code", "wind_speed_10m", "wind_direction_10m"],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_hours", "precipitation_probability_max", "wind_speed_10m_max", "wind_direction_10m_dominant"],
        "timezone": "Europe/Berlin"
    }

    def __init__(self) -> None:
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        self.openmeteo = openmeteo_requests.Client(session = retry_session)

        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)


    def get_weather_data(self, latitude, longitude):
        params = self.params.copy()
        params["latitude"] = latitude
        params["longitude"] = longitude
        # "latitude": 48.5,
        # "longitude": 17.5,
        responses = self.openmeteo.weather_api(
            self.url,
            params=params
        )

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
        hourly_rain = hourly.Variables(3).ValuesAsNumpy()
        hourly_showers = hourly.Variables(4).ValuesAsNumpy()
        hourly_snowfall = hourly.Variables(5).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(6).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(7).ValuesAsNumpy()
        hourly_wind_direction_10m = hourly.Variables(8).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        )}
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["precipitation_probability"] = hourly_precipitation_probability
        hourly_data["precipitation"] = hourly_precipitation
        hourly_data["rain"] = hourly_rain
        hourly_data["showers"] = hourly_showers
        hourly_data["snowfall"] = hourly_snowfall
        hourly_data["weather_code"] = hourly_weather_code
        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
        hourly_data["wind_direction_10m"] = hourly_wind_direction_10m

        hourly_dataframe = pd.DataFrame(data = hourly_data)
        print(hourly_dataframe)

        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_weather_code = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
        daily_sunrise = daily.Variables(3).ValuesAsNumpy()
        daily_sunset = daily.Variables(4).ValuesAsNumpy()
        daily_daylight_duration = daily.Variables(5).ValuesAsNumpy()
        daily_sunshine_duration = daily.Variables(6).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(7).ValuesAsNumpy()
        daily_rain_sum = daily.Variables(8).ValuesAsNumpy()
        daily_showers_sum = daily.Variables(9).ValuesAsNumpy()
        daily_snowfall_sum = daily.Variables(10).ValuesAsNumpy()
        daily_precipitation_hours = daily.Variables(11).ValuesAsNumpy()
        daily_precipitation_probability_max = daily.Variables(12).ValuesAsNumpy()
        daily_wind_speed_10m_max = daily.Variables(13).ValuesAsNumpy()
        daily_wind_direction_10m_dominant = daily.Variables(14).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}
        daily_data["weather_code"] = daily_weather_code
        daily_data["temperature_2m_max"] = daily_temperature_2m_max
        daily_data["temperature_2m_min"] = daily_temperature_2m_min
        daily_data["sunrise"] = daily_sunrise
        daily_data["sunset"] = daily_sunset
        daily_data["daylight_duration"] = daily_daylight_duration
        daily_data["sunshine_duration"] = daily_sunshine_duration
        daily_data["precipitation_sum"] = daily_precipitation_sum
        daily_data["rain_sum"] = daily_rain_sum
        daily_data["showers_sum"] = daily_showers_sum
        daily_data["snowfall_sum"] = daily_snowfall_sum
        daily_data["precipitation_hours"] = daily_precipitation_hours
        daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
        daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
        daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

        daily_dataframe = pd.DataFrame(data = daily_data)
        print(daily_dataframe)

if __name__ == "__main__":
    smolenice_coordinates = [48.506211053607856, 17.43061034187817]
    service = OpenMeteoService()
    service.get_weather_data(smolenice_coordinates[0], smolenice_coordinates[1])
