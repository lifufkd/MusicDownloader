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
        self.__default = [False]
        self.__current_vote_id = 0
        self.__vote_id = {}

    def init_user(self, user_id):  ### запускается только один раз при вводе /start
        if user_id not in self.__online_users.keys():
            self.__online_users.update({user_id: copy.deepcopy(self.__default)})

    def get_vote(self):
        return self.__vote_id

    def get_users(self):
        return self.__online_users

    def add_vote(self, user_id):
        self.__current_vote_id += 1
        self.__vote_id[user_id] = self.__current_vote_id

    def get_user(self):
        return self.__online_users

