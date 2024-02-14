#####################################
#            Created by             #
#                SBR                #
#####################################
import os
import telebot
from threading import Lock
from config_parser import ConfigParser
from frontend import Bot_inline_btns, BotWords
from backend import UserData, DbAct
from db import DB
############static variables#####################
config_name = 'secrets.json'
#################################################


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def broadcast_msg(user_id):
    if user_id in user_data.get_users().keys() and user_id in user_data.get_vote().values():
        personal_data = user_data.get_users()[user_id]
        for admin in db_actions.get_admins():
            bot.send_message(admin, f'Новый пользователь!\nНикнейм: @{personal_data[1]}\nИмя: {personal_data[2]}\nФамилия: '
                                    f'{personal_data[3]}\nID Пользователя: {user_id}\nID обращения: '
                                    f'{get_key(user_data.get_vote(), user_id)}\nПодтвердите верификацию '
                                    f'(/accept "ID обращения") или отклоните (/reject "ID обращения")')


def main():

    @bot.message_handler(commands=['AddMusic', 'creators', 'admin', 'accept', 'reject'])
    def addmusic(message):
        command = message.text.replace('/', '')
        user_id = message.chat.id
        if user_id in user_data.get_users().keys():
            if not user_data.get_users()[user_id][0]:
                buttons = Bot_inline_btns()
                if command == 'AddMusic' and db.get_role(user_id) is not None:
                    bot.send_message(user_id, 'Скачать песню', reply_markup=buttons.dow_music())
                elif command == 'creators':
                    bot.reply_to(message,
                                 'Создатели:\nzzsxd - фронтенд составляющая бота.\nSBR - бэкенд составляющая бота.',
                                 reply_markup=buttons.authors())
                elif db.get_role(user_id):  # раздел с привилегиями админа
                    if command == 'admin':
                        bot.send_message(user_id, f'Привет, {message.from_user.first_name}\nКоличество пользователей:\n'
                                                  f'Всего загружено песен:\nТекущая папка загрузки:\n'
                                                  f'Свободное место на диске:\n', reply_markup=buttons.admin_btns())
                    if command[7:] in user_data.get_vote().keys():
                        candidate_id = user_data.get_vote()[command[7:]]
                        if command[:6] == 'accept':
                            user_data.get_users()[candidate_id][0] = False
                            db_actions.add_user(candidate_id)
                            bot.send_message(candidate_id, 'Вы прошли модерацию, можете загружать музыку (/AddMusic)')
                        elif command[:6] == 'reject':
                            bot.send_message(candidate_id, 'Заявка на модерацию отклонена')
                        del user_data.get_vote()[command[7:]]

    @bot.message_handler(commands=['start'])
    def start(message):
        user_id = message.chat.id
        user_data.init_user(user_id, [message.from_user.username, message.from_user.first_name, message.from_user.last_name])
        user_state = user_data.get_users()[user_id]
        if not user_state[0]:
            buttons = Bot_inline_btns()
            bot.reply_to(message, words.hello_msg(db.get_role(user_id)))
            if db.get_role(user_id) is None:
                bot.send_message(user_id, 'Пройдите модерацию✅', reply_markup=buttons.start_btns())

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        user_id = call.message.chat.id
        if user_id in user_data.get_users().keys():
            buttons = Bot_inline_btns()
            user_state = user_data.get_users()[user_id]
            if not user_state[0]:
                if call.data == 'moder' and db.get_role(user_id) is None:
                    user_state[0] = True
                    user_data.add_vote(user_id)
                    bot.send_message(user_id, 'Ожидайте верификации')
                    broadcast_msg(user_id)
                if db.get_role(user_id): # админ функции
                    if call.data == 'stats':
                        bot.send_message(user_id, 'Всего скачиваний:\nСкачиваний за месяц:\nСкачиваний за неделю:\n'
                                                               'Скачиваний за день:')
                    elif call.data == 'users':
                        bot.send_message(user_id, 'Выберите действие', reply_markup=buttons.users_btns())
                    elif call.data == 'allusers':
                        pass
                    elif call.data == 'change_folder':
                        bot.send_message(user_id, 'Путь до папки', reply_markup=buttons.folder_btns())
                    elif call.data == 'changepath':
                        pass
                if db.get_role(user_id) is not None: # методы загрузки
                    if call.data == 'searchnickname':
                        pass
                    elif call.data == 'onname':
                        pass
                    elif call.data == 'onyoutube':
                        pass
                    elif call.data == 'onvk':
                        pass
                    elif call.data == 'onyandex':
                        pass
                    elif call.data == 'onsoundcloud':
                        pass

    bot.polling(none_stop=True)


if '__main__' == __name__:
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}').get_config()
    db = DB(f'{work_dir}/{config["db_file_name"]}', Lock(), config)
    words = BotWords()
    user_data = UserData(db)
    db_actions = DbAct(db, config)
    bot = telebot.TeleBot(config['tg_api'])
    main()
