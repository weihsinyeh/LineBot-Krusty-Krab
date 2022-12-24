import os
import requests, json, time, statistics  # import statistics 函式庫
from flask import Flask, request
from flask_ngrok import run_with_ngrok
from linebot import WebhookHandler
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
    ImageCarouselColumn,
    ImageCarouselTemplate,
)


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text,emoji):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text,emojis = emoji))

    return "OK"


### Feature1 : about us
def send_about(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    text1 = """The restaurant was founded by Eugene H. Krabs, 
    who invented its famous Krabby Patty sandwich.
    The Krusty Krab is a prominent fast food restaurant in the underwater city of Bikini Bottom.
    """
    img = "https://upload.wikimedia.org/wikipedia/zh/thumb/3/33/Krusty_Krab_230b.png/170px-Krusty_Krab_230b.png"
    message = [
        TextSendMessage(text=text1), 
        ImageSendMessage(  
            original_content_url=img,
            preview_image_url=img,
        ),
    ]
    line_bot_api.reply_message(reply_token, message)
    return "OK"

### Feature2 : menu
def send_menu(reply_token):
    line_bot_api = LineBotApi(channel_access_token)

    message = [
        ImageSendMessage(  # 蟹寶王圖片
            original_content_url="https://i.imgur.com/uMGtgqa.png",
            preview_image_url="https://i.imgur.com/uMGtgqa.png",
        ),
        TemplateSendMessage(
            alt_text="Buttons template",
            template=ButtonsTemplate(
                title="Menu!!!",
                text="We habe MainFood, Meal and Drink.",
                actions=[
                    MessageTemplateAction(label="main food", text="main food"),
                    MessageTemplateAction(label="meal", text="meal"),
                    MessageTemplateAction(label="drink", text="drink"),
                ],
            ),
        ),
    ]
    line_bot_api.reply_message(reply_token, message)

    return "OK"

### Feature3 : order
def send_food(reply_token,index):
    text1=""
    if(index==0):
        img = "https://i.imgur.com/V0PlZBt.png"
        text1 = "$Please enter the number of the Main food you want to order:"
    elif(index==1):
        img = "https://i.imgur.com/i7oh34p.png"
        text1 = "$Please enter the number of the Meal you want to order:"
    elif(index==2):
        img =  "https://i.imgur.com/uETir3s.png"
        text1 = "$Please enter the number of the Drink you want to order:"
    line_bot_api = LineBotApi(channel_access_token)
    emoji = [
        {
            "index": 0, "productId": "5ac2211e031a6752fb806d61", "emojiId": "001"
        },
    ]
    message = [
        ImageSendMessage( original_content_url=img, preview_image_url=img, ),
        TextSendMessage(text=text1, emojis=emoji),  
    ]
    line_bot_api.reply_message(reply_token, message)
    return "OK"

### Feature 4 : address
def send_address(reply_token):
    img = "https://i.imgur.com/WTB6dNt.png"
    line_bot_api = LineBotApi(channel_access_token)
    text1 = "Krusty Krab restaurant"
    message = [ImageSendMessage( original_content_url=img, preview_image_url=img, ),
                LocationSendMessage(  title = "Krusty Krab",  address = text1,  latitude = 23.000614, longitude = 120.217794),]
    line_bot_api.reply_message(reply_token,message)

### Feature 5 : weather  
def send_weather(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-2198F064-C34A-4066-88EA-48ED62190CE1"
    params = {
        "Authorization": "CWB-2198F064-C34A-4066-88EA-48ED62190CE1",
        "locationName": "臺南市",
    }

    response = requests.get(url, params=params)
    print(response.status_code)

    if response.status_code == 200:
        # print(response.text)
        data = json.loads(response.text)
        weather_elements = data["records"]["location"][0]["weatherElement"]
        start_time = weather_elements[0]["time"][0]["startTime"]
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]
        emojis = [
            {"index": 6, "productId": "5ac21542031a6752fb806d55", "emojiId": "001"},
            {"index": 164, "productId": "5ac21d59031a6752fb806d5d", "emojiId": "001"},
        ]
        text1 =  "Bikini Bottom:"+start_time +"\nWeather"+weather_state +"\n"
        text1 += "The Prob Of Rain: "+rain_prob +"\n"
        text1 += "Lowest Temperature: "+min_tem +"\n"
        text1 += "Comfort: "+comfort +"\n"
        text1 += "Highest Temperature: "+max_tem +"\n" 
        graph = ""
        if("雨" in weather_state):
            text1 += "\nThe weather in Bikini Bottom is bad today,you can call delivery!!"
            graph="https://i.redd.it/fq8dqc4p00671.gif"
        else:
            text1 += "\nThe weather in Bikini Bottom is fine today,you can go out to Krusty Krab to enjoy the scenery and delicious meals!"
            graph="https://i.imgur.com/QOJCUmT.png"

        message = [
            TextSendMessage(text=text1,emoji = emojis[1]),  # 蟹寶王簡介
            TemplateSendMessage(
                alt_text="Buttons template",
                template=ButtonsTemplate(
                    thumbnail_image_url=graph,
                    title="Way Of Eating!!!",
                    text="For here or to Go",
                    actions=[
                        MessageTemplateAction(label="deliver", text="deliver"),
                        MessageTemplateAction(label="for here", text="for here"),
                        MessageTemplateAction(label="vehicle", text="vehicle"),
                    ],
                ),
            ),
        ]   
        line_bot_api.reply_message(reply_token, message)
    else:
        print("Can't get data!")
### Feature 6 : way of eating
def send_deliver(reply_token):
    hamburgeremoji = [{"index": 0, "productId": "5ac2211e031a6752fb806d61", "emojiId": "001"},]
    line_bot_api = LineBotApi(channel_access_token)
    text1 = "$Please wait patiently"
    message = [
            TextSendMessage(text=text1, emojis=hamburgeremoji), 
            TemplateSendMessage(
                alt_text="Buttons template",
                template=ButtonsTemplate(
                    thumbnail_image_url= "https://i.imgur.com/polyRYa.png",
                    title="Kill time!!!",
                    text="Video or Audio",
                    actions=[
                        MessageTemplateAction(label="video", text="video"),
                        MessageTemplateAction(label="audio", text="audio"),
                        MessageTemplateAction(label="feedback", text="feedback"),
                    ],
                ),
            ),
        ]   
    line_bot_api.reply_message(reply_token, message)  
### Feature 7 : Vehicle
def send_vehicle(reply_token):
    line_bot_api = LineBotApi(channel_access_token)     
    KrustyKruiser = 'https://static.wikia.nocookie.net/spongebob/images/9/98/The_Krusty_Kruiser.png'
    Pineapple = 'https://static.wikia.nocookie.net/spongebob/images/4/45/Pineapple_RV_119.png'
    JellyAngler = 'https://static.wikia.nocookie.net/spongebob/images/9/9f/The_Jelly_Life_195.png'
    Bus = 'https://static.wikia.nocookie.net/spongebob/images/1/1f/Bus_stock_art.png'
    PattyWagon = 'https://static.wikia.nocookie.net/spongebob/images/2/2c/The_Wagon.png'
    Unicycle='https://static.wikia.nocookie.net/spongebob/images/7/76/SpongeBob-unicycle-promo.png'
    ShellCart = 'https://static.wikia.nocookie.net/spongebob/images/e/e4/Paper14.png'
    MobileKrustyKrab = 'https://static.wikia.nocookie.net/spongebob/images/2/29/20%2C000_Patties_Under_the_Sea_072.png'
    KrustySpongeFunTrain = 'https://static.wikia.nocookie.net/spongebob/images/4/4e/Train1_Stitch_Stitch.jpg'
    Image_Carousel = TemplateSendMessage(
    alt_text='目錄 template',
    template=ImageCarouselTemplate(
    columns=[
            ImageCarouselColumn(image_url=KrustyKruiser,action=MessageTemplateAction(label='Food truck',text='Food truck',)),
            ImageCarouselColumn(image_url=Pineapple,action=MessageTemplateAction(label='Pine apple',text='Pine apple',)),
            ImageCarouselColumn(image_url=JellyAngler,action=MessageTemplateAction(label='JellyAngler',text='JellyAngler',)),
            ImageCarouselColumn(image_url=Bus,action=MessageTemplateAction(label='Bus',text='Bus',)),
            ImageCarouselColumn(image_url=PattyWagon,action=MessageTemplateAction(label='PattyWagon',text='PattyWagon',)),
            ImageCarouselColumn(image_url=Unicycle,action=MessageTemplateAction(label='Unicycle',text='Unicycle',)),
            ImageCarouselColumn(image_url=MobileKrustyKrab,action=MessageTemplateAction(label='KrustyKrab',text='KrustyKrab',)),
            ImageCarouselColumn(image_url=KrustySpongeFunTrain,action=MessageTemplateAction(label='Train',text='Train',)),
            ImageCarouselColumn(image_url=ShellCart,action=MessageTemplateAction(label='ShellCart',text='ShellCart',)),
        ]
    )
    )
    line_bot_api.reply_message(reply_token,Image_Carousel)
    return 'OK'

### Feature 8 : Contact
def send_contact(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text="Contact us",
        template=ButtonsTemplate(
            thumbnail_image_url="https://i.imgur.com/tVjKzPH.jpg",
            title="Contact us",
            text="0912345678",
            actions=[URITemplateAction(label="Call", uri="tel:0123456789")],  # 開啟打電話功能
        ),
    )
    line_bot_api.reply_message(reply_token, message)
    return "OK"

### Feature 9 : Feedback
def send_feedback(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    Spongebob = 'https://i.imgur.com/tUfbHba.png'
    Squidward = 'https://i.imgur.com/c9Vkeys.jpg'
    Crab = 'https://i.imgur.com/ODsRvPc.png'
    Patrick = 'https://i.imgur.com/KVVXhCv.png'
    Image_Carousel = TemplateSendMessage(
    alt_text='目錄 template',
    template=ImageCarouselTemplate(
        columns=[
            ImageCarouselColumn(image_url=Spongebob,action=MessageTemplateAction(label='fry cook',text='fry cook',)),
            ImageCarouselColumn(image_url=Squidward,action=MessageTemplateAction(label='cashier',text='cashier',)),
            ImageCarouselColumn(image_url=Crab,action=MessageTemplateAction(label='boss',text='boss',)),
            ImageCarouselColumn(image_url=Patrick,action=MessageTemplateAction(label='delivery man',text='delivery man',)),
            ]
        )
    )
    line_bot_api.reply_message(reply_token,Image_Carousel)

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

