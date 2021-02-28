import re
import urllib.request
from typing import List


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
            with urllib.request.urlopen(url) as response:
                if response.code != 200:
                    continue
                html = response.read().decode()
                occurrences = re.findall(url_scrapper["pattern"], html)
                user_set.update(occurrences)
