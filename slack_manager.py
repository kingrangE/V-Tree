import os
from slack_bolt import App
from slack_actions import SlackActions
from datetime import datetime
from repository.user_repository import UserRepository
from repository.coin_alert_repository import CoinAlertRepository
from typing import Optional

class SlackAppManager:
    def __init__(self):        
        self.__app = App(
            token=os.getenv("OAUTH_TOKEN"),
            signing_secret=os.getenv("SIGNING_TOKEN")
        )
        self.user_db = UserRepository()
        self.coin_alert_db = CoinAlertRepository()
        self.actions = SlackActions()
        self._register_callbacks()
    def _register_callbacks(self):
        # 알림 설정
        @self.__app.shortcut("coin_alert")
        def handle_coin_alert_shortcut(ack, shortcut):
            ack()
            self.actions.shortcut_view(trigger_id=shortcut["trigger_id"],callback_id=shortcut["callback_id"])

        #특정 알림 삭제
        @self.__app.shortcut("delete_coin_alert")
        def handle_delete_coin_alert_shortcut(ack, shortcut):
            ack()
            options = []
            member_id=shortcut["user"]["id"]
            current_conditions=list(self.coin_alert_db.get_user_condition(member_id=member_id))
            
            # 유저가 첫 이용이면 모달창 XX
            if self.__is_first(member_id= member_id, trigger_id= shortcut['trigger_id']): return 
            # 존재하지 않으면 모달창 XX
            if not self.__is_exist(current_conditions= current_conditions, trigger_id= shortcut['trigger_id']) : return
            
            for result in current_conditions:
                options.append({
                    "text" : {
                        "type" : "plain_text",
                        "text" : f"{result['ticker']} / {result['price']}",
                    },
                    "value" : f"{result['_id']}"
                })

            self.actions.shortcut_view(trigger_id=shortcut["trigger_id"],callback_id=shortcut["callback_id"],multi_select_list=options)
        
        # 전체 알림 삭제
        @self.__app.shortcut("delete_all_coin")
        def handle_delete_all_coin_shortcut(ack, shortcut):
            ack()
            member_id=shortcut["user"]["id"]
            current_conditions=self.coin_alert_db.get_user_condition(member_id=member_id)
            
            # 유저가 첫 이용이면 모달창 XX
            if self.__is_first(member_id= member_id, trigger_id= shortcut['trigger_id']): return 
            # 존재하지 않으면 모달창 XX
            if not self.__is_exist(current_conditions= current_conditions,trigger_id= shortcut['trigger_id']) : return
            
            self.actions.shortcut_view(trigger_id=shortcut["trigger_id"],callback_id=shortcut["callback_id"])

        @self.__app.view("coin_alert")
        def handle_coin_alert_submission(ack, body):
            ack()
            # body 파싱
            state_values = body["view"]["state"]["values"]
            member_id = body["user"]["id"]
            user_name = body["user"]["username"]
            ticker = state_values["Coin Ticker"]["dropdown_option"]["selected_option"]["value"]

            # 금액 자료형 변환
            try :
                price = int(state_values["7GSPG"]["Price"]["value"])
            except :
                self.actions.send_message_to_user(channel="python_test",user=member_id, message=f"[ERROR] : 금액은 숫자만 입력하셔야 합니다. (ex,1234567)")
                return # 함수 종료
            
            # 알림 삽입
            self.coin_alert_db.insert_user_condition(ticker=ticker,member_id=member_id,price=price)

            # 유저 정보 없으면 유저 정보 삽입
            if not (self.user_db.find_user(member_id=member_id)) : # 없는 경우
                    self.user_db.insert_user(name=user_name,member_id=member_id)
                
            self.__alert_view(trigger_id=body["trigger_id"],title="금액 설정 완료",message=f"{ticker}이 {price}에 알림이 전송됩니다.")
            self.actions.send_message_to_channel(channel=member_id,message=f"[금액 설정 완료] : {ticker} -> {price}")
        
        @self.__app.view("delete_coin_alert")
        def handle_delete_coin_alert_submission(ack, body):
            ack()
            # body 파싱
            state_values = body["view"]["state"]["values"]
            ids = [value["value"] for value in state_values["delete_block"]["delete_list"]["selected_options"]]
            
            member_id = body["user"]["id"]
            
            if self.coin_alert_db.delete_all_with_ids(member_id= member_id, ids= ids) :
                self.__alert_view(trigger_id=body["trigger_id"],title="알림 선택 삭제 완료",message=f"선택하신 알림이 모두 삭제 되었습니다.")
                self.actions.send_message_to_user(memeber_id= member_id, message= "모두 삭제가 완료되었습니다.")
            else : 
                self.__alert_view(trigger_id=body["trigger_id"],title="알림 선택 삭제 오류",message=f"알림 삭제가 완료되지 못했습니다.")
                self.actions.send_message_to_user(memeber_id= member_id, message= "알 수 없는 이유로 삭제가 완료되지 못했습니다. 관리자에게 닉네임과 함께 문의해주십시오.")
        
        @self.__app.view("delete_all_coin")
        def handle_delete_all_coin_submission(ack, body):
            ack()
            member_id = body["user"]["id"]
            
            if self.coin_alert_db.delete_all_bulk(member_id= member_id) :
                self.__alert_view(trigger_id=body["trigger_id"],title="알림 선택 삭제 완료",message=f"선택하신 알림이 모두 삭제 되었습니다.")
                self.actions.send_message_to_user(memeber_id= member_id, message= "모두 삭제가 완료되었습니다.")
            else : 
                self.__alert_view(trigger_id=body["trigger_id"],title="알림 선택 삭제 오류",message=f"알림 삭제가 완료되지 못했습니다.")
                self.actions.send_message_to_user(memeber_id= member_id, message= "알 수 없는 이유로 삭제가 완료되지 못했습니다. 관리자에게 닉네임과 함께 문의해주십시오.")
        
        @self.__app.view("alert_view")
        def handle_alert_view_submission(ack, body):
            ack() 

    def __alert_view(self,trigger_id:str, title:str, message:str)->None:
        self.actions.show_alert_view(
                trigger_id=trigger_id,
                title=title,
                message=message,
            )

    def __is_first(self,member_id,trigger_id):
        if not self.user_db.find_user(member_id=member_id):
            # 유저가 한 번도 이용하지 않았다면
            self.actions.show_alert_view(
                trigger_id=trigger_id,
                title="이용 기록 오류",
                message="알림 설정 기록이 없습니다."
            )
            return True
        return False
    
    def __is_exist(self,current_conditions:Optional[list],trigger_id:str):
        if current_conditions :
                return True
        else:
            self.actions.show_alert_view(
                trigger_id=trigger_id,
                title="비어있는 알림",
                message="설정된 알림이 0개입니다."
            )
            return False
    def get_app(self):
        return self.__app