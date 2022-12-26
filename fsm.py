import os
from dotenv import load_dotenv

from transitions.extensions import GraphMachine
from linebot import LineBotApi,WebhookParser
from linebot.models import MessageAction,MessageEvent,TextMessage,TextSendMessage,VideoSendMessage
from linebot.models import PostbackAction,URIAction,CarouselColumn,ImageCarouselColumn,URITemplateAction,MessageTemplateAction

from utils import send_text_message,send_button_message,send_image_message
load_dotenv()

my_url=os.getenv("MY_URL", None)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    def into_f(self,event):
        title='fRONT'
        text='你看著前面，現在要做什麼？'
        btn=[
            MessageTemplateAction(label='向左轉',text='向左轉'),
            MessageTemplateAction(label='向右轉',text='向右轉'),
            MessageTemplateAction(label='向後轉',text='向後轉'),
            MessageTemplateAction(label='檢查',text='檢查')
        ]        
        url=f'{my_url}/img/toc_f.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_r(self,event):
        title='rIGHT'
        text='你看著右邊，現在要做什麼？'
        btn=[
            MessageTemplateAction(label='向左轉',text='向左轉'),
            MessageTemplateAction(label='向右轉',text='向右轉'),
            MessageTemplateAction(label='向後轉',text='向後轉'),
            MessageTemplateAction(label='檢查',text='檢查')
        ]
        url=f'{my_url}/img/toc_r.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_b(self,event):
        title='bACK'
        text='你看著後面，現在要做什麼？'
        btn=[
            MessageTemplateAction(label='向左轉',text='向左轉'),
            MessageTemplateAction(label='向右轉',text='向右轉'),
            MessageTemplateAction(label='向後轉',text='向後轉'),
            MessageTemplateAction(label='檢查',text='檢查')
        ]
        url=f'{my_url}/img/toc_b.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_l(self,event):
        title='lEFT'
        text='你看著左邊，現在要做什麼？'
        btn=[
            MessageTemplateAction(label='向左轉',text='向左轉'),
            MessageTemplateAction(label='向右轉',text='向右轉'),
            MessageTemplateAction(label='向後轉',text='向後轉'),
            MessageTemplateAction(label='檢查',text='檢查')
        ]
        url=f'{my_url}/img/toc_l.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_f_check(self,event):
        title='檢查前面'
        text='你發現前面有白板，公布欄和鎖盒，現在要做什麼？'
        btn=[
            MessageTemplateAction(label='檢查白板',text='檢查白板'),
            MessageTemplateAction(label='檢查公佈欄',text='檢查公佈欄'),
            MessageTemplateAction(label='檢查鎖盒',text='檢查鎖盒'),
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_f.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_r_check(self,event):
        title='檢查右邊'
        text='你發現右邊有月曆與鎖盒，電腦和門，現在要做什麼？'
        btn=[
            MessageTemplateAction(label='檢查月曆與鎖盒',text='檢查月曆與鎖盒'),
            MessageTemplateAction(label='檢查電腦',text='檢查電腦'),
            MessageTemplateAction(label='檢查門',text='檢查門'),
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_r.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_b_check(self,event):
        title='檢查後面'
        text='你發現後面有櫃子和鎖盒，現在要做什麼？'
        btn=[
            MessageTemplateAction(label='檢查櫃子',text='檢查櫃子'),
            MessageTemplateAction(label='檢查鎖盒',text='檢查鎖盒'),
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_b.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_l_check(self,event):
        title='檢查左邊'
        text='你發現左邊有兩面窗戶和鎖盒，現在要做什麼？'
        btn=[
            MessageTemplateAction(label='檢查左邊窗戶',text='檢查左邊窗戶'),
            MessageTemplateAction(label='檢查右邊窗戶',text='檢查右邊窗戶'),
            MessageTemplateAction(label='檢查鎖盒',text='檢查鎖盒'),
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_l.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_white_board(self,event):
        title='檢查白板'
        text='白板上有全部的字母，你發現有些顏色不一樣，是想要提示什麼？'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_white_board.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_billboard(self,event):
        title='檢查公佈欄'
        text='公佈欄上有幾種動物照片若干張。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_billboard.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_f_lock(self,event):
        title='fRONT鎖盒'
        text='你發現了白板旁的鎖盒，應該是要輸入一些字母。※請輸入小寫字母，若想不到可以按下返回。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_f_lock.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_f_ans(self,event):
        title='fRONT鎖盒內'
        text='你解開了fRONT鎖盒，裡面有一張畫著什麼的紙。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_f_ans.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_window(self,event):
        title='檢查窗戶'
        text='你打開窗戶發現這裡是荒郊野外的高樓，只能關上窗戶繼續解謎。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_window.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_l_lock(self,event):
        title='lEFT鎖盒'
        text='你發現了窗戶旁的鎖盒，應該是要輸入一些字母。※請輸入小寫字母，若想不到可以按下返回。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_l_lock.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_l_ans(self,event):
        title='lEFT鎖盒內'
        text='你解開了lEFT鎖盒，裡面有一張畫著什麼的紙。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_l_ans.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_cabinet(self,event):
        title='檢查櫃子'
        text='你感覺櫃子的數量像是什麼，也發現一些櫃子上貼著紙張。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_cabinet.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_b_lock(self,event):
        title='bACK鎖盒'
        text='你發現了櫃子上的鎖盒，應該是要輸入一些字母。※請輸入小寫字母，若想不到可以按下返回。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_b_lock.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_b_ans(self,event):
        title='bACK鎖盒內'
        text='你解開了bACK鎖盒，裡面有一張畫著什麼的紙。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_b_ans.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_c_l(self,event):
        title='檢查月曆與鎖盒'
        text='牆上掛著月曆與鎖盒，之間是有什麼關係？'
        btn=[
            MessageTemplateAction(label='檢查月曆',text='檢查月曆'),
            MessageTemplateAction(label='檢查鎖盒',text='檢查鎖盒'),
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_c_l.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_calendar(self,event):
        title='檢查月曆'
        text='月曆應該是某年的12月，但年份早已看不清楚，上面註記的\'✲\'代表著什麼？'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_calendar.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_r_lock(self,event):
        title='rIGHT鎖盒'
        text='你發現了月曆旁的鎖盒，應該是要輸入一些字母。※請輸入小寫字母，若想不到可以按下返回。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_r_lock.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_r_ans(self,event):
        title='rIGHT鎖盒內'
        text='你解開了rIGHT鎖盒，裡面有一張畫著什麼的紙。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_r_ans.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_computer(self,event):
        title='檢查電腦'
        text='這是一台老舊的電腦，細看還是windows XP系統，螢幕上還打著奇怪的注音，你覺得十分怪異。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_computer.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_door(self,event):
        title='檢查門'
        text='門被鎖上了，所以你出不去。'
        btn=[
            MessageTemplateAction(label='檢查鎖盒',text='檢查鎖盒'),
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_door.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_door_lock(self,event):
        title='門鎖盒'
        text='為了離開這裡，你嘗試解開門上的鎖盒，應該是要輸入一些字母。※請輸入小寫字母，若想不到可以按下返回。'
        btn=[
            MessageTemplateAction(label='返回',text='return')
        ]
        url=f'{my_url}/img/toc_door_lock.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def into_end(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token,'恭喜過關☺☺☺☺☺☺☺☺。任意輸入回到一開始。')
        return True
    def error(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token,'鎖解不開，看來答案錯了。')
        return True
    def start_(self,event):
        title='開始遊戲'
        text='這裡是哪裡？'
        btn=[
            MessageTemplateAction(label='向前看',text='向前看'),
            MessageTemplateAction(label='向右看',text='向右看'),
            MessageTemplateAction(label='向後看',text='向後看'),
            MessageTemplateAction(label='向左看',text='向左看')
        ]
        url=f'{my_url}/img/toc_0.png'
        send_button_message(event.reply_token,title,text,btn,url)
        return True
    def states_not_ch(self,event):
        reply_token = event.reply_token
        send_text_message(reply_token,'沒有效果，請按按鍵或提示再次嘗試')
        return True
    def fsm_(self,event):
        reply_token = event.reply_token
        url=f'{my_url}/img/fsm.png'
        send_image_message(reply_token,url)
        return True

        
