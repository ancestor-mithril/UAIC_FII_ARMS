import requests
from dotenv import load_dotenv
import os


load_dotenv()

endpoint = "https://api.myanimelist.net/v2/users/stefanforce/animelist?fields=list_status&&limit=1000"
headers = {"Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"}
data = {
    "fields": "list_status"
}

x = requests.get(endpoint, data=None, headers=headers).json()
print(x)
print("ok")

# TODO: refresh the API token each 50 requests

