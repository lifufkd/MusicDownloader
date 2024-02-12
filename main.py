#####################################
#            Created by             #
#                SBR                #
#####################################
import telebot
#from telebot import types
from frontend import Bot_inline_btns

#####################################
############static variables#####################
TG_api = '6794028156:AAH8GHDE004iq5TLeXAsWYc11ZpTFKNWct0'
admins = [818895144, 1897256227]
#################################################

bot = telebot.TeleBot(TG_api)


@bot.message_handler(commands=['start', 'creators', 'admin'])
def start(message):
    command = message.text.replace('/', '')
    buttons = Bot_inline_btns()
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


@bot.message_handler(commands=['addmusic'])
def addmusic(message):
    buttons = Bot_inline_btns()
    bot.send_message(message.chat.id, 'Скачать песню', reply_markup=buttons.dow_music())


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    buttons = Bot_inline_btns()
    if call.data == 'moder':
        bot.send_message(call.message.chat.id, 'Ожидайте верификации')
        bot.send_message(1897256227, 'Новый пользователь! Подтвердите верификацию.', reply_markup=buttons.verification())
    elif call.data == 'accept':
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
