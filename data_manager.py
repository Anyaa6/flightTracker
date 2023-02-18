import json
import os
import requests
from flight_search import FlightSearch
import inflection
from pprint import pprint
# To prevent more Sheety API requests
from hardcoded_data import hardcoded_data

SHEETY_BEARER_TOKEN = os.environ.get("SHEETY_BEARER_TOKEN")
SHEETY_ENDPOINT = os.environ.get("SHEETY_PRICES_ENDPOINT")
SHEETY_EDIT_ROW_ENDPOINT = os.environ.get("SHEETY_EDIT_ROW_ENDPOINT")

class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.header = {"Authorization": f"Bearer {SHEETY_BEARER_TOKEN}"}
        # Change below value to empty list [] to do sheety requests
        # Or save requests with self.sheet_data = hardcoded_data
        # Should directly call get_data() but need to save API calls
        self.sheet_data = hardcoded_data

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
            camel_case_data = row_data.json()['prices']
            for n in range(0, len(camel_case_data)):
                self.sheet_data.append({inflection.underscore(key): value for key, value in camel_case_data[n].items()})
            self.check_iata_codes() #TO UNCOMMENT
            with open("./hardcoded_data.py", mode="w") as file:
                pretty_data = json.dumps(self.sheet_data, indent=4).replace("false", "False")
                file.write(f"hardcoded_data = {pretty_data}")
            return self.sheet_data

    def check_iata_codes(self):
        for row in self.sheet_data:
            if "fly_to" not in row:
                row["fly_to"] = FlightSearch().find_iata_code(row.get("city"))

                # No need to put again other infos in body (ex: Lowest price)
                body = {
                    "price": {
                        "fly_to": row.get("fly_to")
                    }
                }
                # do a put request to update row on google sheet
                edit_row = requests.put(url=f"{SHEETY_EDIT_ROW_ENDPOINT}{row.get('id')}", headers=self.header, json=body)
                edit_row.raise_for_status()
                # pprint(self.sheet_data)
