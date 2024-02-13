#####################################
#            Created by             #
#                SBR                #
#####################################
import os
import telebot
#from telebot import types
from threading import Lock
from config_parser import ConfigParser
from frontend import Bot_inline_btns, BotWords
from backend import UserData
from db import DB
############static variables#####################
config_name = 'secrets.json'
#################################################


def broadcast_msg(user_id):
    if user_id in user_data.get_user().keys() and user_id in user_data.get_vote():
        buttons = Bot_inline_btns().verification()
        for admin in config['admins']:
            bot.send_message(admin, f'Новый пользователь! Подтвердите верификацию.\nID обращения: {user_data.get_vote()[user_id]}', reply_markup=buttons)


def main():
    @bot.message_handler(commands=['start', 'creators', 'admin'])
    def start(message):
        command = message.text.replace('/', '')
        user_id = message.chat.id
        user_data.init_user(user_id)
        user_state = user_data.get_user()[user_id]
        if not user_state[0]:
            buttons = Bot_inline_btns()
            if command == 'start':
                bot.reply_to(message, words.hello_msg(db.get_role(user_id)))
                if db.get_role(user_id) is None:
                    bot.send_message(user_id, 'Пройдите модерацию✅', reply_markup=buttons.start_btns())
            elif command == 'creators':
                bot.reply_to(message, 'Создатели:\nzzsxd - фронтенд составляющая бота.\nSBR - бэкенд составляющая бота.',
                             reply_markup=buttons.authors())
            elif command == 'admin' and db.get_role(user_id):
                bot.send_message(user_id, f'Привет, {message.from_user.first_name}\nКоличество пользователей:\n'
                                                  f'Всего загружено песен:\nТекущая папка загрузки:\n'
                                                  f'Свободное место на диске:\n', reply_markup=buttons.admin_btns())

    @bot.message_handler(commands=['AddMusic'])
    def addmusic(message):
        user_id = message.chat.id
        if user_id in user_data.get_user().keys():
            user_state = user_data.get_user()[user_id]
            if db.get_role(user_id) is not None:
                buttons = Bot_inline_btns()
                bot.send_message(user_id, 'Скачать песню', reply_markup=buttons.dow_music())
        else:
            bot.send_message(user_id, 'Введите /start')

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        user_id = call.message.chat.id
        if user_id in user_data.get_user().keys():
            buttons = Bot_inline_btns()
            user_state = user_data.get_user()[user_id]
            if not user_state[0]:
                if call.data == 'moder' and db.get_role(user_id) is None:
                    user_state[0] = True
                    user_data.add_vote(user_id)
                    bot.send_message(user_id, 'Ожидайте верификации')
                    broadcast_msg(user_id)
                if db.get_role(user_id):
                    if call.data == 'accept':
                        bot.send_message(user_id, 'Поздравляем! Вы верифицированы.\nНапишите /addmusic чтобы начать!')
                    elif call.data == 'rejected':
                        bot.send_message(user_id, 'К сожалению, мы не можем вас верифицировать!')
                    elif call.data == 'stats':
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
                if db.get_role(user_id) is not None:
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
        else:
            bot.send_message(user_id, 'Введите /start')
    bot.polling(none_stop=True)


if '__main__' == __name__:
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}').get_config()
    db = DB(f'{work_dir}/{config["db_file_name"]}', Lock())
    words = BotWords()
    user_data = UserData(db)
    bot = telebot.TeleBot(config['tg_api'])
    main()
