import os
from slack_sdk import WebClient
import json
class SlackActions:
    def __init__(self):
        self.__OAUTH = os.getenv("OAUTH_TOKEN")
        self.client = WebClient(token=self.__OAUTH)
        with open("view.json","r",encoding="utf-8") as f :
            self.data = json.load(f)

    def shortcut_view(self,trigger_id:str,callback_id:str):
        return self.client.views_open(
            trigger_id=trigger_id,
            view=self.data[callback_id]
        )
    
    def send_message_to_user(self,channel:str,user:str)-> None:
        """send message to user(user-only)"""
        self.client.chat_postEphemeral(channel=channel,user=user)

    def send_message_to_channel(self,channel:str,message:str)-> None:
        """send message to channel(all user)"""
        self.client.chat_postMessage(channel=channel,text=message)