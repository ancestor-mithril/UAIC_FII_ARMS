import os
import re
import sys
from typing import List

import requests
from dotenv import load_dotenv


def init_anime_model(anime_data_file: str = "anime_data.csv") -> List[List[List[int]]]:
    anime_model = [[[0 for k in range(3)] for j in range(i + 1, 1000)] for i in range(1000 - 1)]
    with open(anime_data_file, "r") as fp:
        for line in fp.readlines():
            data = line.split(",")
            if len(data) == 4:
                data = list(map(int, data))
                anime_model[data[0]][data[1] - data[0] - 1][data[2]] = data[3]
    return anime_model


def init_anime_dict(anime_id_file: str = "anime_set.csv", anime_score_file: str = "anime_set_genres.csv") -> dict:
    anime_list = []
    anime_score_list = []
    anime_id_pattern = re.compile(r"- (\w+) :")
    anime_score_pattern = re.compile(r"\d+,\d+,(.*?),")
    with open(anime_id_file, "r") as fp:
        for line in fp.readlines():
            anime_id = re.findall(anime_id_pattern, line)
            if len(anime_id) > 0:
                anime_list.append(int(anime_id[0]))
    with open("anime_set_genres.csv", "r") as fp:
        for line in fp.readlines():
            anime_score = re.findall(anime_score_pattern, line)
            if len(anime_score) > 0:
                anime_score_list.append(float(anime_score[0]))
    anime_dict = dict()
    for i in range(len(anime_list)):
        anime_dict[anime_list[i]] = {"position": i, "score": anime_score_list[i]}
    return anime_dict


def anime_model_i_j(anime_model: List[List[List[int]]], i: int, j: int) -> int:
    return anime_model[min(i, j)][max(i, j) - min(i, j) - 1][1] + 2 * anime_model[min(i, j)][max(i, j) - min(i, j) - 1][2]


def create_preference_dict(anime_dict: dict) -> dict:
    return {key: 1 for key in anime_dict.keys()}


def get_api_headers() -> dict:
    try:
        load_dotenv()
        access_token = refresh_token()
        return {"Authorization": f"Bearer {access_token}"}
    except Exception as e:
        error_print(e)
        raise Exception(".env file does not exist or does not have expected variables")


def get_api_endpoint(user: str) -> str:
    return f"https://api.myanimelist.net/v2/users/{user}/animelist?fields=list_status&&limit=1000"


def get_user_data(user: str):
    endpoint = get_api_endpoint(user)
    headers = get_api_headers()
    return requests.get(endpoint, data=None, headers=headers)


def process_user_data(user: str) -> dict:
    try:
        user_data = (get_user_data(user)).json()
    except Exception as e:
        error_print(e)
        raise Exception("erroneous api call")
    if "error" in user_data.keys():
        error_print(user_data)
        raise Exception(f"api call succeeded, got error response: {user_data['error']}")
    if "data" not in user_data.keys():
        error_print(user_data)
        raise Exception("api call succeeded, unknown format")
    user_anime_dict = dict()
    for anime in user_data["data"]:
        score = anime["list_status"]["score"]
        if not score:
            score = 0
        user_anime_dict[anime["node"]["id"]] = score
    return user_anime_dict


def refresh_token() -> str:
    base_url = "https://myanimelist.net/v1/oauth2/token"
    try:
        load_dotenv()
        refresh_params = {
            "client_id": os.getenv("CLIENT_ID"),
            "client_secret": os.getenv("CLIENT_SECRET"),
            "grant_type": "refresh_token",
            "refresh_token": os.getenv("REFRESH_TOKEN")
        }
    except Exception as e:
        error_print(e)
        raise Exception(".env file does not exist or does not have expected variables")
    response = requests.post(base_url, refresh_params).json()
    os.putenv("REFRESH_TOKEN", response["refresh_token"])
    os.putenv("ACCESS_TOKEN", response["access_token"])
    print(response)
    with open("new_tokens.json", "w") as fp:
        fp.write(str(response))
    return response["access_token"]


def error_print(*args, **kwargs):
    print(*args, file=sys.stderr, end="\n\n", **kwargs)


def get_multiplier(score: float):
    if score == 0:
        return 0
    if score == 5:
        return -0.5
    if score == 6:
        return -0.25
    if score == 7:
        return 0.25
    if score == 8:
        return 1
    if score == 9:
        return 1.25
    if score == 10:
        return 1.5
    return -0.75


def get_value_of_connection(anime_model: List[List[List[int]]], anime_position, other_anime_position, score) -> int:
    multiplier = get_multiplier(score)
    connection = anime_model_i_j(anime_model, anime_position, other_anime_position)
    if score == 10:
        return multiplier * connection
    return multiplier * connection


def predict_anime_for_user(user: str, predicted: int = 5):
    anime_model = init_anime_model()
    anime_dict = init_anime_dict()
    preference_dict = create_preference_dict(anime_dict)
    user_anime_dict = process_user_data(user)
    for anime, score in user_anime_dict.items():
        if anime not in anime_dict.keys():
            continue
        del preference_dict[anime]
        anime_position = anime_dict[anime]["position"]
        for other_anime in preference_dict.keys():
            other_anime_position = anime_dict[other_anime]["position"]
            value = get_value_of_connection(anime_model, anime_position, other_anime_position, score)
            preference_dict[other_anime] += value
    for key in preference_dict.keys():
        preference_dict[key] *= anime_dict[key]["score"]
    # print(preference_dict)
    sorted_list = dict(sorted(preference_dict.items(), key=lambda item: -item[1]))
    if predicted > len(sorted_list.keys()):
        predicted = len(sorted_list.keys())
    return [f"https://myanimelist.net/anime/{x}" for x in (list(sorted_list.keys())[:predicted])]
