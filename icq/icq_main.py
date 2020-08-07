import json

from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler, CommandHandler

import data
import messages
from icq.debit_card import DebitCard

list_debits = []


def base(bot, event):
    if event.text == '/info':
        send_message(bot, event, messages.GREETING_NEW_USERS)
    elif event.text == '/products':
        send_start_message(bot, event)


def inputer(bot, event):
    if '/' in event.text:
        pass
    else:
        appllience = get_debit_appllience(event.data['from']['userId'])
        if appllience == None:
            bot.send_text(chat_id=event.data['from']['userId'],
                          text='Я не понимаю что вы хотите. Вы можете оформить заявку'
                               ' на продукты банка введя команду ')
        else:
            appllience.set_field(bot, event, event.text)


def get_debit_appllience(id):
    for x in list_debits:
        if x.telegramId == id:
            return x
    return None


def buttons_cb(bot, event):
    if event.data['callbackData'] == "call_back_id_1":
        debit_card_data_grabbing(bot, event)
    elif event.data['callbackData'] == "call_back_id_2":
        credit_card_data_grabbing(bot, event)


def debit_card_data_grabbing(bot, event):
    if (get_debit_appllience(event.data['from']['userId']) == None):
        new_appllience = DebitCard(bot, event, event.data['from']['userId'])
        list_debits.append(new_appllience)
    else:
        bot.send_text(chat_id=event.data['from']['userId'],
                      text='У вас уже оформлена заявка. Введите запрошенное поле.')


def credit_card_data_grabbing(bot, event):
    send_callback_query(bot, event, messages.INFORMATION_BEFORE_START_FILLING_DATA)
    # bot.send_text(chat_id=event.data['from']['userId'], text='shol nahui')


def send_callback_query(bot, event, text):
    bot.answer_callback_query(
        query_id=event.data['queryId'],
        text=text,
        show_alert=True)


def send_message(bot, event, text):
    bot.send_text(chat_id=event.from_chat, text=text)


def send_start_message(bot, event):
    bot.send_text(chat_id=event.from_chat,
                  text=messages.GREETING_NEW_USERS,
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "Дебетовая карта", "callbackData": "call_back_id_1", "style": "primary"},
                      {"text": "Кредитная карта", "callbackData": "call_back_id_2", "style": "primary"}
                  ]]))
                  )


def init():
    bot = Bot(data.ICQ_TOKEN)
    bot.dispatcher.add_handler(CommandHandler(callback=base))
    bot.dispatcher.add_handler(MessageHandler(callback=inputer))
    bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_cb))
    bot.start_polling()
