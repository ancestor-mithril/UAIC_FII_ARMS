from prediction_functions import init_anime_model, init_anime_dict, create_preference_dict, predict_anime_for_user


def run():
    try:
        user = input("Check prediction for user: ")
        print(*predict_anime_for_user(user), sep="\n")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    run()