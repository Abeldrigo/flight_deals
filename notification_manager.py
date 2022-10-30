import requests
from twilio.rest import Client

# load_dotenv will be used to load the .env file to the environment variables.
from dotenv import load_dotenv
# os will be used to refer to those variables in the code
import os

# Credentials
load_dotenv(".env")  # This will load the .env file

#  twilio API Parameters
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_notification(self, flight_details):
        # This class is responsible for sending notifications with the deal flight details.
        # twilio client. To send SMS
        message = self.client.messages.create(
            body=f"Low price alert! only €{flight_details.price} "
                 f"to fly from {flight_details.origin_city} - {flight_details.origin_airport} "
                 f"to {flight_details.destination_city} - {flight_details.destination_airport} "
                 f"from {flight_details.out_date} "
                 f"to {flight_details.return_date} \n"
                 f"Bags Price: {flight_details.bags_price} \n"
                 f"Link: {flight_details.deep_link}",
            from_="+18782192133",
            to="+525611779621",
        )

        # Prints if successfully sent.
        print(message.status)
