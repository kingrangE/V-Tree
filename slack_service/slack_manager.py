import os
from slack_bolt import App
from slack_actions import SlackActions
from repository.user_repository import UserRepository
from repository.coin_alert_repository import CoinAlertRepository

class SlackManager:
    def __init__(self):
        self.__app = App(
            token=os.getenv("OAUTH_TOKEN"),
            signing_secret=os.getenv("SIGNING_TOKEN")
        )
        self.user_db = UserRepository()
        self.coin_alert_db = CoinAlertRepository()
        self.actions = SlackActions()

