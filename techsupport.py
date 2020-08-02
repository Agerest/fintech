import requests

import data

globalBot = None


def init(message, bot):
    global globalBot
    globalBot = bot
    globalBot.send_message(message.from_user.id, "Введите ваше сообщение в техподдержку (для завершения \'выход\'")
    globalBot.register_next_step_handler(message, get_message)


def get_message(message):
    if message == 'выход':
        globalBot.send_message(message.from_user.id, "Вы вышли из техподдержки")
    else:
        result = {'userId': message.from_user.id,
                  'message': message.text}
        response = \
            requests.post(data.HOST + data.SEND_MESSAGE_URL, json=result, headers={'content-type': 'application/json'})
        code = response.status_code
        print(code)
        if code == 200:
            globalBot.send_message(message.from_user.id, "Ваше сообщение успешно доставлено, ожидайте ответа")
        else:
            globalBot.send_message(message.from_user.id, "Ошибка")
        globalBot.register_next_step_handler(message, get_message)
