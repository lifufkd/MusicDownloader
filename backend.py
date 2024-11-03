#####################################
#            Created by             #
#                SBR                #
#####################################
import os
import time
import subprocess
import yt_dlp as youtube_dl
#####################################


class TempUserData:
    def __init__(self):
        super(TempUserData, self).__init__()
        self.__user_data = {}

    def temp_data(self, user_id):
        if user_id not in self.__user_data.keys():
            self.__user_data.update({user_id: [None]})
        return self.__user_data


class DbAct:
    def __init__(self, db, config):
        super(DbAct, self).__init__()
        self.__db = db
        self.__config = config
        self.__user_fields = {0: 'id', 1: 'ник', 2: 'имя', 3: 'фамилия', 4: 'заблокирован', 5: 'роль'}
        self.__blocked = {0: 'нет', 1: 'да'}
        self.__roles = {None: 'не определена', 0: 'пользователь', 1: 'администратор'}
        self.__period = {'month': 2678400, 'week': 604800, 'day': 86400}

    def add_user(self, data, config_admins):
        if data[0] in config_admins:
            role = True
        else:
            role = None
        self.__db.db_write('INSERT OR IGNORE INTO users (tg_id, nickname, firstname, lastname, blocked, role) VALUES (?, ?, ?, ?, ?, ?)', (data[0], data[1], data[2], data[3], False, role))

    def update_role_user(self, user_id):
        self.__db.db_write('UPDATE users SET role = ? WHERE tg_id = ?', (False, user_id))

    def get_user(self, user_id):
        user = self.__db.db_read('SELECT nickname, firstname, lastname, blocked FROM users WHERE tg_id = ?', (user_id, ))
        if len(user) > 0:
            return list(user[0])

    def block_user(self, user_id):
        self.__db.db_write('UPDATE users SET blocked = ? WHERE tg_id = ?', (True, user_id))

    def unblock_user(self, user_id):
        self.__db.db_write('UPDATE users SET blocked = ? WHERE tg_id = ?', (False, user_id))

    def add_request(self, user_id):
        self.__db.db_write(f'INSERT INTO request (tg_id) VALUES ({user_id})', ())

    def get_request_by_user_id(self, user_id):
        request = self.__db.db_read('SELECT request_id FROM request WHERE tg_id = ?', (user_id,))
        if len(request) > 0:
            return request[0][0]

    def get_request_by_request_id(self, request_id):
        request = self.__db.db_read('SELECT tg_id FROM request WHERE request_id = ?', (request_id,))
        if len(request) > 0:
            return request[0][0]

    def del_request_by_request_id(self, request_id):
        self.__db.db_write(f'DELETE FROM request WHERE request_id = ?', (request_id, ))

    def add_download(self, data):
        self.__db.db_write(f'INSERT INTO downloads (tg_id, link, platform, time) VALUES (?, ?, ?, ?)', (data[0], data[1], data[2], data[3]))

    def search_by_nick(self, nickname):
        out = ''
        user = self.__db.db_read('SELECT * FROM users WHERE nickname = ?', (nickname,))
        if len(user) > 0:
            for data in range(len(user[0])):
                if data == 4:
                    out += f'{data+1} {self.__user_fields[data]}: {self.__blocked[user[0][data]]}\n'
                elif data == 5:
                    out += f'{data + 1} {self.__user_fields[data]}: {self.__roles[user[0][data]]}\n'
                else:
                    out += f'{data + 1} {self.__user_fields[data]}: {user[0][data]}\n'
        else:
            out = 'Пользователь не найден!'
        return out

    def search_all(self):
        out = ''
        users = self.__db.db_read('SELECT * FROM users', ())
        if len(users) > 0:
            for user in range(len(users)):
                out += f'{user+1} '
                for admin in range(len(users[user])):
                    if admin == 4:
                        out += f'{self.__user_fields[admin]}: {self.__blocked[users[user][admin]]} '
                    elif admin == 5:
                        out += f'{self.__user_fields[admin]}: {self.__roles[users[user][admin]]} '
                    else:
                        out += f'{self.__user_fields[admin]}: {users[user][admin]} '
        else:
            out = 'Пользователь не найден!'
        return out

    def get_users_quanity(self):
        return self.__db.db_read('SELECT count(*) FROM users', ())[0][0]

    def get_download_quanity(self, period):
        return self.__db.db_read(f'SELECT count(*) FROM downloads WHERE time > {int(time.time()) - self.__period[period]}', ())[0][0]

    def get_download_quanity_all(self):
        return self.__db.db_read(f'SELECT count(*) FROM downloads', ())[0][0]


    def get_admins(self):
        data = list()
        admins = self.__db.db_read('SELECT tg_id FROM users WHERE role = "1"', ())
        if len(admins) > 0:
            for i in admins:
                data.append(i[0])
        else:
            data = []
        return set(data)

    def get_role(self, user_id):
        quanity = self.__db.db_read(f'SELECT role FROM users WHERE tg_id = "{user_id}"', ())
        if len(quanity) > 0:
            if quanity[0][0] == 1:
                is_admin = True
            elif quanity[0][0] == 0:
                is_admin = False
            else:
                is_admin = None
            return is_admin


class MusicDownload:
    def __init__(self, db_act, os_type):
        self.__db_act = db_act
        self.__default_pathes = {'Windows': '\\', 'Linux': '/'}
        self.__os_type = os_type

    def youtube_download(self, url, folder, user_id, ffmpeg, proxy=None, login=None, password=None, cookies=None, oauth=None):
        stat = None
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': ffmpeg,
                'prefer_ffmpeg': True,
                'keepvideo': False,
                'verbose': True
            }

            if proxy:
                ydl_opts['proxy'] = proxy

            if login:
                ydl_opts['username'] = login
            if password:
                ydl_opts['password'] = password
            # if cookies:
            #     ydl_opts['cookiefile'] = cookies
            # if oauth:
            #     ydl_opts['oauth_token'] = self.read_oauth_token(oauth)

            print(ydl_opts)

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                file_name = ydl.prepare_filename(info_dict)
                output_file = os.path.splitext(file_name)[0] + '.m4a'

                print("*"*50)
                print(output_file)
                print("*" * 50)
                if os.path.exists(output_file):
                    stat = 0
                else:
                    ydl.download([url])
                    # self.convert_to_aac(file_name, output_file, ffmpeg)
                    # os.remove(file_name)  # Remove original downloaded file
                    self.__db_act.add_download([user_id, url, 'YouTube', int(time.time())])
                    stat = 1
        except:
            pass
        return stat