from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv
from slack_manager import SlackAppManager
load_dotenv()

flask_app = Flask(__name__)
# Slack 앱 인스턴스 생성
slack_manager = SlackAppManager()
handler = SlackRequestHandler(slack_manager.get_app())


@flask_app.route("/slack/events", methods=['POST'])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(port=6764)