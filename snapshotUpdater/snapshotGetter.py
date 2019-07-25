from pprint import pprint
import requests
import json
import os

from api.models import Snapshot

headers = {
    'Accept': 'application/json', 
    'User-Agent': 'My User Agent 1.0',
}

def get_weather_json():
    url = 'http://api.openweathermap.org/data/2.5/weather'
    encoded_city_name = 'Philadelphia'
    country_code = 'us'
    access_token = os.environ['OPENWEATHERMAP_API_SECRET']
    request_url = '{0}?q={1},{2}&APPID={3}'.format(
        url, 
        encoded_city_name, 
        country_code, 
        access_token)
  
    rw = requests.get(request_url, headers=headers)

    try:
        rw.raise_for_status()
        return rw.json()
    except:
        return None

def get_bike_json():
    url = 'https://www.rideindego.com/stations/json/'
    rb = requests.get(url, headers=headers)
    formatted_dictionary = {}
    try:
        rb.raise_for_status()
        bike_data = rb.json()
        for station in bike_data['features']:
            kioskID = station['properties']['kioskId']
            formatted_dictionary[kioskID] = station
        return formatted_dictionary
    except:
        return None



def new_Snapshot():
    weather_json = get_weather_json()
    bike_json = get_bike_json()

    if weather_json and bike_json:
        pprint(bike_json)
        pprint(weather_json)

        snapshot = Snapshot(
            weather=weather_json,
            stations=bike_json
        )
        snapshot.save()
        print('saved snapshot')

