from flask import Flask, abort
from flask import request

app = Flask(__name__)

globalBot = None


def init(bot):
    global globalBot
    globalBot = bot


@app.route('/api/message/send', methods=['POST'])
def get_tasks():
    if not request.json:
        abort(400)
    content = request.get_json()
    user_id = content['telegramId']
    message = content['message']
    print('sending message to user_id=%s' % user_id)
    globalBot.send_message(user_id, message)
