#####################################
#            Created by             #
#                SBR                #
#####################################
import os

import telebot
#from telebot import types
from config_parser import ConfigParser
from frontend import Bot_inline_btns
from backend import UserData
############static variables#####################
config_name = 'secrets.json'
#################################################


def broadcast_msg():
    buttons = Bot_inline_btns()
    for admin in config['admins']:
        bot.send_message(admin, 'Новый пользователь! Подтвердите верификацию.', reply_markup=buttons.verification())


def main():
    @bot.message_handler(commands=['start', 'creators', 'admin'])
    def start(message):
        command = message.text.replace('/', '')
        buttons = Bot_inline_btns()
        user_data.init(message.chat.id)
        user_state = user_data.get_user(message.chat.id)
        if not user_state[0]:
            if command == 'start':
                bot.reply_to(message,
                             'Привет👋\nЯ MusicDownloaderBot🤖 - помогу с загрузкой музыки\nНапишите /creators для получения информации о создателях.')
                bot.send_message(message.chat.id, 'Пройдите модерацию✅', reply_markup=buttons.start_btns())
            elif command == 'creators':
                bot.reply_to(message, 'Создатели:\nzzsxd - фронтенд составляющая бота.\nSBR - бэкенд составляющая бота.',
                             reply_markup=buttons.authors())
            elif command == 'admin':
                bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}\n Количество пользователей:\n'
                                                  f'Всего загружено песен:\nТекущая папка загрузки:\n'
                                                  f'Свободное место на диске:\n', reply_markup=buttons.admin_btns())


    @bot.message_handler(commands=['AddMusic'])
    def addmusic(message):
        buttons = Bot_inline_btns()
        bot.send_message(message.chat.id, 'Скачать песню', reply_markup=buttons.dow_music())


    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        buttons = Bot_inline_btns()
        if call.data == 'moder':
            bot.send_message(call.message.chat.id, 'Ожидайте верификации')
            broadcast_msg()
        elif call.data == 'accept':
            print(call.message)
            bot.send_message(call.message.chat.id, 'Поздравляем! Вы верифицированы.\nНапишите /addmusic чтобы начать!')
        elif call.data == 'rejected':
            bot.send_message(call.message.chat.id, 'К сожалению, мы не можем вас верифицировать!')
        elif call.data == 'stats':
            bot.send_message(call.message.chat.id, 'Всего скачиваний:\nСкачиваний за месяц:\nСкачиваний за неделю:\n'
                                                   'Скачиваний за день:')
        elif call.data == 'users':
            bot.send_message(call.message.chat.id, 'Выберите действие', reply_markup=buttons.users_btns())
        elif call.data == 'allusers':
            pass
        elif call.data == 'searchnickname':
            pass
        elif call.data == 'change_folder':
            bot.send_message(call.message.chat.id, 'Путь до папки', reply_markup=buttons.folder_btns())
        elif call.data == 'changepath':
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
    user_data = UserData()
    bot = telebot.TeleBot(config['tg_api'])
    main()
