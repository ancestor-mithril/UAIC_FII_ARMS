from functions import get_friends
import random
import time

with open("test_friends.txt", "r") as a_file:
    sets=set()
    for line in a_file:
        stripped_line = line.strip()
        sets.update(get_friends(stripped_line))
        with open('test2.txt', 'w') as filehandle:
            for listitem in sets:
                filehandle.write('%s\n' % listitem)
        sleep_interval = random.randint(10, 30)
        time.sleep(sleep_interval)
        print(len(sets))
