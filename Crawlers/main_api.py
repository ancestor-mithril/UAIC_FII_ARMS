import random

from init import init_user_set
from my_anime_list_api import init_api, get_user_data, process_user_list, refresh_token, collect_data, \
    save_anime_data
import time


def run():
    """"""
    user_set, anime_dict, anime_data = init_user_set()
    print("user set len", len(user_set))
    init_api()
    for i in range(100):
        print(i)
        user = user_set.pop()
        x = get_user_data(user)
        y = process_user_list(x)
        if y is None:
            print(None)
            continue
        collect_data(y, anime_dict, anime_data)
        sleep_interval = random.uniform(0.5, 1.0)
        time.sleep(sleep_interval)
    save_anime_data(anime_data, user_set)


if __name__ == "__main__":
    run()
