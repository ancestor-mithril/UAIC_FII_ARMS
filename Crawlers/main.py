import urllib.request
import re
from init import url_sets, user_set, init_user_set


def run():
    user_set_csv = "./user_set.csv"
    init_user_set(user_set_csv)

    for url_scrapper in url_sets:
        for url in url_scrapper["urls"]:
            with urllib.request.urlopen(url) as response:
                if response.code != 200:
                    continue
                html = response.read().decode()
                occurrences = re.findall(url_scrapper["pattern"], html)
                user_set.update(occurrences)

    print("lenght of user_set:", len(user_set))
    with open(user_set_csv, "w") as fp:
        # print(",".join(user_set))
        fp.write(",".join(user_set))


if __name__ == "__main__":
    run()


