import requests
import os
from dotenv import load_dotenv
load_dotenv()
headers= {
    "Authorization": os.getenv("Authorization")
}
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
AMADEUS_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
OFFER_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.getenv("AMADEUS_API_KEY")
        self._api_secret = os.getenv("AMADEUS_API_SECRET")
        self._token = self._get_new_token()

    def _get_new_token(self):
        header = {
            "Content_Type": "application/x-www-form-urlencoded"
        }
        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret
        }
        response = requests.post(AMADEUS_ENDPOINT, headers=header, data=body)
        return response.json()["access_token"]
    def get_destination_iata(self, city_name):
        headers = {
            "Authorization": f"Bearer {self._token}"
        }
        body = {
            "keyword": city_name,
            "max": "2"
        }
        response = requests.get(url=IATA_ENDPOINT, headers=headers, params=body)
        try:
            code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError: No airport was found in the name {city_name}")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport under {city_name} was found.")
            return "Not Found"

        return code

    def check_flight(self,origin_code, destination_code, out_date, back_date, is_direct=True):
        body = {
            "currencyCode": "GBP",
            "adults": 1,
            "nonStop": 'true' if is_direct else 'false',
            "originLocationCode": origin_code,
            "destinationLocationCode": destination_code,
            "departureDate": out_date.strftime("%Y-%m-%d"),
            "returnDate": back_date.strftime("%Y-%m-%d"),
            "max": "10"

        }
        header = {
            "Authorization": f"Bearer {self._token}"
        }

        response = requests.get(url=OFFER_ENDPOINT, headers=header, params=body)

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)
            return None

        return response.json()

