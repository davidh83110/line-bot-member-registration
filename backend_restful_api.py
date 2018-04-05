from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
import json
import datetime

from DB_CONNECTION import connection

app = Flask(__name__)
api = Api(app)


# sql_stat = ("""select * from bot.Doctor_Info""")
# result = connection.db().do_query(sql_stat)
# print(result)

class db(object):

    __uid_verify = ("""select * from bot.USER_INFO where user_uid = %s""")

    __status_verify = ("""select user_status from bot.USER_INFO where user_uid = %s""")

    __role_verify = ("""select user_role from bot.USER_INFO where user_uid = %s""")

    __uid_insert = ("""INSERT INTO bot.USER_INFO (user_uid) VALUES (%s)""")

    __status_update = ("""UPDATE bot.USER_INFO SET user_status = %s WHERE user_uid = %s""")

    __name_update = ("""UPDATE bot.USER_INFO SET user_name = %s WHERE user_uid = %s""")

    __email_update = ("""UPDATE bot.USER_INFO SET user_email = %s WHERE user_uid = %s""")

    __enable_update = ("""UPDATE bot.USER_INFO SET user_enable = %s WHERE user_uid = %s""")

    __role_update = ("""UPDATE bot.USER_INFO SET user_role = %s WHERE user_uid = %s""")



    @classmethod
    def uid_verify(cls, user_uid):

        result = connection.db().do_query(cls.__uid_verify, (user_uid,))
        print(result)
        if result != ():
            return True
        else:
            return False

    @classmethod
    def status_verify(cls, user_uid):

        result = connection.db().do_query(cls.__status_verify, (user_uid,))
        print(result)
        if result != ():
            result = result[0][0]
            return result
        else:
            return False

    @classmethod
    def role_verify(cls, user_uid):

        result = connection.db().do_query(cls.__role_verify, (user_uid,))
        print(result)
        if result != ():
            result = result[0][0]
            return result
        else:
            return False


    @classmethod
    def user_status_update(cls, user_status, user_uid):

        connection.db().do_query(cls.__status_update, (user_status, user_uid,))

    @classmethod
    def user_name_update(cls, user_name, user_uid):

        connection.db().do_query(cls.__name_update, (user_name, user_uid,))

    @classmethod
    def user_email_update(cls, user_email, user_uid):

        connection.db().do_query(cls.__email_update, (user_email, user_uid,))

    @classmethod
    def user_enable_update(cls, user_enable, user_uid):

        connection.db().do_query(cls.__enable_update, (user_enable, user_uid,))

    @classmethod
    def user_role_update(cls, user_role, user_uid):

        connection.db().do_query(cls.__role_update, (user_role, user_uid,))

    @classmethod
    def user_uid_insert(cls, user_uid):

        connection.db().do_query(cls.__uid_insert, (user_uid,))







class verify(Resource):
    def post(selfs):
        user_data = request.data.decode("utf-8")
        dict_user_data = json.loads(user_data)
        print(dict_user_data)

        user_uid = dict_user_data.get('user_uid')

        user_action = dict_user_data.get('user_action')

        if user_action == 'uid_verify':
            if db.uid_verify(user_uid):
                print('data')
                verify_result = {'uid_verify': 'True'}
                return jsonify(verify_result)
            else:
                print('no data')
                verify_result = {'uid_verify': 'False'}
                return jsonify(verify_result)

        elif user_action == 'status_verify':
            user_status = db.status_verify(user_uid)
            if user_status == '0':
                user_info = {'user_status': '0'}
                return jsonify(user_info)
            elif user_status == '1':
                user_info = {'user_status': '1'}
                return jsonify(user_info)
            elif user_status == '2':
                user_info = {'user_status': '2'}
                return jsonify(user_info)
            elif user_status == '3':
                user_info = {'user_status': '3'}
                return jsonify(user_info)
            else:
                return False

        elif user_action == 'role_verify':
            user_role = db.role_verify(user_uid)
            if user_role == 1:
                user_info = {'user_role': 'doctor'}
                return jsonify(user_info)
            elif user_role == 2:
                user_info = {'user_role': 'sales'}
                return jsonify(user_info)
            else:
                return False


class update(Resource):
    def post(selfs):
        user_data = request.data.decode("utf-8")
        dict_user_data = json.loads(user_data)
        print(dict_user_data)

        user_uid = dict_user_data.get('user_uid')
        user_name = dict_user_data.get('user_name')
        user_email = dict_user_data.get('user_email')
        user_enable = dict_user_data.get('user_enable')
        user_role = dict_user_data.get('user_role')
        user_action = dict_user_data.get('user_action')
        user_status = dict_user_data.get('user_status')

        if user_action == 'user_status_update':
            db.user_status_update(user_status, user_uid)

        if user_action == 'user_uid_insert':
            db.user_uid_insert(user_uid)

        if user_action == 'user_name_update':
            db.user_name_update(user_name, user_uid)

        if user_action == 'user_email_update':
            db.user_email_update(user_email, user_uid)

        if user_action == 'user_enable_update':
            db.user_enable_update(user_enable, user_uid)

        if user_action == 'user_role_update':
            db.user_role_update(user_role, user_uid)



api.add_resource(verify, '/verify')
api.add_resource(update, '/update')


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":

    app.run(host='0.0.0.0')

