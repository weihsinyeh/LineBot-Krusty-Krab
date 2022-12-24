from transitions.extensions import GraphMachine
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

from utils import (send_menu,
                    send_deliver,send_feedback,
                    send_contact,send_text_message,send_about,send_fsm,send_lobby,send_weather,send_address,send_vehicle,send_food,)
from emailweihsin import send_email
class TocMachine(GraphMachine):
    new_order_index = 0
    new_order_number = 0
    order_menu_list = []
    order_name_list = []
    order_number_list = []
    money = 0
    menuindex = 0
    feedbackreceiver = ""
    menu = [[["Krabby patty",10], ["Krabby patty(w\sea chaasa)",15], ["Double krabby patty", 15], ["Double krabby patty(w\sea chaasa)", 20], ["Triple krabby patty",20], ["Triple krabby patty(w\sea chaasa)",25]],
            [["Kelp rings", 15], ["Salty sauce", 5], ["Krabby meal", 20], ["Double krabby meal", 25], ["Triple krabby meal", 30], ["Salty sea dog", 15],["Footlong",25],["Sailors surprise",25],["Golden loaf",10],["Golden loaf (wsauce)",15]],
            [["Kelp shake",20],["Seafoam soda(small)",5],["Seafoam soda(medium)",10],["Seafoam soda(large)",15]]]
    hamburgeremoji = [{"index": 0, "productId": "5ac2211e031a6752fb806d61", "emojiId": "001"},]
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    ### Cancel
    def is_going_to_cancel(self, event):
        text = event.message.text
        return text.lower() == "cancel"

    ### Feature1 : about us
    def is_going_to_about(self, event):
        text = event.message.text
        return text.lower() == "about us"

    ### Feature2 : menu
    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "menu" or text.lower() == "order" or text.lower() == "order"

    ### Feature3 : order
    def is_going_to_order_food(self, event):
        text = event.message.text
        global menuindex
        if(text.lower() == "main food"): menuindex = 0
        elif(text.lower() == "meal"): menuindex = 1
        elif(text.lower() == "drink"): menuindex = 2
        return text.lower() == "main food" or text.lower() == "meal" or text.lower() == "drink"

    def is_going_to_order_name(self, event):
        text = event.message.text
        return True

    def is_going_to_order_num(self, event):
        text = event.message.text
        return True

    def is_going_to_order_success(self, event):
        text = event.message.text
        return True

    ### Feature 4 :Address
    def is_going_to_address(self, event):
        text = event.message.text
        return text.lower() == "address"

    ### Feature 5 : weather
    def is_going_to_weather(self, event):
        text = event.message.text
        return text.lower() == "weather"

    ### Feature 6 : way to eat food
    def is_going_to_way_of_eat(self, event):
        text = event.message.text
        return text.lower() == "for here" or text.lower() == "deliver"

    ### Feature 7 : Vehicle
    def is_going_to_vehicle(self, event):
        text = event.message.text
        return text.lower() == "vehicle"

    def is_goint_to_vehicle_detail(self,event):
        text = event.message.text
        return text.lower() == "Food trunk"

    ### Feature 8 : Contact
    def is_going_to_contact(self, event):
        text = event.message.text
        return text.lower() == "contact"
    ### Feature 9 : Feedback
    def is_going_to_feedback(self, event):
        text = event.message.text
        return text.lower() == "feedback"
    def is_going_to_character(self, event):
        text = event.message.text
        return True
    def is_going_to_email(self, event):
        text = event.message.text
        return True

    ### Cancel
    def on_enter_cancel(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "$Dear customer, you have canceled the order",TocMachine.hamburgeremoji)
        self.go_back()

    ### Feature1 : about us
    def on_enter_about(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "$About Krabby Patty",TocMachine.hamburgeremoji)
        send_about(reply_token)
        self.go_back()

    ### Feature2 : menu
    def on_enter_menu(self, event):
        reply_token = event.reply_token
        send_menu(reply_token)
        self.go_back()

    ### Feature 3 : Order Food (show the detail of the menu)
    def on_enter_order_food(self, event):  
        print("start order food")
        reply_token = event.reply_token  
        global menuindex
        if menuindex == 0:
            send_food(reply_token, 0)
        elif menuindex == 1:
            send_food(reply_token, 1)
        elif menuindex == 2:
            send_food(reply_token, 2)

    def on_enter_order_name(self, event):  # 輸入餐點名稱
        menu = TocMachine.menu
        TocMachine.new_order_index = int(event.message.text) - 1
        reply_token = event.reply_token
        send_text_message( reply_token, "$You have ordered" + menu[menuindex][TocMachine.new_order_index][0] + \
                            "\nPlease input number:\n" "(If you want to cancel, input \"cancel\")",TocMachine.hamburgeremoji)

    def on_enter_order_num(self, event):  # 輸入餐點數量
        menu = TocMachine.menu
        reply_token = event.reply_token
        if event.message.text != "cancel":
            TocMachine.new_order_number = event.message.text
            send_text_message(
                reply_token,
                "$You have ordered\n"
                + TocMachine.new_order_number + " "+ menu[menuindex][TocMachine.new_order_index][0] \
                + "\n(If you are sure, input \"sure\")\n"
                + "(If you want to cancel, input \"cancel\")\n"
                + "((If you want to order more, input \"order more\")\n",TocMachine.hamburgeremoji
            )
        elif event.message.text == "cancel":
            self.go_cancel(event)

    def on_enter_order_success(self, event):
        menu = TocMachine.menu
        reply_token = event.reply_token
        text = ""
        if event.message.text == "sure":
            TocMachine.order_menu_list.append(menuindex)
            TocMachine.order_name_list.append(TocMachine.new_order_index)
            TocMachine.order_number_list.append(TocMachine.new_order_number)
            for i in range(len(TocMachine.order_name_list)):
                pay = TocMachine.menu[TocMachine.order_menu_list[i]][int(TocMachine.order_name_list[i])][1] * int(TocMachine.order_number_list[i])
                text += (
                    menu[TocMachine.order_menu_list[i]][TocMachine.order_name_list[i]][0]
                    + " : "
                    + str(TocMachine.order_number_list[i])
                    + " $" + str(pay) + "\n"
                )
                TocMachine.money += pay
            send_text_message(reply_token, "$Order Success!\nThe following is your current order:\n" + text,TocMachine.hamburgeremoji)
            self.go_back()
        elif event.message.text == "order more":
            TocMachine.order_menu_list.append(menuindex)
            TocMachine.order_name_list.append(TocMachine.new_order_index)
            TocMachine.order_number_list.append(TocMachine.new_order_number)
            self.go_add_food(event)
        elif event.message.text == "cancel":
            self.go_cancel(event)
    ### Feature 3 : Order Food (show the detail of the menu)

    ### Feature 4 : address
    def on_enter_address(self, event):
        reply_token = event.reply_token
        send_address(reply_token)
        self.go_back()

    ### Feature 5 : weather       
    def on_enter_weather(self, event):
        reply_token = event.reply_token
        send_weather(reply_token)
        self.go_back()
  
    ### Feature 6 : way to eat food
    def on_enter_way_of_eat(self, event):
        reply_token = event.reply_token
        if(event.message.text == "for here"):
            send_text_message(reply_token, "$You have chosen to eat here",TocMachine.hamburgeremoji)
        elif(event.message.text == "deliver"):
            if(TocMachine.money == 0):
                send_text_message(reply_token, "$You have to order food!",TocMachine.hamburgeremoji)
            else:
                send_deliver(reply_token)
        self.go_back()

    ### Feature 7 : vehicle
    def on_enter_vehicle(self, event):  
        reply_token = event.reply_token
        send_vehicle(reply_token)
        self.go_back()
        
    ### Feature 8 : contact
    def on_enter_contact(self, event):
        reply_token = event.reply_token
        send_contact(reply_token)
        self.go_back()

    ### Feature 9 : feedback
    def on_enter_feedback(self, event):
        reply_token = event.reply_token
        send_feedback(reply_token)

    def on_enter_character(self, event):
        reply_token = event.reply_token
        text = ""
        if event.message.text == "fry cook":
            text += "$Spongebob works as a fry cook at the Krusty Krab, a job which he is exceptionally skilled at and enjoys thoroughly. "
            TocMachine.feedbackreceiver = "Spongebob"
        elif event.message.text == "delivery man":
            text += "$Patrick works as a delivery man at the Krusty Krab, a job which he send food to customers personally."
            TocMachine.feedbackreceiver = "Patrick"
        elif event.message.text == "cashier":
            text += "$Squidward works as a cashier at the Krusty Krab, a job which he is not good at and hates it."
            TocMachine.feedbackreceiver = "Squidward"
        elif event.message.text == "boss":
            text += "$Mr. crab works as a boss at the Krusty Krab, a job which he is good at and enjoys it."
            TocMachine.feedbackreceiver = "Mr. crab"
        text += "\nInput your feedback to "+TocMachine.feedbackreceiver+"!!!"
        send_text_message(reply_token, text,TocMachine.hamburgeremoji)

    def on_enter_email(self, event):
        print("email")
        reply_token = event.reply_token
        print(event.message.text)
        text1 = event.message.text
        send_email(TocMachine.feedbackreceiver,text1,reply_token)
        self.go_back()