# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import os
import datetime as dt
from data_manager import DataManager
from flight_search import FlightSearch
from pprint import pprint

KIWI_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"

# Prevent extra API requests to Sheety
data_manager = DataManager().get_data()
pprint(data_manager)

# print(FlightSearch().today)
