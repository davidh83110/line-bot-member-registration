import MySQLdb


class db(object):

    def __init__(self):

        self.__cnxn = self.__connect()

    def __connect(self):

        __cnxn = MySQLdb.connect(host="13.113.14.143", user="user",
                                 passwd="aaaaaaa", db="test")
        return __cnxn


    def do_query(self, sql_string, data=None):

        __cursor = self.__cnxn.cursor()
        __data = data

        if __data is None and ('SELECT' in sql_string or 'select' in sql_string):
            __cursor.execute(sql_string)
            return __cursor.fetchall()

        elif __data is None and ('UPDATE' in sql_string or 'update' in sql_string):
            __cursor.execute(sql_string)

        elif __data != None and ('UPDATE' in sql_string or 'update' in sql_string):
            __cursor.execute(sql_string, __data)
            self.__cnxn.commit()

        elif __data is None and 'delete' in sql_string:
            __cursor.execute(sql_string)
            self.__cnxn.commit()

        elif __data != None and ('SELECT' in sql_string or 'select' in sql_string):
            __cursor.execute(sql_string, data)
            return __cursor.fetchall()

        elif __data != None and type(__data) == list:
            __cursor.executemany(sql_string, data)
            self.__cnxn.commit()
        elif __data != None and type(__data) == tuple:
            __cursor.execute(sql_string, data)
            self.__cnxn.commit()
        else:
            print('Do you want to query Database ?')

    def do_commit(self):
        self.__cnxn.commit()


