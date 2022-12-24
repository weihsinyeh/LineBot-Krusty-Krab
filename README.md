# LineBot-Krusty-Krab 
###### tags: `計算理論`
##### Theory Of Computing
##### F74109016 資訊工程系大三 葉惟欣
![](https://i.imgur.com/Y4cyo05.png)
> :hamburger: The LineBot-Krusty-Krab with 9 features!
1. About us
2. See Menu
3. Order Food
4. Weather information (web scraping)
5. Choose way to go to Krusty-Krab
6. FeedBack send to us by email(SMTP)
7. Take a Bus
8. Contact to us
9. Find the address of Krusty-Krab

Button carousel templates are designed and implemented in every feature. Instead of directly typing the commands to the LINE bot, users can just simply press buttons on the carousel template to browse the features and access the NBA information!

There are four main componenets in this project

* LINE Bot: Built by the official LINE Messaging API
* Web Scraping: Use function "get" of Requests Library to scrape json url of 氣象資料開放平台.
    Then use way of dictionary to retrieve weather information
* SMTP : Customer can use Feature Feedback to send email to Krusty-Krab
* FSM: Create FSMs with pytransitions for the users state management

---
## FSM
### The Graph of LineBot-Krusty-Krab Finite State Machine

![](https://i.imgur.com/xGdWMFd.png)


Finite State Machine is implemented for the state management of the users. A FSM is maintained for each individual user. This way, every user has their own independent state, and the operations between two different users will not affect each other.

Finite state machine is a model in Theory of Computation. This model is implemented in Daily-NBA. Each feature is represented by a state, and the button that user pressed on the carousel template will trigger the transitions between states. The FSM graph is drawn by GraphMachine in [transitions.extensions](https://github.com/pytransitions/transitions).
### Operations
After input ==**"show fsm"**== you can see the **graph of finite state machine**
![](https://i.imgur.com/Is8D139.png)


---
## Show Feature menu
### Operations
1. After input ==**"feature"**== we can see the all feature of LineBot-Krusty-Krab 
![](https://i.imgur.com/Y4cyo05.png)
### Function
Guide the customer how to use the line bot properly. 

---
## Feature 1 : About Us
### Operations
1. After input ==**"about us"**== we can see the detail of Krusty-Krab 
![](https://i.imgur.com/0W73tDW.png)
### Function
Show the Menu and Guide the customer to choice ==**"main food"**==, ==**"meal"**==, ==**"drink"**==

---
## Feature 2 : Show Menu
### Operations
1. After input ==**"menu"**== then we can show the menu of Krabby Krab for customer to see 
2. Then you can click ==**"main food"**== ,==**"meal"**== ,==**"drink"**== or just input it.
3. After the operation mentioned above we will enter the order state
![](https://i.imgur.com/FUgoV3R.png)

---
## Feature 3 : Order Food
### Operations
1. After input ==**"main food"**== we will see the detail of the main food
2. Then you just input the number of main food you want to order **(ex:"5" as follewed)**
3. Then input the number of the food you want to order **(ex:"3" as follewed)**
![](https://i.imgur.com/ZLNn6SQ.png)

4. After the operation aboved, we have three choice ==**"sure"**== ,==**"cancel"**==, ==**"order more"**==
    #### case1 : =="sure"==
    show the name of what you order and the total you need to pay 
    ![](https://i.imgur.com/hnXNSZ3.png)

    #### case2 : =="cancel"==
    Just return to the initial state and you can input any request.
    ![](https://i.imgur.com/JCN1dQz.png)

    #### case3 : =="order more"==
    1. show the menu again and you can click ==**"main food"**== ,==**"meal"**== ,==**"drink"**== or just input it.
    2. Back to the step 1.
    ![](https://i.imgur.com/lwv9AHB.png)
    ![](https://i.imgur.com/hhZmuhJ.png)
    3. After you click ==**"sure"**== or input it, then we will show the name of what you order and the total you need to pay.
      
:::info
:hamburger:Order Success!
The following is your current order:
Triple krabby patty : 3 $60
Seafoam soda(large) : 2 $30
Total : $90
:::

![](https://i.imgur.com/WZv7Oo2.png)

---
## Feature 4 : Weather report to you
**Technique : web crawler**

* Data source : 氣象資料開放平台 - https://opendata.cwb.gov.tw/dataset/observation/F-C0032-001
* Location : Tainan's weather at that time (Krusty-Krab is located in Bikini Bottom where is the country of Tainan)
### Operations
1.  After input ==**"weather"**== then we will show the detail of Bikini Bottom's weather
2.  Show Detail
    :::success
    1. Current Time
    2. The description of weather
    3. The probability of rain
    4. Lowest Temperature
    5. Comfort
    6. Highest Temperature
    :::
:::info
:hamburger:Bikini Bottom : 2022-12-25 00:00:00
Weather晴時多雲
The Prob Of Rain: 0
Lowest Temperature: 10
Comfort: 寒冷
Highest Temperature: 12

The weather in Bikini Bottom is fine today,you can go out to Krusty Krab to enjoy the scenery and delicious meals!
:::
3. Give you **Suggestion**
    >The weather in Bikini Bottom is fine today,you can go out to Krusty Krab to enjoy the scenery and delicious meals! 
    
    >The weather in Bikini Bottom is bad today,you can call delivery!!
![](https://i.imgur.com/t6XAv73.png)
4. Then we have two choice **"deliver"**, **"for here"**. 
### Function
1. Give customer comment to make a choice.
2. Provide Friendly and Sincere Service
3. Have a good time with Krusty-Krab

---
## Feature 5 : Choose way to go to Krusty-Krab
### Operations
1. we have two choice **"deliver"**, **"for here"**. 
2. You can just click the text or input it.
    case 1-1 : ==**"deliver"**== (with make a order first).
    Then you can choose to kill time
    ![](https://i.imgur.com/Ytu0lxK.png)
    case 1-2 : ==**"deliver"**== (without make a order first).
    :::info
    :hamburger:You have to order food!
    Input "menu" to see what to eat
    :::
    ![](https://i.imgur.com/RwG8ZaL.png)

    case 2: ==**"for here"**== -> ==**walk**==
    ![](https://i.imgur.com/WcUhliS.png)
    case 2-2: ==**"for here"**== -> ==**bus**==
    see Feature 8 : Take a Bus To Krusty-Krab
### Function
1. Customize your needs

---
## Featuer 6 : Call to Krusty-Krab
### Operation
1. After click ==**Call to Squidward!**== or just input ==**contact**==
![](https://i.imgur.com/bJ7gNgT.png)
2. Then call to 09123456789
![](https://i.imgur.com/sTSi2Lv.png)

### Function
1. Maybe a customer want to make a reservation.
2. Want to talk to Squidward to give some feedback directly!

---
## Featuer 7 : Give us Feedback by email
**Technque** [reference](https://www.learncodewithmike.com/2020/02/python-email.html)
1. Import MIMEMultipart
2. Get the secret of gmail
3. Set SMTP Server

 
### Operation
1. Input ==**feedback**==, then customer will see the Boss and the employee that work in Krusty-Krab
2. Choose which one you want to leave feedback to him.
3. Customer can see the image of every one. Just click them or input the job.
4. After operation, customer can see the detail of everyone.
    > Fry Cook : Spongebob works as a fry cook at the Krusty Krab, a job which he is exceptionally skilled at and enjoys thoroughly.

    > Caher : Squidward works as a cashier at the Krusty Krab, a job which he is not good at and hates it.

    > Delivery Man : Patrick works as a delivery man at the Krusty Krab, a job which he send food to customers personally.

    > Boss : Mr. crab works as a boss at the Krusty Krab, a job which he is good at and enjoys it.
5. Leave Feedback to them (ex. **You are really good at running a restaurant. Thank you!**)
:::info
:hamburger:Mr. crab works as a boss at the Krusty Krab, a job which he is good at and enjoys it.
Input your feedback to Mr. crab!!!
:::
![](https://i.imgur.com/txHbLnj.png)
6. Then Krusty-Krab will receive your feedback. Thank you!
![](https://i.imgur.com/RTd7De4.png)

### Function
Improve the Krusty-Krab or Courage the hard-working employee.

---
## Feature 8 : Take a Bus To Krusty-Krab
### Operation
1. Input ==**"bus"**==
2. Then we will show the customer every stop of the Bus
3. Customer just click one of it or input the name of the stop(ex.==**"pineapple"**==)
![](https://i.imgur.com/tSOEbPM.png)
4. Then customer can see the the ticked price from the source (**pineapple**) to destination (**Krusty-Krab**) and the time to pass (in minutes)
:::info
:hamburger: Stop : Pineapple House
SpongeBob lives here
Ticket price: 7
Time to pass : 5
:::
![](https://i.imgur.com/4BcylHU.png)
5. If the customer choose to click ==**"Krusty-Krab"**== or input ==**"Krusty-Krab"**==, the customer will see the actual **loacation of Krusty Krab restaurant** and the **map** of Bikini Bottom
![](https://i.imgur.com/SmQo2SW.png)

### Function
1. Provide customer a practical way to go to Krusty-Krab.
2. Save the time. The cusomer will feel more comfortable.
3. Provide Friendly and Sincere Service

---
## Feature 9 : Find the address of Krusty-Krab
### Operation
1. Input ==**"address"**==
2. Then we will show the customer the actual **loacation of Krusty Krab restaurant** and the **map** of Bikini Bottom
3. Customer can open the google map
![](https://i.imgur.com/tvMSa22.png)

---
## Reference

### Build a Line Bot
[Python 與 Line bot — 從頭開始建立一個 Line 機器人，部署到 Heroku！](https://medium.com/@chihsuan/pipenv-%E6%9B%B4%E7%B0%A1%E5%96%AE-%E6%9B%B4%E5%BF%AB%E9%80%9F%E7%9A%84-python-%E5%A5%97%E4%BB%B6%E7%AE%A1%E7%90%86%E5%B7%A5%E5%85%B7-135a47e504f4)
[Pipenv 更簡單、更快速的 Python 套件管理工具](https://medium.com/@chihsuan/pipenv-%E6%9B%B4%E7%B0%A1%E5%96%AE-%E6%9B%B4%E5%BF%AB%E9%80%9F%E7%9A%84-python-%E5%A5%97%E4%BB%B6%E7%AE%A1%E7%90%86%E5%B7%A5%E5%85%B7-135a47e504f4)
[為什麼以及如何製作 Requirements.txt](https://boscacci.medium.com/why-and-how-to-make-a-requirements-txt-f329c685181e)

### Line Bot implement
[回覆內容](https://ithelp.ithome.com.tw/articles/10195531)
[選單](https://steam.oxxostudio.tw/category/python/example/line-template-message.html)
[使用說明](https://ithelp.ithome.com.tw/articles/10297676?sc=rss.qu)
[email](https://www.learncodewithmike.com/2020/02/python-email.html)
[表情符號](https://developers.line.biz/en/docs/messaging-api/emoji-list/#line-emoji-definitions)
[Python+LINE Bot 輕鬆打造股市機器人(六) : LINE Bot基本功能-圖片、影片及音訊](https://vocus.cc/article/6209b3f5fd89780001566c9a)
[Python+LINE Bot 輕鬆打造股市機器人(七) : LINE Bot基本功能- 按鈕樣板](https://vocus.cc/article/62157c51fd897800019dd340)
[使用 LINE BOT SDK](https://qiu-yan-ming.gitbook.io/python-chatbot/shi-yong-line-bot-sdk)
[[Python+LINE Bot教學]提升使用者體驗的按鈕樣板訊息(Buttons template message)實用技巧](https://www.learncodewithmike.com/2020/07/line-bot-buttons-template-message.html)
[資料庫](https://www.learncodewithmike.com/2020/06/python-line-bot.html)
[資料庫新竹](https://www.learncodewithmike.com/2020/07/python-line-bot-connect-postgresql.html)
[DAY 28 Image message(圖片訊息)](https://ithelp.ithome.com.tw/articles/10279953)
[天氣資料](https://opendata.cwb.gov.tw/dataset/observation?page=1)
[hooks-vs-callbacks-vs-webhooks](https://medium.com/geekculture/hooks-vs-callbacks-vs-webhooks-f2f1fa6bdbcd)

### Template
[Line Fitness](https://github.com/aqwefghnm/LineChatBot)
[NBA](https://github.com/chonyy/daily-nba)
[ Currency Related](https://github.com/vickyyeh/Linebot)
[TOC](https://github.com/NCKU-CCS/TOC-Project-2020)
[Food Line Bot](https://github.com/mikeku1116/food-linebot/blob/master/foodlinebot/views.py)
[資料庫](https://www.learncodewithmike.com/2020/06/python-line-bot.html)
[資料庫新竹](https://www.learncodewithmike.com/2020/07/python-line-bot-connect-postgresql.html)
[DAY 28 Image message(圖片訊息)](https://ithelp.ithome.com.tw/articles/10279953)
[學姊](https://github.com/F64081169/TOC)










