from urllib import request, parse, error
import json


class Location:
    def __init__(self, lat=0, lon=0):
        self.lat = float(lat)
        self.lon = float(lon)

        self.__GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/reverse?"
        self.__api_token = "70bcd9fd2f6471b4018a4839d84f0b11"
        
    def URL(self) -> str:

        # Format API url for specific coordinates
        result_url = self.__GEOCODE_URL + f"lat={self.lat}"
        result_url = result_url + f"&lon={self.lon}"
        result_url = result_url + f"&appid={self.__api_token}"

        # Return final url
        return result_url

    def handleCoordinatesAsCityName(self, query_url) -> str:
        try:

            # Try to obtain json info
            response = request.urlopen(query_url)
        except error.HTTPError as http_error:

            # If any error occurred then return error message
            match http_error.code:
                case 401:
                    return "❌ API Key Error!"
                case 404:
                    return "❌ Couldn't find city info for this geolocation!"
                case _:
                    return "❌ Unknown search error!"

        # Reading json data
        data = response.read()

        try:

            # Return city as string
            data = json.loads(data)[0]
            return str(data["name"] + ", " + data["country"])
        
        except json.JSONDecodeError:

            # If error occured then return error message
            return "❌ Couldn't read the server response!"

    