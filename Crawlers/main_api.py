import random

from init import init_user_set
from my_anime_list_api import init_api, get_user_data, process_user_list, refresh_token, collect_data, \
    save_anime_data
import time


def run():
    """"""
    user_set, anime_dict, anime_data = init_user_set()
    init_api()
    x = get_user_data("stefanforce")
    y = process_user_list(x)
    if y is None:
        print(None)
    print(y)
    collect_data(y, anime_dict, anime_data)
    sleep_interval = random.uniform(0.5, 1.0)
    time.sleep(sleep_interval)
    save_anime_data(anime_data, user_set)


if __name__ == "__main__":
    run()
