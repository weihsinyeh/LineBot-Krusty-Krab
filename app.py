import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=[
        "user",
        "cancel",
        "about",
        "menu",
        "order_food", "order_name", "order_num", "order_success",
        "weather",
        "address",
        "way_of_eat",
        "bus","ticket",
        "contact",
        "feedback","character","email",
    ],
    transitions=[
        ### Feature1 : about us
        {   "trigger": "advance",   "source": ["way_of_eat","user"],   "dest": "about",    "conditions": "is_going_to_about",  },
        ### Feature2 : menu
        {   "trigger": "advance",   "source": ["way_of_eat","user"],   "dest": "menu",     "conditions": "is_going_to_menu",  },
        ### Feature3 : order
        {   "trigger": "advance",   "source": "user",       "dest": "order_food",   "conditions": "is_going_to_order_food",},
        {   "trigger": "advance",   "source": "order_food", "dest": "order_name",   "conditions": "is_going_to_order_name",},
        {   "trigger": "advance",   "source": "order_name", "dest": "order_num",    "conditions": "is_going_to_order_num",},
        {   "trigger": "advance",   "source": "order_num",  "dest": "order_success","conditions": "is_going_to_order_success",},
        {   "trigger": "advance",   "source": "order_success", "dest": "user",},
        {   "trigger": "go_add_food", "source": "order_success", "dest": "menu"},
        ### cancel
        {   "trigger": "go_cancel", "source": ["order_success", "order_food", "order_name", "order_num"],"dest": "cancel",},
        {   "trigger": "advance",   "source": "user",   "dest": "cancel",   "conditions": "is_going_to_cancel", },
        ### Feature 4 :Address
        {   "trigger": "advance",   "source": "user",   "dest": "address",  "conditions": "is_going_to_address",},
        ### Feature 5 : weather
        {   "trigger": "advance",   "source": "user",   "dest": "weather",  "conditions": "is_going_to_weather",},
        ### Feature 6 : way to eat food
        {   "trigger": "advance",   "source": "user",   "dest": "way_of_eat","conditions": "is_going_to_way_of_eat",},
        ### Feature 7 : bus
        {   "trigger": "advance",   "source": ["way_of_eat","user"],   "dest": "bus",  "conditions": "is_going_to_bus", },
        {   "trigger": "advance",   "source": "bus",    "dest": "ticket",  "conditions": "is_going_to_ticket", },
        {   "trigger": "advance",   "source": "ticket",   "dest": "user", },
        ### Feature 8 : contact
        {   "trigger": "advance",   "source": "user",   "dest": "contact",  "conditions": "is_going_to_contact", },
        ### Feature 9 : feedback
        {   "trigger": "advance",   "source": ["way_of_eat","user"],   "dest": "feedback",  "conditions": "is_going_to_feedback", },
        {   "trigger": "advance",   "source": "feedback",   "dest": "character",  "conditions": "is_going_to_character", },
        {   "trigger": "advance",   "source": "character",   "dest": "email",  "conditions": "is_going_to_email", },
        {   "trigger": "advance",   "source": "email",   "dest": "user", },
        ### go back
        {   "trigger": "go_back",   "source": ["cancel"
                                                "about",
                                                "menu",
                                                "order_food","order_name","order_num","order_success",
                                                "email",
                                                "address",
                                                "weather",
                                                "ticket",
                                                "contact",
                                                "feedback",],"dest": "user",},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)
app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State",TocMachine.hamburgeremoji)

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
