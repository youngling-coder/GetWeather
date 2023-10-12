from urllib import request, error
import json, os


class Location:
    def __init__(self, lat=0, lon=0):
        self.lat = float(lat)
        self.lon = float(lon)

        self.__GEOCODE_URL = "https://nominatim.openstreetmap.org/reverse?format=json&"
        
    def URL(self) -> str:

        # Format API url for specific coordinates
        result_url = self.__GEOCODE_URL + f"lat={self.lat}"
        result_url = result_url + f"&lon={self.lon}"

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
            data = json.loads(data)
            if 'city' in list(data['address'].keys()):
                return data["address"]["city"] + ", " + data["address"]["country_code"]
            elif 'town' in list(data['address'].keys()):
                return data["address"]["town"] + ", " + data["address"]["country_code"]
            elif 'village' in list(data['address'].keys()):
                return data["address"]["village"] + ", " + data["address"]["country_code"]
            else:
                return data["address"]["country_code"]
        
        except json.JSONDecodeError:

            # If error occured then return error message
            return "❌ Couldn't read the server response!"

    
