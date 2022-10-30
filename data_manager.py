import requests
from dotenv import load_dotenv  # load_dotenv will be used to load the .env file to the environment variables.
import os  # os will be used to refer to those variables in the code

# Credentials
load_dotenv(".env")  # This will load the .env file

# sheety.co/docs/requests   -> Need to sing in with google account.
SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
SHEETY_REQUEST_HEADERS = {
    "Authorization": os.getenv("SHEETY_TOKEN"),
    "Content-Type": "application/json",
}


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        sheety_response = requests.get(url=SHEETY_ENDPOINT, headers=SHEETY_REQUEST_HEADERS)
        sheety_response.raise_for_status()
        data = sheety_response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    # PUT Request that use the row id from sheet_data to update the Google Sheet with the IATA codes
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            sheety_response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=SHEETY_REQUEST_HEADERS
            )
            print(sheety_response.text)
