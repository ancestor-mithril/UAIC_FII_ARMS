import csv


from functions import scrap_url_sets, remove_inconsistent_users
from init import url_sets, user_set, init_user_set


def run():
    user_set_csv = "./user_set.csv"
    init_user_set(user_set_csv)

    # scrap_url_sets(url_sets, user_set)  # initial method of getting the most important users
    # by taking the most popular and appreciated comment posters
    # should not be used anymore

    remove_inconsistent_users(user_set)

    print(user_set)

    print("length of user_set:", len(user_set))
    with open(user_set_csv, "w") as fp:
        write = csv.writer(fp)
        write.writerow(user_set)


if __name__ == "__main__":
    run()


