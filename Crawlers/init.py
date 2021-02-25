import re
import csv
import os

common_url_set = {
    'https://myanimelist.net/reviews.php?st=mosthelpful',
}

uncommon_url_set_1 = {
    'https://myanimelist.net/blog.php?eid=830113',
}

common_pattern = re.compile(r'/profile\/(.*?)"><strong>\1<')  # valid for every friend file
uncommon_pattern_1 = re.compile(r'profile/(.*?)" rel="nofollow">\1<')

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


def init_user_set(file: str = "user_set.csv"):
    assert os.path.isfile(file), f"{file} is not a path to a valid file"
    fp = open(file)
    try:
        csv_fp = csv.reader(fp)
    except Exception as e:
        raise Exception("file not a csv file")
    for i in csv_fp:
        # print(i)
        user_set.update(i)

