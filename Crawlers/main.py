import csv

from functions import scrap_url_sets, remove_inconsistent_users, update_with_friends, get_ro_users, get_anime
from init import url_sets, user_set, init_user_set


def obsolete():
    # scrap_url_sets(url_sets, user_set)  # initial method of getting the most important users
    # by taking the most popular and appreciated comment posters
    # should not be used anymore

    # remove_inconsistent_users(user_set)  # done once, should be enough
    # update_with_friends(check_limit=500)  # done once
    pass


def run():
    anime_set_csv = "./anime_set.csv"

    anime_dict = get_anime(anime_set_csv)
    print("length of anime_set:", len(anime_dict))


if __name__ == "__main__":
    run()
