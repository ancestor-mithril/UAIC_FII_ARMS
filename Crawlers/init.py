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


def init_user_set(file: str = "user_set_1.csv"):
    """

    :param file: a valid path to the csv file containing the already processed users
    :return: void, does add read users to global user_set
    """
    global user_set
    for i in csv_fp(file):
        # print(i)
        user_set.update(i)

