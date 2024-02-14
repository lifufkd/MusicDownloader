#####################################
#            Created by             #
#                SBR                #
#####################################
import os
import telebot
from threading import Lock
from config_parser import ConfigParser
from frontend import Bot_inline_btns, BotWords
from backend import DbAct, TempUserData, MusicDownload
from db import DB
############static variables#####################
config_name = 'secrets.json'
#################################################


def broadcast_msg(user_id):
    if db_actions.get_user(user_id) is not None and db_actions.get_request_by_user_id(user_id) is not None:
        personal_data = db_actions.get_user(user_id)
        for admin in db_actions.get_admins():
            bot.send_message(admin, f'Новый пользователь!\nНикнейм: @{personal_data[0]}\nИмя: {personal_data[1]}\nФамилия: '
                                    f'{personal_data[2]}\nID Пользователя: {user_id}\nID обращения: '
                                    f'{db_actions.get_request_by_user_id(user_id)}\nПодтвердите верификацию '
                                    f'(/accept "ID обращения") или отклоните (/reject "ID обращения")')


def main():
    @bot.message_handler(commands=['start'])
    def start(message):
        user_id = message.chat.id
        db_actions.add_user(
            [user_id, message.from_user.username, message.from_user.first_name, message.from_user.last_name])
        if not db_actions.get_user(user_id)[3]:
            buttons = Bot_inline_btns()
            bot.reply_to(message, words.hello_msg(db_actions.get_role(user_id)))
            if db_actions.get_role(user_id) is None:
                bot.send_message(user_id, 'Пройдите модерацию✅', reply_markup=buttons.start_btns())

    @bot.message_handler(commands=['AddMusic', 'creators', 'admin', 'accept', 'reject'])
    def addmusic(message):
        command = message.text.replace('/', '')
        user_id = message.chat.id
        if db_actions.get_user(user_id) is not None:
            if not db_actions.get_user(user_id)[3]:
                buttons = Bot_inline_btns()
                if command == 'AddMusic' and db_actions.get_role(user_id) is not None:
                    bot.send_message(user_id, 'Скачать песню', reply_markup=buttons.dow_music())
                elif command == 'creators':
                    bot.reply_to(message,
                                 'Создатели:\nzzsxd - фронтенд составляющая бота.\nSBR - бэкенд составляющая бота.',
                                 reply_markup=buttons.authors())
                elif db_actions.get_role(user_id):  # раздел с привилегиями админа
                    if command == 'admin':
                        bot.send_message(user_id, f'Привет, {message.from_user.first_name}\nКоличество пользователей:\n'
                                                  f'Всего загружено песен:\nТекущая папка загрузки:\n'
                                                  f'Свободное место на диске:\n', reply_markup=buttons.admin_btns())
                    if db_actions.get_request_by_request_id(command[7:]) is not None:
                        candidate_id = db_actions.get_request_by_request_id(command[7:])
                        if command[:6] == 'accept':
                            db_actions.unblock_user(candidate_id)
                            db_actions.update_role_user(candidate_id)
                            bot.send_message(candidate_id, 'Вы прошли модерацию, можете загружать музыку (/AddMusic)')
                        elif command[:6] == 'reject':
                            bot.send_message(candidate_id, 'Заявка на модерацию отклонена')
                        db_actions.del_request_by_request_id(command[7:])

    @bot.message_handler(content_types=['text'])
    def text(message):
        user_input = message.text
        user_id = message.chat.id
        user_current_action = temp_user_data.temp_data(user_id)[user_id][0]
        if user_current_action == 0:
            bot.send_message(user_id, f'Информация о пользователе\n{db_actions.search_by_nick(user_input)}')
        elif user_current_action == 1:
            if music_downloader.youtube_download(user_input):
                bot.send_message(user_id, 'Ваша песня успешно загружена!')
            else:
                bot.send_message(user_id, 'Произошла ошибка, попробуйте ещё раз')
        elif user_current_action == 2:
            if config.update_music_folder(user_input):
                bot.send_message(user_id, 'Папка успешно обновлена!')
            else:
                bot.send_message(user_id, 'Путь не существует')
        temp_user_data.temp_data(user_id)[user_id][0] = None

    @bot.callback_query_handler(func=lambda call: True)
    def callback(call):
        user_id = call.message.chat.id
        if db_actions.get_user(user_id) is not None:
            buttons = Bot_inline_btns()
            if not db_actions.get_user(user_id)[3]:
                if call.data == 'moder' and db_actions.get_role(user_id) is None:
                    db_actions.block_user(user_id)
                    db_actions.add_request(user_id)
                    bot.send_message(user_id, 'Ожидайте верификации')
                    broadcast_msg(user_id)
                if db_actions.get_role(user_id): # админ функции
                    if call.data == 'stats':
                        bot.send_message(user_id, 'Всего скачиваний:\nСкачиваний за месяц:\nСкачиваний за неделю:\n'
                                                               'Скачиваний за день:')
                    elif call.data == 'users':
                        bot.send_message(user_id, 'Выберите действие', reply_markup=buttons.users_btns())
                    elif call.data == 'allusers':
                        bot.send_message(user_id, f'Информация о пользователях\n{db_actions.search_all()}')
                    if call.data == 'searchnickname':
                        temp_user_data.temp_data(user_id)[user_id][0] = 0
                        bot.send_message(user_id, 'Введите никнейм без "@"')
                    elif call.data == 'change_folder':
                        bot.send_message(user_id, f'Текущий путь до папки: {config.get_config()["misic_folder"]}', reply_markup=buttons.folder_btns())
                    elif call.data == 'changepath':
                        temp_user_data.temp_data(user_id)[user_id][0] = 2
                        bot.send_message(user_id, 'Введите новый путь до папки с музыкой')
                if db_actions.get_role(user_id) is not None: # методы загрузки
                    if call.data == 'onname':
                        pass
                    elif call.data == 'onyoutube':
                        temp_user_data.temp_data(user_id)[user_id][0] = 1
                        bot.send_message(user_id, 'Введите ссылку на видео')
                    elif call.data == 'onvk':
                        pass
                    elif call.data == 'onyandex':
                        pass
                    elif call.data == 'onsoundcloud':
                        pass

    bot.polling(none_stop=True)


if '__main__' == __name__:
    users_actions = {}
    work_dir = os.path.dirname(os.path.realpath(__file__))
    config = ConfigParser(f'{work_dir}/{config_name}')
    db = DB(f'{work_dir}/{config.get_config()["db_file_name"]}', Lock(), config.get_config())
    temp_user_data = TempUserData()
    music_downloader = MusicDownload()
    words = BotWords()
    db_actions = DbAct(db, config.get_config())
    bot = telebot.TeleBot(config.get_config()['tg_api'])
    main()
