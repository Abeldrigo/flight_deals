import requests
from dotenv import load_dotenv  # load_dotenv will be used to load the .env file to the environment variables.
import os  # os will be used to refer to those variables in the code
from pprint import pprint  # to see the data formatted.

# Credentials
load_dotenv(".env")  # This will load the .env file

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = os.getenv("TEQUILA_API_KEY")
TEQUILA_REQUEST_HEADERS = {
    "apikey": TEQUILA_API_KEY,
    "Content-Type": "application/json",
}

parameters = {
    "fly_from": "MEX",
    "fly_to": "AGR",
    "date_from": "29/10/2022",
    "date_to": "29/04/2023",
    "nights_in_dst_from": "7",
    "nights_in_dst_to": "28",
    "flight_type": "round",
    "one_for_city": "1",
    "max_stopovers": "6",
    "curr": "EUR",
}

tequila_response = requests.get(
    url=f"{TEQUILA_ENDPOINT}/v2/search",
    params=parameters,
    headers=TEQUILA_REQUEST_HEADERS,
)
tequila_response.raise_for_status()
try:
    data = tequila_response.json()
except IndexError:
    print("No flights found for SYD.")

if not data["data"]:
    print(data["data"])
pprint(data)
# Dictionary Comprehension to get "price", "bags_price", and "deep_link" from data["data"][0]
flight_tracker = {k: v for (k, v) in data["data"][0].items() if k in ["price", "bags_price", "deep_link"]}
# Gets the "currency" from response result and adds it to the dictionary with the flights.
flight_tracker["currency"] = data["currency"]

# Empty list that will have all the flights details
leg_list = []
for leg in data["data"][0]["route"]:
    leg_dic = {k: v for (k, v) in leg.items() if k in
               ["cityCodeFrom", "cityCodeTo", "cityFrom", "cityTo", "flyFrom", "flyTo", "local_arrival",
                "local_departure"]
               }

    leg_list.append(leg_dic)
flight_tracker["route"] = leg_list

# Calls FlightData class passing flight_tracker dictionary to assign the attributes.
# flight_data = FlightData(flight_tracker)
# print(f"{flight_data.destination_city}: €{flight_data.price}")

