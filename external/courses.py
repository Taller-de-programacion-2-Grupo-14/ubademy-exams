import os
import requests


class Courses:
    def __init__(self):
        self.host = os.environ.get("USERS_HOSTNAME")

    def getUser(self, userId: int):
        response = requests.get(f"{self.host}users?id={userId}")
        # f"https://ubademy-14-prod.herokuapp.com/users?id={userId}" 
        # For debugging
        response.raise_for_status()
        return response.json()

    def getBatchUsers(self, userIds: list):
        if not userIds:
            return {}
        response = requests.get(
            f"{self.host}users/batch?ids={','.join(map(str, userIds))}"
        )
        # response = requests.get(
        #     f"https://ubademy-14-prod.herokuapp.com/users/batch?ids=
        # {','.join(map(str, userIds))}"
        # ) # For debugging
        response.raise_for_status()
        return response.json()

# collaborators = [ids, ]
# subscribers = [ids, ]
