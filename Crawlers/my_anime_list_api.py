import csv
import io
import json
import re
from typing import List

import requests
from dotenv import load_dotenv
import os

load_dotenv()

# endpoint = "https://api.myanimelist.net/v2/users/ChampionChaos/animelist?fields=list_status&&limit=1000"
headers = None
data = None

score_value = {
    10: 0,
    9: 1,
    8: 1,
    7: 2,
    6: 2
}

def init_api():
    """
    initializes headers used in mal api requests

    :return: void
    """
    global headers
    headers = {"Authorization": f"Bearer {os.getenv('ACCESS_TOKEN')}"}
    print(os.getenv('ACCESS_TOKEN'))


def get_user_data(user: str):
    """

    :param user: username of mal user
    :return: { data: [list of {node(anime) , status(score)} ] }
    """
    global headers
    endpoint = f"https://api.myanimelist.net/v2/users/{user}/animelist?fields=list_status&&limit=1000"
    x = requests.get(endpoint, data=None, headers=headers).json()
    return x


def process_user_list(user_list: dict):
    """

    :param user_list: { data: [list of {node(anime) , status(score)} ] }
    :return: dictionary of anime title and score
    """
    if "error" in user_list:
        print("ERROR", user_list)
        return None
    user_anime_list = dict()
    for anime_data in user_list["data"]:
        score = anime_data["list_status"]["score"]
        if score > 5:
            user_anime_list[anime_data["node"]["id"]] = score_value[score]
    return user_anime_list


def collect_data(user_anime_list: dict, anime_dict: list, anime_data: List[List[List[int]]]):
    """
    1. creates a dict of score, list of animes
    2. appends new anime to anime list
    3. adds relation between all animes with the same score

    :param user_anime_list: dictionary of anime title and score
    :return: void, collects data and adds it to anime list and anime dict
    """
    scores = {i: [] for i in range(3)}
    for anime in user_anime_list:
        if anime in anime_dict:
            scores[user_anime_list[anime]].append(anime)
    for score in scores:
        n = len(scores[score])
        for i in range(n - 1):
            anime_index_1 = anime_dict[scores[score][i]]
            for j in range(i + 1, n):
                anime_index_2 = anime_dict[scores[score][j]]
                i_min = min(anime_index_1, anime_index_2)
                i_max = max(anime_index_1, anime_index_2)
                anime_data[i_min][i_max - i_min - 1][score] += 1


def save_anime_data(anime_data, user_set):
    with open("user_set.csv", "w") as fp:
        write = csv.writer(fp)
        write.writerow(user_set)
    with open("anime_data.csv", "w") as fp:
        write = csv.writer(fp)
        for anime_1 in range(len(anime_data)):
            for anime_2 in range(len(anime_data[anime_1])):
                for category in range(3):
                    write.writerow([anime_1, anime_2 + anime_1 + 1, category, anime_data[anime_1][anime_2][category]])


def refresh_token():
    base_url = "https://myanimelist.net/v1/oauth2/token"
    refresh_params = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "refresh_token",
        "refresh_token": os.getenv("REFRESH_TOKEN")
    }
    x = requests.post(base_url, refresh_params).json()
    print(x)
    os.putenv("REFRESH_TOKEN", x["refresh_token"])
    os.putenv("ACCESS_TOKEN", x["access_token"])
    init_api()
    with open("new_tokens.json", "w") as fp:
        fp.write(str(x))
# TODO: refresh the API token each 50 requests

