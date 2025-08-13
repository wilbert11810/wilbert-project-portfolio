#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import time
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import timedelta, datetime
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager


response_data = DataManager()
list_city = response_data.retrieve_data()
list_email = response_data.get_customer_emails()
update_data = FlightSearch()
twilio_message = NotificationManager()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
ORIGIN_CITY_IATA = "LON"

for destination in list_city:
    print(f"Getting flights for {destination['city']}...")
    flights = update_data.check_flight(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        out_date=tomorrow,
        back_date=six_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)
    if cheapest_flight.stops == 0:
        message = f"Low price alert! Only £{cheapest_flight.prices} to fly from {cheapest_flight.departure_airport_code} to {cheapest_flight.arrival_airport_code}, on {cheapest_flight.departure_date} until {cheapest_flight.return_date}"
    else:
        message = f"Low price alert! Only £{cheapest_flight.prices} to fly from {cheapest_flight.departure_airport_code} to {cheapest_flight.arrival_airport_code} with {cheapest_flight.stops} transit, on {cheapest_flight.departure_date} until {cheapest_flight.return_date}"
    try:
        if cheapest_flight.prices < destination["lowestPrice"]:
            twilio_message.send_emails(list_email, message)
    except ValueError:
        print(f"Invalid price data for {destination['city']}. Skipping...")

    print(f"{destination['city']}: £{cheapest_flight.prices}")
    time.sleep(2)

