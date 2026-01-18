"""
slack 메시지 전송 및 modal view 
"""

import os
from slack_sdk import WebClient
import json
class SlackActions:
    def __init__(self):
        self.__OAUTH = os.getenv("OAUTH_TOKEN")
        self.client = WebClient(token=self.__OAUTH)
        with open("view.json","r",encoding="utf-8") as f :
            self.data = json.load(f)

    def shortcut_view(self,trigger_id:str,callback_id:str,multi_select_list:list = None):
        if multi_select_list : 
            # For using multi-select function
            self.data[callback_id]["blocks"][0]["element"]["options"] = multi_select_list
            
        return self.client.views_open(
            trigger_id=trigger_id,
            view=self.data[callback_id]
        )
    def show_alert_view(self, trigger_id:str, title:str, message:str):
        view_payload = {
            "type": "modal",
            "callback_id": "alert_view", 
            "title": {"type": "plain_text", "text": title},
            "submit": {"type": "plain_text", "text": "확인"}, 
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                }
            ]
        }
        return self.client.views_open(trigger_id=trigger_id, view=view_payload)
    def send_message_to_user(self,memeber_id:str,message:str)-> None:
        """send message to user(user-only)"""
        self.client.chat_postMessage(channel=memeber_id,text=message)

    def send_message_to_channel(self,channel:str,message:str)-> None:
        """send message to channel(all user)"""
        self.client.chat_postMessage(channel=channel,text=message)