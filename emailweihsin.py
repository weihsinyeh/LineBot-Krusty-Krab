import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from utils import send_text_message

gmail_password = os.getenv("GMAIL_PASSWORD", None)
port = os.environ.get("PORT", 8000)

def send_email(feature_name,description,reply_token):

    content = MIMEMultipart()
    print("complete")    
    content['subject'] = 'FeedBack of Krusty-Krab'                        
    content['from'] = 'weihsinyeh168@gmail.com'                                    # 寄件者
    content['to'] = 'f74109016@gs.ncku.edu.tw'                         # 收件者
    content.attach(MIMEText(f'{feature_name}\n\n{description}'))  # 內容
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:  # 設定SMTP伺服器
        try:
            print("complete")    
            smtp.ehlo()
            print("complete")                                            # 驗證SMTP伺服器
            smtp.starttls()
            print("complete")                                        # 建立加密傳輸
            smtp.login('weihsinyeh168@gmail.com', gmail_password)  # 登入寄件者gmail
            print("complete")
            smtp.send_message(content)  
            print("complete")                           # 寄送郵件
            send_text_message(reply_token, 'We have recive your feedback!\U0001f914')
        except Exception as e:
            send_text_message(reply_token, 'Sorry we do not recive your feedback')