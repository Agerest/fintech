import requests

import data
import messages

globalBot = None


def init(message, bot):
    global globalBot
    globalBot = bot
    globalBot.send_message(message.from_user.id, messages.ENTER_MESSAGE)
    globalBot.register_next_step_handler(message, get_message)


def get_message(message):
    if message.text.lower() == 'выход':
        globalBot.send_message(message.from_user.id, messages.TECH_SUPPORT_EXIT)
    else:
        result = {'telegramId': message.from_user.id,
                  'message': message.text}
        response = requests.post(data.CUBA_HOST + data.SEND_MESSAGE_URL,
                                 json=result, headers={'content-type': 'application/json'})
        code = response.status_code
        print(code)
        if code == 200:
            globalBot.send_message(message.from_user.id, messages.TECH_SUPPORT_SUCCESS)
        else:
            globalBot.send_message(message.from_user.id, messages.FAILED)
        globalBot.register_next_step_handler(message, get_message)
