import os
import requests
from pprint import pprint
from datetime import datetime as dt

KIWI_TOKEN = os.environ.get("KIWI_API_TOKEN")
KIWI_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.header = {"apikey": f"{KIWI_TOKEN}"}
        self.departure_city = self.find_iata_code("Lyon")
        self.today = dt.now().strftime("%d/%m/%Y")

    def find_iata_code(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city",
        }
        city_infos = requests.get(url=KIWI_ENDPOINT, headers=self.header, params=params)
        try:
            city_infos.raise_for_status()
        except requests.HTTPError as err_msg:
            print("There was a request issue with the KIWI API looking for IATA codes")
            print("Error msg : ", err_msg)

        #Some cities do not have an airport for themselves (ex: Kyoto), need to look for alternative departure points
        if city_infos.json()["locations"][0].get("code"):
            return city_infos.json()["locations"][0].get("code")
        else:
            return city_infos.json()["locations"][0].get("alternative_departure_points")[0].get("id")
        # pprint(city_infos.json())

    def find_cheap_flights(self):
        #apikey
        #do not include empty values or "city" in params
        #create function for parameter formatting in flight_data
        pass

