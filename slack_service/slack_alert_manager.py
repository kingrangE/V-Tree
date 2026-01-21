import asyncio
from slack_service.slack_manager import SlackManager
from coin_service import CoinService
from time import time
from datetime import datetime

class SlackAlertManager(SlackManager):
    def __init__(self):
        super().__init__()
        self.coin_service = CoinService()
        self.coin_symbols = self.coin_alert_db.get_coins_symbols()

    async def send_alert_loop(self):
        while True:
            self.users_condition = self.coin_alert_db.get_all_conditions()
            try:
                if not self.users_condition:
                    await asyncio.sleep(1)
                    continue

                # 실시간 코인 가격 조회
                self.coin_prices = self.coin_service.get_prices(self.coin_symbols)
                now = time()

                for condition in self.users_condition:
                    ticker = condition['ticker']
                    target_price = condition['price']
                    # 필드가 없을 경우 None 반환
                    last_triggered = condition.get('last_triggered',None)

                    # 1시간 이내에 알람이 갔다면 무시
                    if last_triggered and now - last_triggered < 3600:
                        continue

                    current_price = self.coin_prices.get(ticker)
                    
                    # 조건 달성시, 알림 발송
                    if current_price and int(current_price) == int(target_price):
                        message = f"[Alert]({datetime.now().strftime('%d일 %H:%M:%S')}) 조건 만족 : {ticker} / 목표가: {target_price} (현재가: {current_price})"
                        await self.actions.send_message_to_user(member_id=condition['member_id'], message=message)
                        
                        # 알림 전송 시 시간 기록
                        self.coin_alert_db.update_last_triggered(
                            member_id=condition['member_id'], 
                            id=condition['_id'], 
                            timestamp=now
                        )
                
            except Exception as e:
                print(f"[Error](SlackAlertManager-send_alert_loop {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) : {e}")
            
            await asyncio.sleep(1) # 1초 대기
