from typing import List
import requests
from model.User import User


def fetch_users() -> List[User]:
    response = requests.get("https://randomuser.me/api?results=4")
    data = response.json()
    users = []
    for user_data in data['results']:
        user = User(
            first=user_data['name']['first'],
            last=user_data['name']['last'],
            email=user_data['email']
        )
        users.append(user)
    return users
