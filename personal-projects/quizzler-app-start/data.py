import requests
URL = "https://opentdb.com/api.php"
PARAMETERS = {
    "amount": 10,
    "type": "boolean",
    "category": 18,
}
class Data:
    def __init__(self):
        self.question_data = []
        self.retrieve_data()

    def retrieve_data(self):
        response = requests.get(URL, params=PARAMETERS)
        response.raise_for_status()
        data = response.json()["results"]
        self.question_data = data

