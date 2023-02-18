import os
import requests
from pprint import pprint
from flight_data import FlightData
import json

KIWI_TOKEN = os.environ.get("KIWI_API_TOKEN")
KIWI_ENDPOINT = "https://api.tequila.kiwi.com/"
KIWI_LOCATION_ENDPOINT = "locations/query"
KIWI_FLIGHT_SEARCH_ENDPOINT = "v2/search"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.header = {"apikey": f"{KIWI_TOKEN}"}

    def find_iata_code(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city",
        }
        city_info = requests.get(url=f"{KIWI_ENDPOINT + KIWI_LOCATION_ENDPOINT}", headers=self.header, params=params)
        try:
            city_info.raise_for_status()
        except requests.HTTPError as err_msg:
            print("There was a request issue with the KIWI API looking for IATA codes")
            print("Error msg : ", err_msg)
            print("Error info : ", err_msg.response.text)
            return

        #Some cities do not have an airport for themselves (ex: Kyoto), need to look for alternative departure points
        if city_info.json()["locations"][0].get("code"):
            return city_info.json()["locations"][0].get("code")
        else:
            return city_info.json()["locations"][0].get("alternative_departure_points")[0].get("id")
        # pprint(city_info.json())

    def find_cheap_flights(self, data):
        flight_data = FlightData()
        #apikey
        #do not include empty values or "city" in params
        for city in data:
            params = flight_data.create_flight_search_params(city)
            pprint(params)
            flight_search = requests.get(url=f"{KIWI_ENDPOINT + KIWI_FLIGHT_SEARCH_ENDPOINT}", headers=self.header, params=params)
            try:
                flight_search.raise_for_status()
            except requests.HTTPError as err_msg:
                print("There was a request issue with the KIWI API looking for flights")
                print("Error msg : ", err_msg)
                print("Error info : ", err_msg.response.text)
                return
            # with open("flight_data.json", "a") as flight_search_file:
            #     # Saving the updated data in the same JSON file
            #     json.dump(flight_search.json(), flight_search_file, indent=4)
            pprint(flight_search.json())
            if city["city"] == "Tokyo":
                break

