class FlightData:
    # This class is responsible for structuring the flight data. Is called from FlightSearch class check_flights method.
    def __init__(self, flight_tracker):
        self.currency = flight_tracker["currency"]
        self.price = flight_tracker["price"]
        self.bags_price = flight_tracker["bags_price"]
        flights = flight_tracker["route"]
        len_route = len(flights) - 1
        self.origin_city = f"{flights[0]['cityFrom']}({flights[0]['cityCodeFrom']})"
        self.origin_airport = flights[0]["flyFrom"]
        self.destination_city = f"{flights[len_route]['cityTo']}({flights[len_route]['cityCodeTo']})"
        self.destination_airport = flights[len_route]["flyTo"]
        self.out_date = flights[0]["local_departure"]
        self.return_date = flights[len_route]["local_arrival"]
        self.deep_link = flight_tracker["deep_link"]
