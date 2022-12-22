import os

from linebot import LineBotApi, WebhookParser
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    PostbackEvent,
    ImageSendMessage,
    LocationSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    URITemplateAction,
    ConfirmTemplate,
    PostbackTemplateAction,
    MessageTemplateAction,
)


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


##關於我們
def send_about(reply_token):
    line_bot_api = LineBotApi(channel_access_token)

    text1 = """老闆為尤金·H·蟹（蟹老闆）。
    這家餐廳被認為是比奇堡「有史以來為飲食而建立的最好的飲食場所」，
    餐廳的美味蟹堡非常出名。
    """
    message = [
        TextSendMessage(text=text1),  # 蟹寶王簡介
        ImageSendMessage(  # 蟹寶王圖片
            original_content_url="https://upload.wikimedia.org/wikipedia/zh/thumb/3/33/Krusty_Krab_230b.png/170px-Krusty_Krab_230b.png",
            preview_image_url="https://upload.wikimedia.org/wikipedia/zh/thumb/3/33/Krusty_Krab_230b.png/170px-Krusty_Krab_230b.png",
        ),
    ]
    line_bot_api.reply_message(reply_token, message)

    return "OK"


##關於我們
def send_menu(reply_token):
    line_bot_api = LineBotApi(channel_access_token)

    text1 = """蟹寶王的菜單有："""
    message = [
        TextSendMessage(text=text1),  # 蟹寶王簡介
        ImageSendMessage(  # 蟹寶王圖片
            original_content_url="https://i.imgur.com/uMGtgqa.png",
            preview_image_url="https://i.imgur.com/uMGtgqa.png",
        ),
        TemplateSendMessage(
            alt_text="Buttons template",
            template=ButtonsTemplate(
                title="類別!!!",
                text="分為以下主食與飲料:",
                actions=[
                    MessageTemplateAction(label="@主食", text="@主食"),
                    MessageTemplateAction(label="@套餐", text="@套餐"),
                    MessageTemplateAction(label="@飲料", text="@飲料"),
                ],
            ),
        ),
    ]
    line_bot_api.reply_message(reply_token, message)

    return "OK"


### 使用說明
def send_use(reply_token):
    line_bot_api = LineBotApi(channel_access_token)

    text1 = """
1. 「房間預約」及「取消訂房」可預訂及取消訂房。每個 LINE 帳號只能進行一個預約記錄。
2. 「關於我們」對國立成功大學做簡單介紹及旅館圖片。
3. 「位置資料」列出旅館地址，並會顯示地圖。
4. 「聯絡我們」可直接撥打電話與我們聯繫。

輸入「查看功能」即可完成show fsm ，查詢訂房的功能
輸入「show fsm」查看有限狀態機的圖片
輸入「查詢訂房」查看你現在的訂房狀態

輸入「意見回饋 "主旨" "內容"」即可將你的意見打包成email寄給我喔喔!
               """
    message = TextSendMessage(text=text1)
    line_bot_api.reply_message(reply_token, message)

    return "OK"


### 位置資訊
def send_address(reply_token):
    line_bot_api = LineBotApi(channel_access_token)

    text1 = "成功大學店 701台南市東區大學路1號"
    message = [
        TextSendMessage(text=text1),  # 顯示地址
        LocationSendMessage(  # 顯示地圖
            title="成功大學", address=text1, latitude=23.000614, longitude=120.217794
        ),
    ]
    line_bot_api.reply_message(reply_token, message)

    return "OK"


### 聯絡我們
def send_contact(reply_token):
    line_bot_api = LineBotApi(channel_access_token)

    message = TemplateSendMessage(
        alt_text="聯絡我們",
        template=ButtonsTemplate(
            thumbnail_image_url="https://i.imgur.com/tVjKzPH.jpg",
            title="聯絡我們",
            text="打電話給我們",
            actions=[URITemplateAction(label="撥打電話", uri="tel:0123456789")],  # 開啟打電話功能
        ),
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"


### show fsm
def send_fsm(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    fsm = ImageSendMessage(
        original_content_url="https://i.imgur.com/csunAds.png",
        preview_image_url="https://i.imgur.com/csunAds.png",
    )
    line_bot_api.reply_message(reply_token, fsm)
    return "OK"


### show breakfast
def send_breakfast(reply_token):
    line_bot_api = LineBotApi(channel_access_token)

    message = TemplateSendMessage(
        alt_text="Buttons template",
        template=ButtonsTemplate(
            title="最後一問!!!",
            text="飯店有提供早餐，請選擇早餐",
            actions=[
                MessageTemplateAction(label="中式", text="中式"),
                MessageTemplateAction(label="西式", text="西式"),
            ],
        ),
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"


### show lobby
def send_lobby(reply_token):
    line_bot_api = LineBotApi(channel_access_token)

    message = TemplateSendMessage(
        alt_text="Buttons template",
        template=ButtonsTemplate(
            title="其他功能",
            text="知識是光，善良是影",
            actions=[
                MessageTemplateAction(label="show fsm", text="show fsm"),
                MessageTemplateAction(label="查詢訂房", text="查詢訂房"),
            ],
        ),
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"
