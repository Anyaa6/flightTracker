# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import os
import datetime as dt
from data_manager import DataManager
from flight_search import FlightSearch
from pprint import pprint

KIWI_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"

#!!! bien verifier que la data a l'INTERIEUR du tableau n'a pas besoin non plus de passer en snake_case
# Prevent extra API requests to Sheety
data = DataManager().get_data()
# pprint(data)
FlightSearch().find_cheap_flights(data)
# print(FlightSearch().today)
