import requests
from .types import WeatherInfo, GeoLocation

#Main request url
WEATHER_INFO_ENDPOINT = "http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}"

#Geocoder url
GEOCODE_INFO_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct?q={cityname}&limit=100&appid={apikey}"

def fetch_geolocation(cityname, apikey: str) -> list[GeoLocation]:
    """
    Fetches geo info based on cityname, will return multiple values if multiple cities by the same name exist.

    IN:
        cityname - Name of the city to get GeoLocation info for
        apikey - api key to perform the query

    OUT:
        A list of GeoLocation objects
    """
    rv: list[GeoLocation] = list()

    resp = requests.get(
        GEOCODE_INFO_ENDPOINT.format(
            cityname=cityname,
            apikey=apikey
        )
    )

    #Since there's likely more than one, we convert all
    for item in resp.json():
        rv.append(GeoLocation(**item))

    return rv

def fetch_weather_info(lat: float, lon: float, apikey) -> WeatherInfo:
    """
    Fetches weather info given latitude and longitude and an api key

    IN:
        lat - Latitude of the location to get weather for
        lon - Longitude of the location to get weather for
        apikey - Api key to perform the query

    OUT:
        WeatherInfo object representing the weather at the specified location
    """
    resp = requests.get(
        WEATHER_INFO_ENDPOINT.format(
            lat=lat,
            lon=lon,
            apikey=apikey
        )
    )

    return WeatherInfo.from_json(resp.json())
