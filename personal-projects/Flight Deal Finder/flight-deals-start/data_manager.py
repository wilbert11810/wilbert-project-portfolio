import requests
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv()
headers= {
    "Authorization": os.getenv("Authorization")
}
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination = {}
        self.users = []
        self.user_endpoint = os.getenv("USER_ENDPOINT")
        self.prices_endpoint = os.getenv("PRICES_ENDPOINT")
    def retrieve_data(self):
        response = requests.get(self.prices_endpoint,headers=headers)
        data = response.json()
        self.destination = data["prices"]
        return self.destination

    def get_customer_emails(self):
        response = requests.get(self.user_endpoint, headers=headers)
        data = response.json()
        for user in data['users']:
            self.users.append(user["whatIsYourEmail?"])
        return self.users


    def update_destination_code(self):
        for city in self.destination:
            new_data = {
                "price" : {
                    "iataCode": city["iataCode"]
                }
            }
            endpoint = f"{self.prices_endpoint}/{city["id"]}"

            response = requests.put(url=endpoint, headers=headers, json=new_data)
            print(response.text)
