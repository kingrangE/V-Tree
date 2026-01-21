import os
from slack_bolt.async_app import AsyncApp
from slack_service.slack_actions import SlackActions
from repository.user_repository import UserRepository
from repository.coin_alert_repository import CoinAlertRepository

class SlackManager:
    def __init__(self):
        self.__app = AsyncApp(
            token=os.getenv("OAUTH_TOKEN"),
            signing_secret=os.getenv("SIGNING_TOKEN")
        )
        self.user_db = UserRepository()
        self.coin_alert_db = CoinAlertRepository()
        self.actions = SlackActions()

    @property
    def app(self):
        return self.__app

