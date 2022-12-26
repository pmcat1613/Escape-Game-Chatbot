import os
import sys
import json 

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import PostbackAction,URIAction,CarouselColumn,MessageEvent,MessageAction, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message,send_button_message
from ans import check_Q_b,check_Q_door,check_Q_f,check_Q_l,check_Q_r

load_dotenv()

hash_map = dict()

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


@app.route("/", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    data = json.loads(body)

    userId = data['events'][0]['source']['userId']
    print("userid : "+userId)
    machine = hash_map.setdefault(userId,TocMachine(
            states=[
                    "start",
                    "f","f_check","white_board","billboard","f_lock","f_ans",
                    "l","l_check","window","l_lock","l_ans",
                    "b","b_check","cabinet","b_lock","b_ans",
                    "r","r_check","computer","c_l","calendar","r_lock","r_ans",
                    "door","door_lock","end"
            ],
            transitions=[
                #user_start:out
                {"trigger":"start_f","source":"start","dest":"f","conditions":"into_f"},
                {"trigger":"start_r","source":"start","dest":"r","conditions":"into_r"},
                {"trigger":"start_b","source":"start","dest":"b","conditions":"into_b"},
                {"trigger":"start_l","source":"start","dest":"l","conditions":"into_l"},
                #f/r/b/l:trun_'l/r/b'
                {"trigger":"turn_right","source":"f","dest":"r","conditions":"into_r"},
                {"trigger":"turn_right","source":"r","dest":"b","conditions":"into_b"},
                {"trigger":"turn_right","source":"b","dest":"l","conditions":"into_l"},
                {"trigger":"turn_right","source":"l","dest":"f","conditions":"into_f"},
                {"trigger":"turn_left" ,"source":"f","dest":"l","conditions":"into_l"},
                {"trigger":"turn_left" ,"source":"r","dest":"f","conditions":"into_f"},
                {"trigger":"turn_left" ,"source":"b","dest":"r","conditions":"into_r"},
                {"trigger":"turn_left" ,"source":"l","dest":"b","conditions":"into_b"},
                {"trigger":"turn_back" ,"source":"f","dest":"b","conditions":"into_b"},
                {"trigger":"turn_back" ,"source":"r","dest":"l","conditions":"into_l"},
                {"trigger":"turn_back" ,"source":"b","dest":"f","conditions":"into_f"},
                {"trigger":"turn_back" ,"source":"l","dest":"r","conditions":"into_r"},
                #f/r/b/l:into_'f/r/b/l'_check
                {"trigger":"into_check","source":"f","dest":"f_check","conditions":"into_f_check"},
                {"trigger":"into_check","source":"r","dest":"r_check","conditions":"into_r_check"},
                {"trigger":"into_check","source":"b","dest":"b_check","conditions":"into_b_check"},
                {"trigger":"into_check","source":"l","dest":"l_check","conditions":"into_l_check"},
                #'f/r/b/l'_check:return_'f/r/b/l'
                {"trigger":"return_","source":"f_check","dest":"f","conditions":"into_f"},
                {"trigger":"return_","source":"r_check","dest":"r","conditions":"into_r"},
                {"trigger":"return_","source":"b_check","dest":"b","conditions":"into_b"},
                {"trigger":"return_","source":"l_check","dest":"l","conditions":"into_l"},
                #f_check:into_(3*f_place)
                {"trigger":"f_lock"     ,"source":"f_check","dest":"f_lock"     ,"conditions":"into_f_lock"     },
                {"trigger":"white_board","source":"f_check","dest":"white_board","conditions":"into_white_board"},
                {"trigger":"billboard"  ,"source":"f_check","dest":"billboard"  ,"conditions":"into_billboard"  },
                #(f_ans + 3*f_place):return_f_check
                {"trigger":"return_","source":["f_ans","f_lock","white_board","billboard"],"dest":"f_check","conditions":"into_f_check"},
                #Q[f]:error&correct
                {"trigger":"error"  ,"source":"f_lock","dest":"f_lock","conditions":"error"   },
                {"trigger":"correct","source":"f_lock","dest":"f_ans", "conditions":"into_f_ans"},
                #l_check:into_(2*l_place)
                {"trigger":"window","source":"l_check","dest":"window","conditions":"into_window"},
                {"trigger":"l_lock","source":"l_check","dest":"l_lock","conditions":"into_l_lock"},
                #(l_ans + 2*l_place):return_l_check
                {"trigger":"return_","source":["l_ans","l_lock","window"],"dest":"l_check","conditions":"into_l_check"},
                #Q[l]:error&correct
                {"trigger":"error"  ,"source":"l_lock","dest":"l_lock","conditions":"error"     },
                {"trigger":"correct","source":"l_lock","dest":"l_ans" ,"conditions":"into_l_ans"},
                #b_check:into_(2*b_place)
                {"trigger":"cabinet","source":"b_check","dest":"cabinet","conditions":"into_cabinet"},
                {"trigger":"b_lock" ,"source":"b_check","dest":"b_lock" ,"conditions":"into_b_lock" },
                #(b_ans + 2*b_place):return_b_check
                {"trigger":"return_","source":["b_ans","b_lock","cabinet"],"dest":"b_check","conditions":"into_b_check"},
                #Q[b]:error&correct
                {"trigger":"error"  ,"source":"b_lock","dest":"b_lock","conditions":"error"     },
                {"trigger":"correct","source":"b_lock","dest":"b_ans" ,"conditions":"into_b_ans"},
                #r_check:into_(3*r_place)
                {"trigger":"c_l"     ,"source":"r_check","dest":"c_l"     ,"conditions":"into_c_l"     },
                {"trigger":"computer","source":"r_check","dest":"computer","conditions":"into_computer"},
                {"trigger":"door"    ,"source":"r_check","dest":"door"    ,"conditions":"into_door"    },
                #(3*r_place):return_r_check
                {"trigger":"return_","source":["c_l","computer","door"],"dest":"r_check","conditions":"into_r_check"},
                #c_l:into_(2*c_l_place)
                {"trigger":"r_lock"  ,"source":"c_l","dest":"r_lock"  ,"conditions":"into_r_lock"  },
                {"trigger":"calendar","source":"c_l","dest":"calendar","conditions":"into_calendar"},
                #(r_ans + 2*c_l_place):return_c_l
                {"trigger":"return_","source":["r_ans","r_lock","calendar"],"dest":"c_l","conditions":"into_c_l"},
                #Q[r]:error&correct
                {"trigger":"error"  ,"source":"r_lock","dest":"r_lock","conditions":"error"     },
                {"trigger":"correct","source":"r_lock","dest":"r_ans" ,"conditions":"into_r_ans"},
                #door:into_door_lock
                {"trigger":"door_lock","source":"door","dest":"door_lock","conditions":"into_door_lock"},
                #door_lock:return_door
                {"trigger":"return_","source":"door_lock","dest":"door","conditions":"into_door"},
                #Q[door]:error&correct
                {"trigger":"error"  ,"source":"door_lock","dest":"door_lock","conditions":"error"},
                {"trigger":"correct","source":"door_lock","dest":"end"      ,"conditions":"into_end"  },
                #'start/end':into_start
                {"trigger":"end_to_start","source":["start","end"],"dest":"start","conditions":"start_"},
                #not_ch
                {"trigger":"states_not_ch","source":"f"          ,"dest":"f"          ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"r"          ,"dest":"r"          ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"b"          ,"dest":"b"          ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"l"          ,"dest":"l"          ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"f_check"    ,"dest":"f_check"    ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"r_check"    ,"dest":"r_check"    ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"b_check"    ,"dest":"b_check"    ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"l_check"    ,"dest":"l_check"    ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"white_board","dest":"white_board","conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"billboard"  ,"dest":"billboard"  ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"f_ans"      ,"dest":"f_ans"      ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"window"     ,"dest":"window"     ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"l_ans"      ,"dest":"l_ans"      ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"cabinet"    ,"dest":"cabinet"    ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"b_ans"      ,"dest":"b_ans"      ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"c_l"        ,"dest":"c_l"        ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"calendar"   ,"dest":"calendar"   ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"r_ans"      ,"dest":"r_ans"      ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"computer"   ,"dest":"computer"   ,"conditions":"states_not_ch"},
                {"trigger":"states_not_ch","source":"door"       ,"dest":"door"       ,"conditions":"states_not_ch"},
                #fsm
                {"trigger":"fsm_","source":"start"      ,"dest":"start"      ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"f"          ,"dest":"f"          ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"r"          ,"dest":"r"          ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"b"          ,"dest":"b"          ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"l"          ,"dest":"l"          ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"f_check"    ,"dest":"f_check"    ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"r_check"    ,"dest":"r_check"    ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"b_check"    ,"dest":"b_check"    ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"l_check"    ,"dest":"l_check"    ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"white_board","dest":"white_board","conditions":"fsm_"},
                {"trigger":"fsm_","source":"billboard"  ,"dest":"billboard"  ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"f_lock"     ,"dest":"f_lock"     ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"f_ans"      ,"dest":"f_ans"      ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"window"     ,"dest":"window"     ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"l_ans"      ,"dest":"l_ans"      ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"l_lock"     ,"dest":"l_lock"     ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"cabinet"    ,"dest":"cabinet"    ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"b_lock"     ,"dest":"b_lock"     ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"b_ans"      ,"dest":"b_ans"      ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"c_l"        ,"dest":"c_l"        ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"calendar"   ,"dest":"calendar"   ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"r_lock"     ,"dest":"r_lock"     ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"r_ans"      ,"dest":"r_ans"      ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"computer"   ,"dest":"computer"   ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"door"       ,"dest":"door"       ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"door_lock"  ,"dest":"door_lock"  ,"conditions":"fsm_"},
                {"trigger":"fsm_","source":"end"        ,"dest":"end"        ,"conditions":"fsm_"},
            ],
            initial="start",
            auto_transitions=False,
            show_conditions=True,
        )
    )

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
        
    if events == []:
        return "OK" 
    #machine.get_graph().draw('fsm.png', prog="dot", format="png")
    
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        #print(f"REQUEST BODY: \n{body}")
        if event.message.text=='fsm':
            machine.fsm_(event)
        elif machine.state=='end':
            machine.end_to_start(event)
        elif machine.state=='start':
            if event.message.text=='向前看':
                machine.start_f(event)
            elif event.message.text=='向右看': 
                machine.start_r(event)
            elif event.message.text=='向後看':
                machine.start_b(event)
            elif event.message.text=='向左看':
                machine.start_l(event)
            else:
                machine.end_to_start(event)
        elif event.message.text=='return' and (machine.state!='start' and machine.state!='f' and machine.state!='r' and machine.state!='b' and machine.state!='l' and machine.state!='end'):
            machine.return_(event)
        elif machine.state=='f' or machine.state=='r' or machine.state=='b' or machine.state=='l':
            if event.message.text=='向左轉':
                machine.turn_left(event)
            elif event.message.text=='向右轉': 
                machine.turn_right(event)
            elif event.message.text=='向後轉':
                machine.turn_back(event)
            elif event.message.text=='檢查':
                machine.into_check(event)
            else:
                machine.states_not_ch(event)
        elif machine.state=='f_check':
            if event.message.text=='檢查白板':
                machine.white_board(event)
            elif event.message.text=='檢查公佈欄': 
                machine.billboard(event)
            elif event.message.text=='檢查鎖盒':
                machine.f_lock(event)
            else:
                machine.states_not_ch(event)
        elif machine.state=='f_lock':
            if check_Q_f(event.message.text):
                machine.correct(event)
            else:
                machine.error(event)
        elif machine.state=='l_check':
            if event.message.text=='檢查左邊窗戶' or event.message.text=='檢查右邊窗戶': 
                machine.window(event)
            elif event.message.text=='檢查鎖盒':
                machine.l_lock(event)
            else:
                machine.states_not_ch(event)
        elif machine.state=='l_lock':
            if check_Q_l(event.message.text):
                machine.correct(event)
            else:
                machine.error(event)
        elif machine.state=='b_check':
            if event.message.text=='檢查櫃子':
                machine.cabinet(event)
            elif event.message.text=='檢查鎖盒': 
                machine.b_lock(event)
            else:
                machine.states_not_ch(event)
        elif machine.state=='b_lock':
            if check_Q_b(event.message.text):
                machine.correct(event)
            else:
                machine.error(event)
        elif machine.state=='r_check':
            if event.message.text=='檢查月曆與鎖盒':
                machine.c_l(event)
            elif event.message.text=='檢查電腦': 
                machine.computer(event)
            elif event.message.text=='檢查門':
                machine.door(event)
            else:
                machine.states_not_ch(event)
        elif machine.state=='c_l':
            if event.message.text=='檢查月曆':
                machine.calendar(event)
            elif event.message.text=='檢查鎖盒':
                machine.r_lock(event)
            else:
                machine.states_not_ch(event)
        elif machine.state=='r_lock':
            if check_Q_r(event.message.text):
                machine.correct(event)
            else:
                machine.error(event)
        elif machine.state=='door':
            if event.message.text=='檢查鎖盒':
                machine.door_lock(event)
            else:
                machine.states_not_ch(event)
        elif machine.state=='door_lock':
            if check_Q_door(event.message.text):
                machine.correct(event)
            else:
                machine.error(event)
        else:
            machine.states_not_ch(event)
    return "OK"

# '''png_name=""
# @app.route(f"/{png_name}", methods=["GET"])
# def show_fsm():
#     machine.get_graph().draw(png_name, prog="dot", format="png")
#     return send_file("fsm.png", mimetype="image/png")'''
@app.route('/img/<ImageName>', methods=["GET"])
def getImage(ImageName):
    return send_file(f'./img/{ImageName}', mimetype='image/png',as_attachment=True)
#os.environ['PATH'] =  os.pathsep + './Graphviz/bin/'
if __name__ == "__main__":
    from gevent import pywsgi  
    port = os.environ.get("PORT", 8000)

    server = pywsgi.WSGIServer(('0.0.0.0',int(port)),app)

    server.serve_forever()
    # port = os.environ.get("PORT", 8000)
    # app.run(host="0.0.0.0", port=port, debug=True)
