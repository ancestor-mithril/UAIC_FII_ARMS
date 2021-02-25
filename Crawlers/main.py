import urllib.request
import re


uncommon_url_set_1 = {
    'https://myanimelist.net/blog.php?eid=830113',
}

common_url_set = {
    'https://myanimelist.net/reviews.php?st=mosthelpful',
}

common_pattern = re.compile(r'/profile\/(.*?)"><strong>\1<')
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


user_set = {
    'stefanforce',
    'nirmian',
    'kkkkkk99',
}


for url_scrapper in url_sets:
    for url in url_scrapper["urls"]:
        with urllib.request.urlopen(url) as response:
            if response.code != 200:
                continue
            html = response.read().decode()
            occurrences = re.findall(url_scrapper["pattern"], html)
            user_set.update(occurrences)

print("\n".join(user_set))
print(len(user_set))


