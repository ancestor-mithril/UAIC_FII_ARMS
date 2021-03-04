import re
import csv
import os

from utils import csv_fp

common_url_set = {
    'https://myanimelist.net/reviews.php?st=mosthelpful',
}

uncommon_url_set_1 = {
    'https://myanimelist.net/blog.php?eid=830113',
}

common_pattern = re.compile(r'\/profile\/(.*?)"><strong>\1<')  # valid for every friend file
uncommon_pattern_1 = re.compile(r'profile/(.*?)" rel="nofollow">\1<')
# valid for this forum link: https://myanimelist.net/blog.php?eid=830113
friend_count_pattern = re.compile(r'>All \((\d+)\)<\/')

url_sets = [
    {
        "urls": uncommon_url_set_1,
        "pattern": uncommon_pattern_1
    },
    {
        "urls": common_url_set,
        "pattern": common_pattern
    }
]

user_set = set()
anime_list = list()
anime_dict = dict()


def init_user_set(user_file: str = "user_set.csv", anime_file: str = "anime_list.csv"):
    """

    :param user_file: a valid path to the csv file containing the already processed users
    :param anime_file: a valid path to the csv file containing the list of anime
    :return: void, does add read users to global user_set and animes to anime_set
    """
    global user_set
    global anime_list
    global anime_dict
    for i in csv_fp(user_file):
        user_set.update(i)
    anime_list = eval(open(anime_file, "r").read())
    anime_dict = eval(open("anime_dict.json", "r").read())
    return user_set, anime_list, anime_dict


