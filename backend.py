#####################################
#            Created by             #
#                SBR                #
#####################################
import copy
import json
#####################################


class UserData:
    def __init__(self, db):
        super(UserData, self).__init__()
        self.__db = db
        self.__online_users = {}
        self.__current_vote_id = 0
        self.__vote_id = {}

    def init_user(self, user_id, data):  ### запускается только один раз при вводе /start
        if user_id not in self.__online_users.keys():
            self.__online_users.update({user_id: copy.deepcopy([False, data[0], data[1], data[2]])})

    def get_vote(self):
        return self.__vote_id

    def get_users(self):
        return self.__online_users

    def add_vote(self, user_id):
        self.__current_vote_id += 1
        self.__vote_id[str(self.__current_vote_id)] = user_id

    def get_user(self, user_id):
        if user_id in self.__online_users.keys():
            return self.__online_users[user_id]


class DbAct:
    def __init__(self, db, config):
        super(DbAct, self).__init__()
        self.__db = db
        self.__config = config

    def add_user(self, user_id):
        self.__db.db_write('INSERT INTO users (tg_id, role) VALUES (?, ?)', (user_id, False))

    def get_admins(self):
        data = list()
        admins = self.__db.db_read('SELECT tg_id FROM users WHERE role = "1"', ())
        for i in self.__config['admins']:
            admins.append((i, ))
        if len(admins) > 0:
            for i in admins:
                data.append(i[0])
        else:
            data = []
        return set(data)

