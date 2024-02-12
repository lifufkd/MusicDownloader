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

    def get_players(self):
        return self.__online_users

    def update_pull(self, tg_id, data):
        self.__online_users[tg_id][3].append(data)

    def update_reset(self, tg_id):
        self.__online_users[tg_id][0:4] = copy.deepcopy(self.__default_admin)