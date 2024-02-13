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
    def __init__(self, path, lock):
        super(DB, self).__init__()
        self.__lock = lock
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
            role BOOLEAN,
            UNIQUE(tg_id)
            )
            ''')
            self.__db.commit()
        else:
            self.__db = sqlite3.connect(self.__db_path, check_same_thread=False)
            self.__cursor = self.__db.cursor()

    def db_write(self, queri, args):
        self.set_lock()
        self.__cursor.execute(queri, args)
        self.__db.commit()
        self.realise_lock()

    def db_read(self, queri, args):
        self.set_lock()
        self.__cursor.execute(queri, args)
        self.realise_lock()
        return self.__cursor.fetchall()

    def get_role(self, user_id):
        is_admin = None
        quanity = self.db_read(f'SELECT role FROM users WHERE tg_id = "{user_id}"', ())
        if len(quanity) > 0:
            if quanity[0][0] == 1:
                is_admin = True
            else:
                is_admin = False
        return is_admin
    
    def set_lock(self):
        self.__lock.acquire(True)

    def realise_lock(self):
        self.__lock.release()
