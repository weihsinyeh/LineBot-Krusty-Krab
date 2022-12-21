from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    state = "user"
    new_order_name = ""
    new_order_number = 0
    order_name_list = []
    order_number_list = []
    money = 0
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_cancel(self, event):
        text = event.message.text
        return text.lower() == "@取消"

    def is_going_to_order_food(self, event):
        text = event.message.text
        return text.lower() == "@餐點預訂"

    ### 訂餐流程
    def is_going_to_order_name(self, event):
        text = event.message.text
        return True
    def is_going_to_order_num(self, event):
        text = event.message.text
        return True
    def is_going_to_order_success(self, event):
        text = event.message.text
        return True

    ### 餐點預定
    def on_enter_order_food(self, event):# 顯示菜單
        print("開始 order_food")
        TocMachine.state = "order_food"  # 設定狀態
        reply_token = event.reply_token  # 取得回覆用的token
        send_text_message(reply_token, "菜單:\n"
                                       "蟹堡-----------------------價格\n"
                                       "1.Krabby patty       (單層) 10$\n"
                                       "2.w\sea chaasa(加海草醬)    15$\n"
                                       "3.double krabby patty(雙層) 15$\n"
                                       "4.w\sea chaasa(加海草醬)    20$\n"
                                       "5.triple krabby patty(三層) 20$\n"
                                       "6.w\sea chaasa(加海草醬)    25$\n"
                                       "請輸入餐點編號:")
    def on_enter_order_name(self, event):      # 輸入餐點名稱
        print("進入 order_name")
        TocMachine.state="order_name"
        TocMachine.new_order_name = event.message.text
        reply_token = event.reply_token
        send_text_message(reply_token, "你點了"+TocMachine.new_order_name+"號蟹堡\n"
                                       "請輸入數量:\n"
                                       "(如欲取消請輸入 @取消)")

    def on_enter_order_num(self, event):       # 輸入餐點數量
        print("進入 order_num")
        TocMachine.state="order_num"
        reply_token = event.reply_token
        if  event.message.text != "@取消":
            TocMachine.new_order_number =event.message.text 
            send_text_message(reply_token, "你點了"+TocMachine.new_order_name+"號餐點"+TocMachine.new_order_number+"份\n"
                                           "(如欲取消請輸入 @取消)")

        elif event.message.text == "@取消":
            self.go_cancel(event)
        else:
            self.on_enter_cancel(self,event)

    def on_enter_order_success(self, event):
        print("I'm entering order_success")
        TocMachine.state="order_success"
        reply_token = event.reply_token
        text = "你點了"
        
        if event.message.text != "@取消":
            TocMachine.order_name_list.append(TocMachine.new_order_name)
            TocMachine.order_number_list.append(TocMachine.new_order_number)
            for i in range(len(TocMachine.order_name_list)):
                text += TocMachine.order_name_list[i]+"號餐點"+TocMachine.order_number_list[i]+"份\n"
                send_text_message(reply_token, "訂餐成功，以下是您目前的訂單:\n"+text)
            self.go_back()
        else:
            self.go_cancel(event)

    def on_enter_cancel(self, event):
        print("I'm entering cancel")
        reply_token = event.reply_token
        TocMachine.state="cancel"
        send_text_message(reply_token,"親愛的顧客您已經取消訂餐")
        self.go_back()


