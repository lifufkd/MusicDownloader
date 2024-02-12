#####################################
#            Created by             #
#                SBR                #
#####################################
import copy
import json
import os
import sys


#####################################

class ConfigParser:
    def __init__(self, file_path):
        super(ConfigParser, self).__init__()
        self.__file_path = file_path
        self.__default = {'tg_api': '', 'admins': []}
        self.__current_config = None
        self.parse_args()

    def load_conf(self):
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                config = json.loads(file.read())
            if len(config['tg_api']) == 0:
                sys.exit('config is invalid')
        else:
            self.create_conf()
            sys.exit('config is not existed')
        return config

    def parse_args(self):
        self.__current_config = self.load_conf()

    def create_conf(self):
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.__default, sort_keys=True, indent=4))

    def get_config(self):
        return self.__current_config


