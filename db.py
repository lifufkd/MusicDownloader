#####################################
#            Created by             #
#                SBR                #
#####################################
import copy
import json
import os
import sqlite3
#####################################


class DB:
    def __init__(self, path):
        super(DB, self).__init__()
        self.__db_path = path
        self.__cursor = None
        self.__db = None
        self.init()

    def init(self):
        if not os.path.exists(self.__db_path):
            self.__db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.__cursor = self.__db.cursor()
            self.__cursor.execute('''CREATE TABLE users(
            tg_id INTEGER,
            role INTEGER,
            UNIQUE(tg_id)
            )
            ''')
            self.__db.commit()
        else:
            self.__db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.__cursor = self.__db.cursor()

    def db_write(self, queri, args):
        self.__cursor.execute(queri, args)
        self.__db.commit()

    def db_read(self, queri, args):
        self.__cursor.execute(queri, args)
        return self.__cursor.fetchall()

