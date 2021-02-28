import csv
import os
import re
import urllib.request
from urllib.error import HTTPError
from typing import List
import time
from init import common_pattern, friend_count_pattern
from utils import csv_fp
import random


def scrap_url_sets(url_sets: List[dict], user_set: set):
    """

    :param url_sets: a list of dictionaries with the following structure:
                        {"urls" : a set of urls}
                        {"pattern": a compiled re pattern appliable on each of the current dictionary's urls}
    :param user_set: set of already determined users
    :return: void, does update the user_set
    """
    for url_scrapper in url_sets:
        for url in url_scrapper["urls"]:
            # TODO: add http_error try catch
            with urllib.request.urlopen(url) as response:
                if response.code != 200:
                    continue
                html = response.read().decode()
                occurrences = re.findall(url_scrapper["pattern"], html)
                user_set.update(occurrences)


def remove_inconsistent_users(user_set: set):
    """
    TODO: check the real rate limit of MAL and use it
    !This method should be only used on datasets taken from outdated forum pages
    normal MAL rankings ought to be consistent

    :param user_set: set of already determined users
    :return: void, does check the user_set and removes all nonexistent users
    """
    iterable_set = frozenset(user_set)
    i = 0
    n = len(iterable_set)
    for user in iterable_set:
        print(f"{i} from {n}")
        i += 1
        user_url = f"https://myanimelist.net/animelist/{user}"
        try:
            with urllib.request.urlopen(user_url) as response:
                pass
        except HTTPError as err:
            if err.code == 404:
                user_set.remove(user)
                print("removed")
            elif err.code == 418:
                print(418)
                time.sleep(120)
                continue
            else:
                print(err)
                print(err.code)
                print("da deci m-a prins ca is bot")
                return "da deci m-a prins ca is bot"
        time.sleep(60)
    print("DONE")


def update_with_friends(user_set_path: str = "user_set.csv", checked_path: str = "checked_user_set.csv",
                        to_check_path: str = "to_be_checked_user_set.csv") -> set:
    """
    function reads all users, already processed users and the users to be processed now
    takes the last and processes them, and after that moves them to already processed file
    rewrites to be processed users with new data should it exist

    :param user_set_path: a valid path to the csv file containing the already processed users
    :param checked_path: as above but users within were already checked for friends
    :param to_check_path: as above but users within are to be checked for friends
    :return: user_set with all determined users until exit time
    """
    user_set = set()
    checked_users = set()
    to_check_users = set()
    path_set_list = [(user_set_path, user_set), (checked_path, checked_users), (to_check_path, to_check_users)]
    for file, st in path_set_list:
        for i in csv_fp(file):
            st.update(i)
    to_check_users = frozenset(to_check_users)
    for user in to_check_users:
        friends = get_friends(user)
        user_set.update(friends)
    checked_users = set.union(checked_users, to_check_users)
    to_check_users = set.difference(user_set, checked_users)
    for file, st in path_set_list:
        with open(file, "w") as fp:
            write = csv.writer(fp)
            write.writerow(st)
    print("DONE")
    return user_set


def get_friends(user: str, friend_pattern: re.Pattern = common_pattern,
                no_friends_pattern: re.Pattern = friend_count_pattern) -> List[str]:
    """

    :param user: mal user
    :param friend_pattern: compiled re pattern appliable on friend page
    :param no_friends_pattern: compiled re pattern appliable to find number of friends on current user page
    :return: a list of usernames, friends with user
    """
    # TODO: rename to friend scrapper
    return_list = []
    url = f"https://myanimelist.net/profile/{user}/friends"
    with urllib.request.urlopen(url) as response:
        if response.code != 200:
            return return_list
        html = response.read().decode()
    friends_number = int(re.findall(no_friends_pattern, html)[0])
    return_list += re.findall(friend_pattern, html)
    i = 0
    while i + 100 < friends_number:
        # TODO: de vazut daca e ok asa sau se poate un interval mai mic sau trebuie un interval mai mare
        #  stefan poate testezi tu metoda asta
        sleep_interval = random.randint(10, 30)
        time.sleep(sleep_interval)
        i += 100
        url = f"https://myanimelist.net/profile/{user}/friends?offset={i}"
        with urllib.request.urlopen(url) as response:
            if response.code != 200:
                return return_list
            html = response.read().decode()
        return_list += re.findall(friend_pattern, html)
    return return_list
