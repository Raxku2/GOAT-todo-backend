from requests import get, post, Response
from dotenv import load_dotenv
from os import getenv

load_dotenv()
AUTH_API = getenv("FA_AUTH_API")


def verify_auth_token(authToken) -> None | Response:
    res = post(
        url=f"{AUTH_API}/verify",
        json={"authToken": authToken, "authClient": {"additionalProp1": {}}},
    )

    if res.status_code == 200:
        print("Response from verify:", res.json())
        return res

    return None
