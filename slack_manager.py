import os
from slack_bolt import App
from slack_actions import SlackActions
import json
class SlackAppManager:
    def __init__(self):        
        self.__app = App(
            token=os.getenv("OAUTH_TOKEN"),
            signing_secret=os.getenv("SIGNING_TOKEN")
        )
        self.actions = SlackActions()
        self._register_callbacks()
    def _register_callbacks(self):
        @self.__app.shortcut("add_user")
        def handle_shortcut(ack, shortcut):
            ack()
            self.actions.shortcut_view(trigger_id=shortcut["trigger_id"],callback_id=shortcut["callback_id"])

        @self.__app.view("add_user")
        def handle_submission(ack, body):
            ack()
            state_values = body["view"]["state"]["values"] 
            member_id = state_values["yR+Jm"]["MemberID"]["value"]
            name = state_values['xmNln']["Name"]["value"]
            
            # 비즈니스 로직 수행
            self.actions.send_message_to_channel("python_test", f"[등록 완료] : {name}({member_id})")

        @self.__app.shortcut("coin_alert")
        def handle_shortcut(ack, shortcut):
            ack()
            self.actions.shortcut_view(trigger_id=shortcut["trigger_id"],callback_id=shortcut["callback_id"])

        @self.__app.view("coin_alert")
        def handle_submission(ack, body):
            ack()
            state_values = body["view"]["state"]["values"]
            ticker = state_values["Coin Ticker"]["dropdown_option"]["selected_option"]["value"]
            price = state_values["7GSPG"]["Price"]["value"]
            
            self.actions.send_message_to_channel("python_test", f"[금액 설정 완료] : {ticker} -> {price}")
        
    def get_app(self):
        return self.__app