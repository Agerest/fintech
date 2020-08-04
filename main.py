import threading

import telebot

import application
import controller
import credit_card
import data
import debit_card
import messages
import techsupport

bot = telebot.TeleBot(data.BOT_TOKEN)

if __name__ == '__main__':
    bot_polling_thread = threading.Thread(target=bot.polling, args=())
    bot_polling_thread.start()
    flask_thread = threading.Thread(target=controller.init, args=())
    flask_thread.start()
    print('bot is started')


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.add(messages.CREDIT_CARD, messages.DEBIT_CARD, messages.CREDIT, messages.TECH_SUPPORT)
    bot.send_message(message.chat.id, 'Тип заявки', reply_markup=keyboard)


@bot.message_handler(commands=['test'])
def test(message):
    print("I`m still working")
    bot.send_message(message.chat.id, "I`m still working")


@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.text)
    if message.text.lower() == 'дебетовая карта':
        debit_card.init(message, bot)
    elif message.text.lower() == 'техподдержка':
        techsupport.init(message, bot)
    if message.text.lower() == 'кредитная карта':
        credit_card.init(message, bot)
    if message.text.lower() == 'оформленные заявки':
        application.init(message, bot)
