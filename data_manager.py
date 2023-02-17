import os
import requests
from flight_search import FlightSearch
from pprint import pprint

SHEETY_BEARER_TOKEN = os.environ.get("SHEETY_BEARER_TOKEN")
SHEETY_ENDPOINT = os.environ.get("SHEETY_PRICES_ENDPOINT")
SHEETY_EDIT_ROW_ENDPOINT = os.environ.get("SHEETY_EDIT_ROW_ENDPOINT")

# To prevent more Sheety API requests
temp_data = [{'city': 'Kyoto', 'flyFrom': 'KIX', 'id': 2},
 {'city': 'Fukuoka', 'flyFrom': 'FUK', 'id': 3},
 {'city': 'Tokyo', 'flyFrom': 'TYO', 'id': 4},
 {'city': 'Lisbon', 'flyFrom': 'LIS', 'id': 5},
 {'city': 'Istanbul', 'flyFrom': 'IST', 'id': 6},
 {'city': 'New York', 'flyFrom': 'NYC', 'id': 7},
 {'city': 'Berlin', 'flyFrom': 'BER', 'id': 8},
 {'city': 'Taipei', 'flyFrom': 'TPE', 'id': 9},
 {'city': 'Tainan', 'flyFrom': 'TNN', 'id': 10}]


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.header = {"Authorization": f"Bearer {SHEETY_BEARER_TOKEN}"}
        # Change below value to empty dict {} or list [] to do sheety requests
        # Or save requests with self.sheet_data = temp_data
        # Should directly call get_data() but need to save API calls
        self.sheet_data = {}

    def get_data(self):
        #prevent extra sheety requests
        if self.sheet_data:
            return self.sheet_data
        row_data = requests.get(url=SHEETY_ENDPOINT, headers=self.header)
        try:
            row_data.raise_for_status()
        except requests.HTTPError as err_msg:
            print("There was an API issue when getting the rows of the Google Sheet")
            print("Error msg : ", err_msg)
        else:
            self.sheet_data = row_data.json()['prices']
            # self.check_iata_codes()
            # pprint(self.sheet_data)
            return self.sheet_data

    def check_iata_codes(self):
        for row in self.sheet_data:
            if "flyFrom" not in row:
                row["flyFrom"] = FlightSearch().find_iata_code(row.get("city"))

                # No need to put again other infos in body (ex: Lowest price)
                body = {
                    "price": {
                        "flyFrom": row.get("flyFrom")
                    }
                }
                # do a put request to update row on google sheet
                edit_row = requests.put(url=f"{SHEETY_EDIT_ROW_ENDPOINT}{row.get('id')}", headers=self.header, json=body)
                edit_row.raise_for_status()
                # pprint(self.sheet_data)
