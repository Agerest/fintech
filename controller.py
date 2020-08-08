from flask import Flask, abort
from flask import request

import data
from icq import icq_main
from telegram import telegram_main
from vk import vk_main

app = Flask(__name__)

telegramBot = telegram_main.bot
vkBot = vk_main.vk_session
icqBot = icq_main.bot


def init():
    app.run(port=data.FLASK_PORT)


@app.route('/', methods=['GET'])
def test():
    print('test request')
    return 'TEST'


@app.route('/api/message/send', methods=['POST'])
def get_tasks():
    if not request.json:
        abort(400)
    content = request.get_json()
    user_id = content['telegramId']
    message = content['message']
    user_type = content['userType']
    print('sending message \'%s\' to user_id=%s' % (message, user_id))
    if user_type == 'tlg':
        telegramBot.send_message(user_id, message)
    if user_type == 'icq':
        icqBot.send_text(chat_id=user_id, text=message)
    if user_type == 'vk':
        vkBot.messages.send(user_id=user_id, random_id=0, message=message)
    return 'success'
