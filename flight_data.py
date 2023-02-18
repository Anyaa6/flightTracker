class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self):
        pass

    def create_flight_search_params(self, city: dict):
        params = {key:value for key, value in city.items() if key != "city" if key != "id" if value != ""}
        return params