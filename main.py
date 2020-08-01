import threading

import requests
import telebot

import data
import debit
import keyboard

bot = telebot.TeleBot(data.BOT_TOKEN)

if __name__ == '__main__':
    # response = requests.post(data.CREATE_DEBIT_URL, data={'debitCard': '{}'}, headers=data.headers)
    # print(response.status_code)
    bot_polling_thread = threading.Thread(target=bot.polling, args=())
    bot_polling_thread.start()

    print('bot is started')


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.text)
    bot.send_message(message.chat.id, 'Тип заявки', reply_markup=keyboard.WELCOME)


@bot.message_handler(commands=['test'])
def test(message):
    print("I`m still working")
    bot.send_message(message.chat.id, "I`m still working")


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'дебетовая карта':
        debit.debit(message, bot)
