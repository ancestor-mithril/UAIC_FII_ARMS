import csv
import io
import json
import re

import requests
from dotenv import load_dotenv
import os

load_dotenv()

# endpoint = "https://api.myanimelist.net/v2/users/ChampionChaos/animelist?fields=list_status&&limit=1000"
headers = None
data = None


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
            user_anime_list[re.sub(r"[^a-zA-Z0-9_ ]", "", anime_data["node"]["title"])] = score
    return user_anime_list


def collect_data(user_anime_list: dict, anime_list: list, anime_dict: dict):
    """
    1. creates a dict of score, list of animes
    2. appends new anime to anime list
    3. adds relation between all animes with the same score

    :param user_anime_list: dictionary of anime title and score
    :return: void, collects data and adds it to anime list and anime dict
    """
    scores = {i: [] for i in range(6, 11)}
    for anime in user_anime_list:
        scores[user_anime_list[anime]].append(anime)
        if anime not in anime_list:
            anime_list.append(anime)
    for score in scores:
        n = len(scores[score])
        for i in range(n - 1):
            index_1 = anime_list.index(scores[score][i])
            for j in range(i + 1, n):
                index_2 = anime_list.index(scores[score][j])
                i_min = str(min(index_1, index_2))
                i_max = str(max(index_1, index_2))
                if i_min not in anime_dict.keys():
                    anime_dict[i_min] = dict()
                if i_max not in anime_dict[i_min].keys():
                    anime_dict[i_min][i_max] = {str(i): 0 for i in range(6, 11)}
                anime_dict[i_min][i_max][str(score)] += 1


def re_print(user_set, anime_list, anime_dict):
    """

    :return: void, prints user_list, anime_list and anime_dict
    """
    with open("user_set.csv", "w") as fp:
        write = csv.writer(fp)
        write.writerow(user_set)
    with io.open("anime_list.csv", "w", encoding="utf-8") as fp:
        fp.write(str(anime_list))
    a = {i: j for i, j in enumerate(anime_list)}
    with io.open("anime_list.json", "w", encoding="utf-8") as fp:
        json.dump(a, fp)
    with open("anime_dict.json", "w") as fp:
        json.dump(anime_dict, fp)


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

