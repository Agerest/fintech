import requests
import telebot

import data
import messages


class Application(object):
    def __init__(self, id, type, status):
        self.id = id
        self.type = type
        self.status = status

    id = None
    type = None
    status = None


globalBot = telebot.TeleBot
applicationList = []


def init(message, bot):
    global globalBot
    globalBot = bot
    get_keyboard(message)


def get_keyboard(message):
    response = requests.post(data.CUBA_HOST + data.GET_APPLICATION_LIST_URL,
                             json={'id': message.from_user.id}, headers={'content-type': 'application/json'})
    code = response.status_code
    print(code)
    if code == 200:
        application_list_json = response.json()
        global applicationList
        for app in application_list_json:
            applicationList.append(Application(app['id'], app['type'], app['status']))
        result_array = [key.id for key in applicationList]
        print(result_array)
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.row(*result_array)
        globalBot.send_message(message.from_user.id, messages.ENTER_CURRENT_APPLICATION, reply_markup=keyboard)
        globalBot.register_next_step_handler(message, message_handler)
    else:
        globalBot.send_message(message.from_user.id, messages.FAILED)


def message_handler(message):
    application_id = message.text
    status = ''
    for app in applicationList:
        if app.id == application_id:
            status = app.status
    if status != '':
        globalBot.send_message(message.from_user.id, messages.APPLICATION_STATUS + status)
    else:
        globalBot.send_message(message.from_user.id, messages.FAILED)
