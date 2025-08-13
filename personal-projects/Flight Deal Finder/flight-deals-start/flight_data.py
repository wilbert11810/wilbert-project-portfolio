
class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, prices, out_code, in_code, out_date, return_date, stops):
        self.prices = prices
        self.departure_airport_code = out_code
        self.arrival_airport_code = in_code
        self.departure_date = out_date
        self.return_date = return_date
        self.stops = stops


def find_cheapest_flight(data):
    if data is None or not data["data"]:
        print("No data available")
        return FlightData('N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A')


    first_flight = data["data"][0]
    flight_price = float(first_flight["price"]["grandTotal"])
    nr_stops = len(first_flight["itineraries"][0]["segments"]) - 1
    departure = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    arrival = first_flight["itineraries"][0]["segments"][nr_stops]["arrival"]["iataCode"]
    departure_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    back_date = departure_date = first_flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]

    cheapest_flight = FlightData(flight_price, departure, arrival, departure_date, back_date, nr_stops)

    for flight in data["data"]:
        prices = float(flight["price"]["grandTotal"])
        if prices < flight_price:
            flight_price = prices
            origin = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            destination = flight["itineraries"][0]["segments"][nr_stops]["arrival"]["iataCode"]
            out_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            return_date = flight["itineraries"][1]["segments"][0]["departure"]["at"].split("T")[0]
            cheapest_flight = FlightData(flight_price, origin, destination, out_date, return_date, nr_stops)
            print(f"Lowest price to {destination} is £{flight_price}")

    return cheapest_flight
