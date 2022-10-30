from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
from datetime import date
from dateutil.relativedelta import relativedelta
from pprint import pprint  # to see the data formatted.

ORIGIN_CITY_IATA = "MEX"

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

flight_search = FlightSearch()

notification_manager = NotificationManager()
# pprint(sheet_data)  # to see the data formatted(json).

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    # print(f"sheet_data:\n {sheet_data}")

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow_dt = date.today() + relativedelta(days=1)
six_months_dt = date.today() + relativedelta(months=6)

for destination in sheet_data:
    flight = flight_search.check_flights(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=destination["iataCode"],
        from_time=tomorrow_dt,
        to_time=six_months_dt
    )

    # Validates is flight is found and the price is below 25% of the price we have on sheets.
    if flight is not None and round(
            (destination["lowestPrice"] - flight.price) / destination["lowestPrice"] * 100) >= 25:
        notification_manager.send_notification(flight_details=flight)

