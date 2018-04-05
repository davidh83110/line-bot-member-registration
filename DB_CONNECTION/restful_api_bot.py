#-*- coding: utf-8 -*-
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.models import *
import json
import requests


app = Flask(__name__)

line_bot_api = LineBotApi('UzPWIqC+oUZN4d3NNmVJNyJN9QmSrY5hM6KpKh+ZIBf1HilTC2jBD2gvF+WsC1t+3kk564wIO7r4go0Vjc6KfomZGLjCoXys7esSMGbAHbr2Ht2dUcF6t3sO8KJDTKGq/hQ7J79Urd+m59Z')
handler = WebhookHandler('16fb1eb8d6fbf5deb2868a21f54www')

### REST URL
verify_url = "http://13.113.14.143:5000/verify"
update_url = "http://13.113.14.143:5000/verify"


def user_post_data(user_data, action):
    user_data['user_action'] = action
    data = json.dumps(user_data)

    if action == 'uid_verify':
        result = requests.post(verify_url, data)
        print(result.text)
        if json.loads(result.text)['uid_verify'] == 'True':
            user_name = json.loads(result.text)['user_name']
            user_role = json.loads(result.text)['user_role']
            return user_name, user_role
        else:
            return None, None

    elif action == 'role_verify':
        result = requests.post(verify_url, data)
        print(result.text)
        if json.loads(result.text)['role_verify'] == 'True':
            user_role = json.loads(result.text)['user_role']
            return user_role
        else:
            return None, None

    elif action == 'status_verify':
        result = requests.post(verify_url, data)
        print(result.text)
        try:
            status_result = json.loads(result.text)['user_status']
            print(status_result)
        except:
            pass

        if status_result == '0':
            return str(0)
            # todo: please enter name

        elif status_result == '1':
            return str(1)
            # todo: please enter mail

        elif status_result == '2':
            return str(2)
            # todo : verify role and show template

        else:
            return False



    elif action == 'user_status_update':
        requests.post(update_url, data)




@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return str(200)



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_uid = event.source.user_id
    print(user_uid)
    msg = event.message.text
    print(msg)

    try:
        input = msg.split(',')
        input_name = input[0]
        input_otp = input[1]
        print(input_name)
        print(input_otp)
    except:
        pass

    print("event.reply_token:", event.reply_token)

    if msg == "sales" or msg == "doctor":
        user_data = {'user_uid': user_uid, 'user_action': 'uid_verify'}
        uid_verify_result = user_post_data(user_data, 'uid_verify')

        if uid_verify_result != (None, None):
            user_data = {'user_uid': user_uid, 'user_action': 'status_verify'}
            status_verify_result = user_post_data(user_data, 'status_verify')

            if status_verify_result == '0':
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="尚未註冊,請輸入姓名"))
                # update status = 1
                user_status_data = {'user_status': '1', 'user_uid': user_uid, 'user_action': 'user_status_update'}
                status_update_result = user_post_data(user_status_data, 'user_status_update')

            elif status_verify_result == '1':
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="請輸入E-Mail,空白請輸入0"))
                # update status = 2 and insert name
                # todo: mail formate verify
                user_status_data = {'user_status': '2', 'user_uid': user_uid, 'user_action': 'user_status_update'}
                status_update_result = user_post_data(user_status_data, 'user_status_update')

            elif status_verify_result == '2':
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="註冊完成,您好"))
                # update status = 3 and insert email
                user_status_data = {'user_status': '3', 'user_uid': user_uid, 'user_action': 'user_status_update'}
                status_update_result = user_post_data(user_status_data, 'user_status_update')

            elif status_verify_result == '3':
                # role = 1 , doctor
                role_verify_result = user_post_data(user_data, 'role_verify')
                if role_verify_result == 'doctor':
                    print("doctor template")# todo: show doctor template

                # role = 2 , sales
                if role_verify_result == 'sales':
                    print("sales template")# todo: shoe slaes template

                else:
                    return False




            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="Permission Denied , 請聯絡Admin"))
                return 0
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Permission Denied , 請聯絡Admin"))
            return 0
    else:
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Permission Denied , 請聯絡Admin"))
        return 0






if __name__ == "__main__":
    app.run()
