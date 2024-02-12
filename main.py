#####################################
#            Created by             #
#                SBR                #
#####################################
import telebot
#####################################


class TgBot:
    def __init__(self, config):
        super(TgBot, self).__init__()
        global bot
        self.__config = config
        bot = telebot.TeleBot(self.__config)

    @bot.message_handler(commands=['start', 'creators', 'admin'])
    def start(self, message):
        pass


    @bot.message_handler(content_types=['photo', 'video', 'voice', 'audio', 'image', 'sticker', 'text'])
    def text(self, message):
        pass

    @bot.callback_query_handler(func=lambda call: True)
    def callback(self, call):
        pass

        bot.polling(none_stop=True)


if '__main__' == __name__:
    bot = telebot.TeleBot()
    tgbot = TgBot
user = User_data()
db = db_oper(DB_path)