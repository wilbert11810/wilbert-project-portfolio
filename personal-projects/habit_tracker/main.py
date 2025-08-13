import requests
from datetime import datetime

USERNAME ="wilbert118"
TOKEN = "asdfdsfr123"
USERID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsofService": "yes",
    "notMinor": "yes",
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": USERID,
    "name": "Cycling Graph",
    "unit": "Km",
    "type": "float",
    "color": "ajisai"
}

header = {
    "X-USER-TOKEN": TOKEN,
}

# reponse = requests.post(url=graph_endpoint, json=graph_config, headers=header)
# print(reponse.text)

graph_post_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{USERID}"
today = datetime(year=2025, month=5, day=28)
graph_post_config = {
    "date": today.strftime('%Y%m%d'),
    "quantity": "12"

}

# update_data = requests.post(url=graph_post_endpoint, json=graph_post_config, headers=header)
# print(update_data.text)

graph_put_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{USERID}/{today.strftime('%Y%m%d')}"

graph_put_config = {
    "quantity": "5"
}
# updateed_data = requests.put(url=graph_put_endpoint, json=graph_put_config, headers=header)
# print(updateed_data.text)

delete_data = requests.delete(url=graph_put_endpoint, headers=header)
print(delete_data.text)