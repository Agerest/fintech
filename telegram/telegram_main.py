import telebot

import application
import data
import messages
import techsupport
from telegram import debit_card, credit_card, credit, other, voice_assistant

bot = telebot.TeleBot(data.BOT_TOKEN)


def init():
    bot.polling()


@bot.message_handler(commands=['start'])
def start_message(message):
    start(message)


def start(message):
    if message.chat.id not in voice_assistant.voices_enable:
        voice_assistant.voices_enable[message.chat.id] = False
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row(messages.CREDIT_CARD, messages.DEBIT_CARD)
    keyboard.row(messages.CREDIT, messages.TECH_SUPPORT)
    keyboard.row(messages.APPLICATION_LIST, messages.VOICE_GENERATOR)
    keyboard.row(messages.HOLDING, messages.APPLICATION_LIST)
    bot.send_message(message.chat.id, messages.GREETING_NEW_USERS, reply_markup=keyboard)
    voice_assistant.send_voice_message(message, messages.GREETING_NEW_USERS)


@bot.message_handler(commands=['test'])
def test(message):
    print("I`m still working")
    bot.send_message(message.chat.id, "I`m still working")


@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.text)
    if message.text == messages.DEBIT_CARD:
        debit_card.init(message, bot)
    if message.text == messages.TECH_SUPPORT:
        techsupport.init(message, bot)
    if message.text == messages.CREDIT_CARD:
        credit_card.init(message, bot)
    if message.text == messages.APPLICATION_LIST:
        application.init(message, bot)
    if message.text == messages.VOICE_GENERATOR:
        voice_assistant.change(message, bot)
    if message.text == messages.CREDIT:
        credit.init(message, bot)
    if message.text == messages.HOLDING:
        other.init_holding(message, bot)
