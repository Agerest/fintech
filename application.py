import requests
import telebot

import data
import messages

globalBot = None


def init(message, bot):
    global globalBot
    globalBot = bot
    get_keyboard(message)


def get_keyboard(message):
    response = requests.get(data.CUBA_HOST + data.GET_APPLICATION_LIST_URL, params={'telegramId': message.from_user.id})
    code = response.status_code
    print(code)
    if code == 200:
        application_list = response.json()
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.row(application_list)
        globalBot.send_message(message.from_user.id, messages.ENTER_CURRENT_APPLICATION, reply_markup=keyboard)
        globalBot.register_next_step_handler(message, message_handler)
    else:
        globalBot.send_message(message.from_user.id, messages.FAILED)


def message_handler(message):
    application_id = message.text
    response = requests.get(data.CUBA_HOST + data.GET_APPLICATION_URL, params={'applicationId': application_id})
    code = response.status_code
    print(code)
    if code == 200:
        application_status = response.json()
        globalBot.send_message(message.from_user.id, messages.APPLICATION_STATUS + application_status)
    else:
        globalBot.send_message(message.from_user.id, messages.FAILED)
