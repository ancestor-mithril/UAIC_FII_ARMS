import secrets
from dotenv import load_dotenv
import os
import requests
from urllib.parse import urlencode


load_dotenv()

# TODO: use this: https://gitlab.com/-/snippets/2039434


def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]


code_verifier = code_challenge = get_new_code_verifier()

print(len(code_verifier))
print(code_verifier)
print(os.getenv("CLIENT_ID"))

def step_2():
    base_url_step_2 = "https://myanimelist.net/v1/oauth2/authorize"
    step_2_params = {
        "response_type": "code",
        "client_id": os.getenv("CLIENT_ID"),
        "code_challenge": code_challenge,
        "state": "again"
    }
    # x = requests.get(base_url_step_2, step_2_params)
    print(urlencode(step_2_params))


def step_4():
    code = "def50200b4c56a83f8b2206f64a2a6994b9272bd1123f76d1592189891b66679dbc5b2933faba67a6e349f080c28ccd845ff2204c24538720806c0272f34ab6a5d5adc65066ca27446653239fbaef3b685546e6f93055eb8c4df5eda3195b6cd0c01ef90650705ac35f4bd7c58f9b70daecbc960c8d0a1035e69d152890ec195049497326df401b3fcf46b26f71bcd15b9550b5345c7882c1e0d7d9521c4a0eb23645f72b94fb059c9fd0cf7be90e15a437c2abe9cbc0871352ac0cab7156a44714656d6611e008e614b0a0b763e46d5587612d81eed5b7acbe8ab2ccd61d4cd40e9d49fd3a5a396a3ee8aa5b718a76728e5046e009104119b66eb587691a00cb23f1e3b8aa2a757c1726297d8ba87cf5400d1ef829a51bb965fbb13130da893ae8ce541a2e56f9d79b4f16be34917569f870fbdce75f9d860f62288f9c6905e085f7b3516cecbe633166b105d91b78e2acc89d67f0603f2a8f1cc79172d275aeb96aa7e1b838e055e4d7661fddaa9b69cf95e39aa36b68c57eda42a940ccf66b1264bfde29923b488cf008deea11a19b9e061da534cfbc31f94dd51eb9f46d13992d31f502730429e611ad3256409b79c400699ba48ed0d5fcb8db9d7118be5b0142b6324972eafba61c31ad48a905bad708e06e300e2f416730f6a2214d3b1a4a4c298fe813f316514"
    base_url_step_4 = "https://myanimelist.net/v1/oauth2/token"
    step_4_params = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "code": code,
        "code_verifier": "REFjdeSXJARQEueH1mRPz7l5cmZUOmCBCaokioLh5L6VCTq4YaeN6dg4ezdihV3HwFibF_SkkBEOv_uEWlg9PtBeNxthlvRmrP6tT0_Nq4pMGSfv6sjvuLPPYSAuU_n5",
        "grant_type": "authorization_code"
    }
    # x = requests.post(base_url_step_4, step_4_params)
    # TODO: DEBUG here
    # print(x)


def step_5_refresh():
    base_url_step_5 = "https://myanimelist.net/v1/oauth2/token"
    step_5_params = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "grant_type": "refresh_token",
        "refresh_token": os.getenv("REFRESH_TOKEN")
    }
    x = requests.post(base_url_step_5, step_5_params).json()
    os.putenv("REFRESH_TOKEN", x["refresh_token"])
    os.putenv("ACCESS_TOKEN", x["access_token"])
    with open("new_tokens.json", "w") as fp:
        fp.write(x)

