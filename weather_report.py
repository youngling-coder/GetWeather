# Import necessary libraries and modules
from urllib import request, parse, error
from aiogram.utils.markdown import hbold
import json, os
import flag


class WeatherReport:
    def __init__(self, city, unit_system):

        # Initializing required variables
        self.__weather = {}
        city = parse.quote_plus(city)
        self.city = city
        self.unit_system = unit_system
        
        self.__WEATHER_TOKEN = "70bcd9fd2f6471b4018a4839d84f0b11"
        self.__WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather"


    def URL(self) -> str:

        # Format API url for specific unit system & city|region
        result_url = self.__WEATHER_URL + f"?q={self.city}"
        result_url = result_url + f"&units={self.unit_system}"
        result_url = result_url + f"&appid={self.__WEATHER_TOKEN}"

        # Return final url
        return result_url

    def getWeatherData(self, query_url) -> None | str:
        try:

            # Try to obtain json info
            response = request.urlopen(query_url)
        except error.HTTPError as http_error:

            # If any error occurred then return error message
            match http_error.code:
                case 401:
                    return "❌ API Key Error!"
                case 404:
                    return "❌ Can't find weather data for this city."
                case _:
                    return "❌ Unknown search error!"

        # Reading json data
        data = response.read()

        try:

            # Try to JSON data to dictionary
            self.__weather = json.loads(data)
        except json.JSONDecodeError:

            # If error occured then return error message
            return "❌ Couldn't read the server response!"

    def getWindDirection(self) -> str:

        # Obtain wind degree
        wind_deg = self.__weather["wind"]["deg"]

        # Simple if-elif-elif-else block to get wind direction
        if 315 < wind_deg or wind_deg <= 45:
            return "🧭 North"
        elif 45 < wind_deg <= 135:
            return "🧭 East"
        elif 135 < wind_deg <= 225:
            return "🧭 South"
        else:
            return "🧭 West"

    def getBasicForecast(self) -> str:

        # Obtain brief weather description
        weather_main = self.__weather["weather"][0]["main"]

        weather_main = weather_main.lower()

        # Generate beautified output
        match weather_main:
            case "thunderstorm":
                weather_main = f"it's a {weather_main} outside ⛈️"
            case "drizzle":
                weather_main = f"just a light {weather_main} 🌧️"
            case "rain":
                weather_main = f"it's {weather_main}ing 🌧️"
            case "snow":
                weather_main = f"let it {weather_main} ❄️"
            case "mist" | "smoke" | "haze" | "dust" | "sand" | "ash":
                weather_main = f"it's too {weather_main}y 🌫️"
            case "fog":
                weather_main = f"it's too {weather_main}gy 🌫️"
            case "squall":
                weather_main = f"it's a {weather_main}! 🌪"
            case "tornado":
                weather_main = f"woah, a {weather_main}! 🌪"
            case "clouds":
                weather_main = f"such a cloudy weather ☁️"
            case "clear":
                weather_main = f"it's {weather_main} outside! Time to go for a walk! ☀️"
            case _:
                weather_main = f"hmm.. Sorry but I don't know what's going on outside ☹."

        # Return beautified output
        return weather_main

    def beautify(self) -> str:

        # Obtain wind direction
        wind_direction = self.getWindDirection()

        # Obtain country flag emoji
        country_code = flag.flag(self.__weather["sys"]["country"])

        # Obtain units to use in output
        wind_speed_unit = "m/s" if self.unit_system == "metric" else "mi/h"
        temperature_unit = "°C" if self.unit_system == "metric" else "°F"

        # Beautify resulting weather info
        result = f"""
{hbold('🏙️ City:')} {self.__weather["name"]}, {self.__weather["sys"]["country"]} {country_code}
{hbold('🌡 Current:')} {self.__weather["main"]["temp"]} {temperature_unit}
{hbold('🌡️ Feels like:')} {self.__weather["main"]["feels_like"]} {temperature_unit}
{hbold('💨 Wind:')} {wind_direction}, {self.__weather["wind"]["speed"]} {wind_speed_unit}
\nIn brief, {self.getBasicForecast()}"""

        # Return beautified output
        return result
