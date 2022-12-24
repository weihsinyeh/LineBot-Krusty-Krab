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
    MessageAction,
    ImageSendMessage,
    LocationSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    URITemplateAction,
    CarouselTemplate,
    MessageTemplateAction,
    ImageCarouselColumn,
    ImageCarouselTemplate,
    CarouselColumn,
)


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text,emoji):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text,emojis = emoji))

    return "OK"

### show fsm
def send_fsm(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    img  = 'https://i.imgur.com/xGdWMFd.png'
    fsm = ImageSendMessage(
            original_content_url=img,
            preview_image_url=img
        )
    line_bot_api.reply_message(reply_token, fsm)
    return "OK"

def send_feature(reply_token):
    message = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/qTGZ0up.png',
                    title='Order Food For Here or Deliver',
                    text='What would you like to watch?',
                    actions=[
                        MessageTemplateAction( label='What\'s on the menu?', text='menu' ),
                        MessageTemplateAction( label='For Here!!!', text='for here' ),
                        MessageTemplateAction( label='Deliver!!!', text='deliver' )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/i1uHF3i.jpg',
                    title='Find Us or Go to Krusty Krab',
                    text='What would you want to do?',
                    actions=[
                        MessageTemplateAction( label='Know weather!', text='weather' ),
                        MessageTemplateAction( label='Where are we?', text='address' ),
                        MessageTemplateAction( label='Take bus!', text='bus'),
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/1yErAaK.png',
                    title='Contact Us or Know More',
                    text='What would you want to do?',
                    actions=[
                        MessageTemplateAction( label='Show me fsm!', text='show fsm' ),
                        MessageTemplateAction( label='Call to Squidward!', text='contact' ),
                        MessageTemplateAction( label='Give us feedback!', text='feedback' ),
                    ]
                ),
            ]
        )
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)

    return "OK"
### Feature1 : about us
def send_about(reply_token):
    hamburgeremoji = [{"index": 0, "productId": "5ac2211e031a6752fb806d61", "emojiId": "001"},]
    line_bot_api = LineBotApi(channel_access_token)
    text1 =  "$About Krusty Krab\n"
    text1 += "The restaurant was founded by Eugene H. Krabs,\n"
    text1 += "who invented its famous Krabby Patty sandwich.\n"
    text1 += "The Krusty Krab is a prominent fast food restaurant in the underwater city of Bikini Bottom."
    img = "https://i.imgur.com/4dpgMlh.png"
    message = [
        TextSendMessage(text=text1,emojis = hamburgeremoji), 
        ImageSendMessage(  original_content_url=img,preview_image_url=img,),
    ]
    line_bot_api.reply_message(reply_token, message)
    return "OK"

