import os

from gtts import gTTS

from telegram import telegram_main

voices_enable = telegram_main.voices_enable
globalBot = telegram_main.bot


def send_voice_message(message, text):
    if voices_enable[message.from_user.id]:
        tts = gTTS(text=text, lang='ru')
        filename = str(message.from_user.id) + '.ogg'
        tts.save(filename)
        file = open(str(filename), 'rb')
        globalBot.send_voice(message.from_user.id, file)
        file.close()
        os.remove(filename)
