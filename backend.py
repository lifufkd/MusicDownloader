#####################################
#            Created by             #
#                SBR                #
#####################################
import copy
import json
#####################################


class UserData:
    def __init__(self):
        super(UserData, self).__init__()
        self.__online_users = {}
        self.__default = [False, 0]

    def init(self, user_id):  ### запускается только один раз при вводе /start
        if user_id not in self.__online_users.keys():
            self.__online_users.update({user_id: copy.deepcopy(self.__default)})

    def get_users(self):
        return self.__online_users

    def get_user(self, user_id):
        return self.__online_users[user_id]

    def update_reset(self, tg_id):
        self.__online_users[tg_id][0:4] = copy.deepcopy(self.__default)