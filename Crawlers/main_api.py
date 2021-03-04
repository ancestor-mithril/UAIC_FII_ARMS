import random

from init import init_user_set
from my_anime_list_api import init_api, get_user_data, process_user_list, refresh_token, collect_data, re_print
import time


def run():
    user_set, anime_list, anime_dict = init_user_set()
    i = 0
    print("user set", len(user_set))
    print("anime list", len(anime_list))
    print("anime, dict", len(anime_dict))
    init_api()
    while i < 100:
        i += 1
        print(i)
        user = user_set.pop()
        x = get_user_data(user)
        y = process_user_list(x)
        if y is None:
            print(None)
            continue
        collect_data(y, anime_list, anime_dict)
        sleep_interval = random.uniform(0.5, 1.0)
        time.sleep(sleep_interval)

    # re_print(user_set, anime_list, anime_dict)


if __name__ == "__main__":
    run()
