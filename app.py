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

line_bot_api = LineBotApi('UzPWIqC+oUZN4d3NNmVJNyJN9QmSrY5hM6KpKh+ZIBf1HilTC2jBD2gvF+WsC1t+3kk564wIO7r4go0Vjc6KfomZGLjCoXys7esSMGbAHbr2Ht2dUcF6t3sO8KJDTKGq/hQ7J79Urd+m59ZDlQqq')
handler = WebhookHandler('16fb1eb8d6fbf5deb2868a21f54wwww')

### REST URL
verify_url = "http://13.113.14.143:5000/verify"
update_url = "http://13.113.14.143:5000/update"


def user_post_data(user_data, action):
	user_data['user_action'] = action
	data = json.dumps(user_data)

	if action == 'uid_verify':
		result = requests.post(verify_url, data)
		print(result.text)
		if json.loads(result.text)['uid_verify'] == 'True':
			# user_name = json.loads(result.text)['user_name']
			# user_role = json.loads(result.text)['user_role']
			return True
		else:
			return None, None

	elif action == 'role_verify':
		result = requests.post(verify_url, data)
		print(result.text)
		if json.loads(result.text)['user_role'] != ():
			user_role = json.loads(result.text)['user_role']
			return user_role
		else:
			return None

	elif action == 'status_verify':
		result = requests.post(verify_url, data)
		print(result.text)
		try:
			status_result = json.loads(result.text)['user_status']
			print(status_result)
		except:
			status_result = 'false'

		if status_result == '1':
			return str(1)
			# todo: please enter name

		elif status_result == '2':
			return str(2)
			# todo: please enter mail

		elif status_result == '3':
			return str(3)
			# todo : verify role and show template

		else:
			return False

	elif action == 'user_status_update':
		requests.post(update_url, data)

	elif action == 'user_uid_insert':
		requests.post(update_url, data)

	elif action == 'user_name_update':
		requests.post(update_url, data)

	elif action == 'user_email_update':
		requests.post(update_url, data)

	elif action == 'user_enable_update':
		requests.post(update_url, data)

	elif action == 'user_role_update':
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


	if msg == "sales":
		user_data = {'user_uid': user_uid, 'user_action': 'uid_verify'}
		uid_verify_result = user_post_data(user_data , 'uid_verify')

		status_data = {'user_uid': user_uid, 'user_action': 'status_verify'}
		status_verify_result = user_post_data(status_data, 'status_verify')
		print(status_verify_result)

		if uid_verify_result != (None, None) and status_verify_result == '3':
			line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="Sales,歡迎"))
		else:
			line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="Permission Denied"))


	elif msg == "doctor":
		user_data = {'user_uid': user_uid, 'user_action': 'uid_verify'}
		uid_verify_result = user_post_data(user_data, 'uid_verify')

		status_data = {'user_uid': user_uid, 'user_action': 'status_verify'}
		status_verify_result = user_post_data(status_data, 'status_verify')

		if uid_verify_result != (None, None) and status_verify_result == '3':
			line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="Doctor,歡迎"))
		else:
			line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="Permission Denied"))



	else:
		user_id_data = {'user_uid': user_uid, 'user_action': 'uid_verify'}
		uid_verify_result = user_post_data(user_id_data, 'uid_verify')

		user_status_data = {'user_uid': user_uid, 'user_action': 'status_verify'}
		status_verify_result = user_post_data(user_status_data, 'status_verify')
		print(status_verify_result)

		if status_verify_result == '1':
			line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="請輸入E-Mail,空白請輸入0"))
			# update status = 2 and insert name
			# todo: mail format verify
			user_status_data = {'user_status': '2', 'user_uid': user_uid, 'user_action': 'user_status_update'}
			status_result = user_post_data(user_status_data, 'user_status_update')
			print(status_result)

			input_user_name = msg
			user_name_data = {'user_name': input_user_name, 'user_uid': user_uid, 'user_action': 'user_name_update'}
			name_result = user_post_data(user_name_data, 'user_name_update')
			print(name_result)

		elif status_verify_result == '2':
			line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="註冊完成,您好"))
			# update status = 3 and insert email
			user_status_data = {'user_status': '3', 'user_uid': user_uid, 'user_action': 'user_status_update'}
			status_result = user_post_data(user_status_data, 'user_status_update')
			print(status_result)

			input_user_email = msg
			user_email_data = {'user_email': input_user_email, 'user_uid': user_uid, 'user_action': 'user_email_update'}
			mail_result = user_post_data(user_email_data, 'user_email_update')
			print(mail_result)

			# update user_enable
			user_enable_data = {'user_uid': user_uid, 'user_enable': '1', 'user_action': 'user_enable_update'}
			enable_result = user_post_data(user_enable_data, 'user_enable_update')
			print(enable_result)

			# update user_role
			user_role_data = {'user_uid': user_uid, 'user_role': '2', 'user_action': 'user_role_update'}
			role_result = user_post_data(user_role_data, 'user_role_update')
			print(role_result)

		elif status_verify_result == '3':
			line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="status = 3"))
			# role = 1 , doctor
			user_role_data = {'user_uid': user_uid, 'user_action': 'role_verify'}
			role_verify_result = user_post_data(user_role_data, 'role_verify')

			if role_verify_result == 'doctor':
				print("doctor template")# todo: show doctor template
				return 0

			# role = 2 , sales
			if role_verify_result == 'sales':
				print("sales template")# todo: shoe sales template
				return 0

			else:
				return False

		else:
			line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="尚未註冊,請輸入姓名"))

			user_uid_data = {'user_uid': user_uid, 'user_action': 'user_uid_insert'}
			user_uid_insert_result = user_post_data(user_uid_data, 'user_uid_insert')

			user_status_data = {'user_status': '1', 'user_uid': user_uid, 'user_action': 'user_status_update'}
			status_update_result = user_post_data(user_status_data, 'user_status_update')


	# else:
	# 	user_data = {'user_uid': user_uid, 'user_action': 'user_uid_insert'}
	# 	# user_post_data(user_uid, 'user_uid_insert')
	# 	user_post_data(user_data)
	# 	user_status_data = {'user_status': '0', 'user_uid': user_uid, 'user_action': 'user_status_update'}
	# 	user_post_data(user_status_data)
	# 	line_bot_api.reply_message(
	# 		event.reply_token,
	# 		TextSendMessage(text="歡迎"))
	# 	return 0
	# else:
	# 	line_bot_api.reply_message(
	# 			event.reply_token,
	# 			TextSendMessage(text="Permission Denied , 請聯絡Admin"))
	# 	return 0






if __name__ == "__main__":
	app.run()
