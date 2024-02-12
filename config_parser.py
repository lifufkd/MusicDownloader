#####################################
#            Created by             #
#                SBR                #
#####################################
import copy
import json
#####################################

class ConfigParser:
    def __init__(self, path):
        super(ConfigParser, self).__init__()
        self.__path = path

    def __init__(self, file_path):
        super(Parser, self).__init__()
        self.__file_path = file_path
        self.__default = {'db_name': '', 'db_host': '', 'db_user': '', 'db_passwd': '', 'logo_path': '', 'export_xlsx_path': ''}
        self.__current_config = None
        self.parse_args()

    def load_conf(self):
        if os.path.exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                config = file.read()
        else:
            self.create_conf()
            sys.exit('config is not existed')
        return config

    def parse_args(self):
        args = json.loads(self.load_conf())
        self.__current_config = args

    def create_conf(self):
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.__default, sort_keys=True, indent=4))
    def init(self, id, admins):  ### запускается только один раз при вводе /start
        default_user = [False, False, 0, [], None]
        if id not in self.__online_users.keys():
            if id in admins:
                default_user[0] = True
            self.__online_users.update({id: copy.deepcopy(default_user)})


