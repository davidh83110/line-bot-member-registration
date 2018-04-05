import requests
import json

verify_url = "http://13.113.14.143:5000/verify"
update_url = "http://127.0.0.1:5000/update"


def user_post_data(user_data, action):
	user_data['user_action'] = action
	data = json.dumps(user_data)

	if action == 'user_uid_insert':
		requests.post(update_url, data)

	elif action == 'user_enable_update':
		requests.post(update_url, data)

	elif action == 'user_role_update':
		requests.post(update_url, data)






user_uid = 'f0070854b92daea0a6f9d42f57f'
user_data = {'user_uid': user_uid, 'user_enable': '1', 'user_action': 'user_enable_update'}
result = user_post_data(user_data, 'user_enable_update')
print(result)


# if result == '3':
#
#     # role = 1 , doctor
#     user_role_data = {'user_uid': user_uid, 'user_action': 'role_verify'}
#     role_verify_result = user_post_data(user_role_data, 'role_verify')
#     if role_verify_result == 'doctor':
#         print("doctor template")# todo: show doctor template
#
#     # role = 2 , sales
#     if role_verify_result == 'sales':
#         print("sales template")# todo: shoe slaes template


