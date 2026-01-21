import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import uvicorn

from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from dotenv import load_dotenv

from slack_service.slack_shortcut_manager import SlackShortcutManager
from slack_service.slack_alert_manager import SlackAlertManager

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 실행
    asyncio.create_task(alert_manager.send_alert_loop())
    yield

app = FastAPI(lifespan=lifespan)

# Slack 앱 인스턴스 생성
shortcut_manager = SlackShortcutManager()
alert_manager = SlackAlertManager()
handler = AsyncSlackRequestHandler(shortcut_manager.app)

@app.post("/slack/events")
async def slack_events(request: Request):
    return await handler.handle(request)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6764)
