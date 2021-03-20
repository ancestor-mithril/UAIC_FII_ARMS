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


def init_user_set(user_file: str = "user_set.csv", anime_file: str = "anime_set.csv",
                  anime_data_file: str = "anime_data.csv"):
    """

    :param user_file: a valid path to the csv file containing the already processed users
    :param anime_file: a valid path to the csv file containing the list of anime
    :param anime_data_file:
    :return: user
    """
    global user_set
    global anime_dict
    global anime_list
    for i in csv_fp(user_file):
        user_set.update(i)
    anime_list = []
    anime_id_pattern = re.compile(r"- (\w+) :")
    with open(anime_file, "r") as fp:
        for line in fp.readlines():
            anime_id = re.findall(anime_id_pattern, line)
            if len(anime_id) > 0:
                anime_list.append(int(anime_id[0]))
    anime_dict = dict()
    for i in range(len(anime_list)):
        anime_dict[anime_list[i]] = i
    anime_data = [[[0 for k in range(3)] for j in range(i + 1, 1000)] for i in range(1000 - 1)]
    with open(anime_data_file, "r") as fp:
        for line in fp.readlines():
            data = line.split(",")
            if len(data) == 4:
                data = list(map(int, data))
                anime_data[data[0]][data[1] - data[0] - 1][data[2]] = data[3]

    return user_set, anime_dict, anime_data


