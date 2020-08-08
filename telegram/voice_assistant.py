import os

import telebot
from gtts import gTTS

from telegram import telegram_main

voices_enable = {}
globalBot = telebot.TeleBot


def change(message, bot):
    global globalBot
    globalBot = bot
    voices_enable[message.chat.id] = not voices_enable[message.chat.id]
    globalBot.send_message(message.chat.id,
                           'Voice assistant is ' + ('enabled' if voices_enable[message.chat.id] else 'disabled'))
    telegram_main.start(message)


def send_voice_message(message, text):
    try:
        if voices_enable[message.from_user.id]:
            tts = gTTS(text=text, lang='ru')
            filename = str(message.from_user.id) + '.ogg'
            tts.save(filename)
            file = open(str(filename), 'rb')
            globalBot.send_voice(message.from_user.id, file)
            file.close()
            os.remove(filename)
    except Exception:
        print('exception')
