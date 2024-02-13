#####################################
#            Created by             #
#                SBR                #
#####################################
import telebot
from telebot import types


#####################################
class Bot_inline_btns:
    def __init__(self):
        super(Bot_inline_btns, self).__init__()
        self.__markup = types.InlineKeyboardMarkup(row_width=2)

    def start_btns(self):
        moder = types.InlineKeyboardButton('Пройти модерацию', callback_data='moder')
        self.__markup.add(moder)
        return self.__markup

    def admin_btns(self):
        btn1 = types.InlineKeyboardButton('Статистика', callback_data='stats')
        btn2 = types.InlineKeyboardButton('Пользователи', callback_data='users')
        btn3 = types.InlineKeyboardButton('Изменить папку сохранения', callback_data='change_folder')
        self.__markup.add(btn1, btn2, btn3)
        return self.__markup

    def users_btns(self):
        btn1 = types.InlineKeyboardButton('Все пользователи', callback_data='allusers')
        btn2 = types.InlineKeyboardButton('Поиск по никнейму', callback_data='searchnickname')
        self.__markup.add(btn1, btn2)
        return self.__markup

    def folder_btns(self):
        btn1 = types.InlineKeyboardButton('Изменить путь', callback_data='changepath')
        self.__markup.add(btn1)
        return self.__markup

    def dow_music(self):
        btn1 = types.InlineKeyboardButton('По названию', callback_data='onname')
        btn2 = types.InlineKeyboardButton('По ссылке YouTube', callback_data='onyoutube')
        btn3 = types.InlineKeyboardButton('По ссылке VK', callback_data='onvk')
        btn4 = types.InlineKeyboardButton('По ссылке Yandex Music', callback_data='onyandex')
        btn5 = types.InlineKeyboardButton('По ссылке SoundCloud', callback_data='onsoundcloud')
        self.__markup.add(btn1, btn2, btn3, btn4, btn5)
        return self.__markup

    def authors(self):
        zzsxd = types.InlineKeyboardButton('zzsxd', url='https://github.com/zzsxd')
        sbr = types.InlineKeyboardButton('SBR', url='https://github.com/lifufkd')
        self.__markup.add(zzsxd, sbr)
        return self.__markup


class BotWords:
    def __init__(self):
        super(BotWords, self).__init__()
        self.__all_words_ru = [', /AddMusic для загрузки музыки', ', /admin для администрирования бота']

    def hello_msg(self, rules):
        addition_rule = {None: [], True: self.__all_words_ru, False: self.__all_words_ru[0]}
        base = 'Привет👋\nЯ MusicDownloaderBot🤖 - помогу с загрузкой музыки\nНапишите /creators для получения информации о создателях'
        return base + ''.join(addition_rule[rules])

