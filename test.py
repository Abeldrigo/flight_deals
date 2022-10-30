import requests
from datetime import date
from dateutil.relativedelta import relativedelta
from pprint import pprint  # to see the data formatted.
from dotenv import load_dotenv  # load_dotenv will be used to load the .env file to the environment variables.
import os  # os will be used to refer to those variables in the code

# Credentials
load_dotenv(".env")  # This will load the .env file

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = os.getenv("TEQUILA_API_KEY")
TEQUILA_REQUEST_HEADERS = {
    "apikey": TEQUILA_API_KEY,
    "Content-Type": "application/json",
}

tomorrow_dt = date.today() + relativedelta(days=1)
six_months_dt = date.today() + relativedelta(months=6)

cities = ["PAR", "BER", "TYO", "SYD", "IST", "KUL", "NYC", "SFO", "CPT", "BUH", "YMQ", "ROM", "MAD", "TLV", "AGR"]
for city in cities:
    parameters = {
        "fly_from": "MEX",
        "fly_to": city,
        "date_from": tomorrow_dt.strftime("%d/%m/%Y"),
        "date_to": six_months_dt.strftime("%d/%m/%Y"),
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
    data = tequila_response.json()

    # Dictionary Comprehension to get "price", "bags_price", and "deep_link" from data["data"][0]
    flight_tracker = {k: v for (k, v) in data["data"][0].items() if k in ["price", "bags_price", "deep_link"]}
    # Gets the "currency" from response result and adds it to the dictionary with the flights.
    flight_tracker["currency"] = data["currency"]

    # Empty list that will have all the flights details
    leg_list = []
    for leg in data["data"][0]["route"]:
        leg_dic = {k: v for (k, v) in leg.items() if k in
                   ["cityCodeFrom", "cityCodeTo", "cityFrom", "cityTo", "flyFrom", "flyTo", "local_arrival", "local_departure"]
                   }

        leg_list.append(leg_dic)
    flight_tracker["route"] = leg_list
    pprint(flight_tracker)
    print(flight_tracker["route"][0]["local_departure"])
    len_route = len(flight_tracker["route"]) - 1
    print(flight_tracker["route"][len_route]["local_arrival"])