### Feature2 : menu
def send_menu(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    img = "https://i.imgur.com/uMGtgqa.png"
    message = [
        ImageSendMessage(  original_content_url=img, preview_image_url=img,),
        TemplateSendMessage(
            alt_text="Buttons template",
            template=ButtonsTemplate(
                title="Menu!!!",
                text="We have MainFood, Meal and Drink.",
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
    imgs = ["https://i.imgur.com/V0PlZBt.png","https://i.imgur.com/i7oh34p.png","https://i.imgur.com/uETir3s.png"]
    texts = ["$Please enter the number of the Main food you want to order:",
            "$Please enter the number of the Meal you want to order:",
            "$Please enter the number of the Drink you want to order:"]
    line_bot_api = LineBotApi(channel_access_token)
    emoji = [{"index": 0, "productId": "5ac2211e031a6752fb806d61", "emojiId": "001"},]
    message = [
        ImageSendMessage( original_content_url=imgs[index], preview_image_url=imgs[index], ),
        TextSendMessage(text=texts[index], emojis=emoji),  
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
    hamburgeremoji = [{"index": 0, "productId": "5ac2211e031a6752fb806d61", "emojiId": "001"},]
    line_bot_api = LineBotApi(channel_access_token)
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-2198F064-C34A-4066-88EA-48ED62190CE1"
    params = {"Authorization": "CWB-2198F064-C34A-4066-88EA-48ED62190CE1","locationName": "臺南市",}
    response = requests.get(url, params=params)
    print(response.status_code)

    if response.status_code == 200:
        data = json.loads(response.text)
        weather_elements = data["records"]["location"][0]["weatherElement"]
        start_time = weather_elements[0]["time"][0]["startTime"]
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]
        text1 =  "$Bikini Bottom : "+start_time +"\nWeather"+weather_state +"\n"
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
            TextSendMessage(text=text1,emojis = hamburgeremoji),  # 蟹寶王簡介
            TemplateSendMessage(
                alt_text="Buttons template",
                template=ButtonsTemplate(
                    thumbnail_image_url=graph,
                    title="Way Of Eating!!!",
                    text="For here or to Go",
                    actions=[
                        MessageTemplateAction(label="deliver", text="deliver"),
                        MessageTemplateAction(label="for here", text="for here"),
                    ],
                ),
            ),
        ]   
        line_bot_api.reply_message(reply_token, message)
    else:
        print("Can't get data!")
### Feature 6 : way of eating
def send_eathere(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    img = "https://i.imgur.com/44wzquJ.png"
    message = TemplateSendMessage(
            alt_text='ConfirmTemplate',
            template=ButtonsTemplate(
                thumbnail_image_url=img,
                text='Which way do you prefer to go to Krusty Krab?',
                actions=[
                    MessageAction(label='Just Walk', text='walk'),
                    MessageAction(label='Take A Bus',text='bus'),
                ]
            )
        )
    line_bot_api.reply_message(reply_token, message)
    
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
                    text="Know more about us",
                    actions=[
                        MessageTemplateAction(label="Know more about Us", text="about us"),
                        MessageTemplateAction(label="Call to Squidward!", text="contact"),
                        MessageTemplateAction(label="Give us Feedback", text="feedback"),
                    ],
                ),
            ),
        ]   
    line_bot_api.reply_message(reply_token, message)  
### Feature 7 : place
def send_place(reply_token):
    line_bot_api = LineBotApi(channel_access_token)     
    pineapple =  'https://i.imgur.com/ovQiTDM.png'
    stone =      'https://i.imgur.com/1yrXe8l.jpg'
    rock =       'https://i.imgur.com/PEcNGC2.png'
    chumbucket = 'https://i.imgur.com/H331Ywr.png'
    sandyhouse = 'https://i.imgur.com/nKAOYQ4.png'
    Jellyfish=   'https://i.imgur.com/sL1eZDm.png'
    Bank =       'https://i.imgur.com/rHG5giy.png'
    School =     'https://i.imgur.com/LDQW5J8.png'
    KrustyKrab = 'https://i.imgur.com/4dpgMlh.png'
    Image_Carousel = TemplateSendMessage(
    alt_text='目錄 template',
    template=ImageCarouselTemplate(
    columns=[
            ImageCarouselColumn(image_url=KrustyKrab,action=MessageTemplateAction(label='KrustyKrab',text='KrustyKrab',)),
            ImageCarouselColumn(image_url=pineapple,action=MessageTemplateAction(label='pineapple',text='pineapple',)),
            ImageCarouselColumn(image_url=stone,action=MessageTemplateAction(label='stone',text='stone',)),
            ImageCarouselColumn(image_url=rock,action=MessageTemplateAction(label='rock',text='rock',)),
            ImageCarouselColumn(image_url=chumbucket,action=MessageTemplateAction(label='chum bucket',text='chum bucket',)),
            ImageCarouselColumn(image_url=sandyhouse,action=MessageTemplateAction(label='sandy house',text='sandy house',)),
            ImageCarouselColumn(image_url=Jellyfish,action=MessageTemplateAction(label='jellyfish',text='jellyfish',)),
            ImageCarouselColumn(image_url=Bank,action=MessageTemplateAction(label='bank',text='bank',)),
            ImageCarouselColumn(image_url=School,action=MessageTemplateAction(label='school',text='school',)),
        ]
    )
    )
    line_bot_api.reply_message(reply_token,Image_Carousel)
    return 'OK'

def send_ticket(reply_token,index):
    hamburgeremoji = [{"index": 0, "productId": "5ac2211e031a6752fb806d61", "emojiId": "001"},]
    ticket = [[7,5],[10,7],[13,9],[5,3],[8,6],[9,6],[10,7],[15,12],[20,15]]
    text2 = ["$Stop : Pineapple House\nSpongeBob lives here",
                 "$Stop : Squidward Tentacles' house\n:Squidward lives here",
                 "$Stop : Rock House\n:Patrick lives here",
                 "$Stop : Chum Bucket\nThe Chum Bucket is normally unable to compete with the Krusty Krab because it mostly serves awful and foul-tasting foods made from chum, so it rarely gets any customers.",
                 "$Stop : Sandy House\nSandy lives here",
                 "$Stop : Jellyfish Field\nThere are a lot of jellyfish here, and SpongeBob often comes here to collect them.",
                 "$Stop : Bank\nThe bank of Bikini Botton",
                 "$Stop : School\nThe school of Bikini Bottom. Puff teaches here.",
                 "$Stop : Krusty Krab\nThe Krusty Krab is a fast food restaurant located in Bikini Bottom"
                 ]
    text1 = text2[index] + "\nTicket price: " + str(ticket[index][0]) + "\n" + "Time to pass : " + str(ticket[index][1])
    img = "https://i.imgur.com/6rCJ1Ik.png"
    message = [
        ImageSendMessage(original_content_url=img,preview_image_url=img,),
        TextSendMessage(text=text1, emojis=hamburgeremoji), 
    ]
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, message)
    return 'OK'

### Feature 8 : Contact
def send_contact(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    message = TemplateSendMessage(
        alt_text="Call to Squidward!",
        template=ButtonsTemplate(
            thumbnail_image_url="https://i.imgur.com/1yErAaK.png",
            title="Call to Squidward!",
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
    return "OK"




