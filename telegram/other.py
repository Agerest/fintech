import telebot

import messages
from telegram import telegram_main

globalBot = telebot.TeleBot


def init_holding(message, bot):
    global globalBot
    globalBot = bot
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.add('вклады', 'брокерский счет', 'иис', 'опиф', 'подбор инвестиционной программы', messages.BACK)
    globalBot.send_message(message.from_user.id, text=messages.ENTER_TYPE, reply_markup=keyboard)
    globalBot.register_next_step_handler(message, set_type_holding)


def set_type_holding(message):
    if message.text == messages.BACK:
        telegram_main.start(message)
    elif message.text == 'иис':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.add('сейф', 'простое решение', 'иис', messages.BACK)
        globalBot.send_message(message.from_user.id, text=messages.ENTER_TYPE, reply_markup=keyboard)
        globalBot.register_next_step_handler(message, set_iis)
    elif message.text == 'опиф':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.add('опиф', 'опиф Лалэ', messages.BACK)
        globalBot.send_message(message.from_user.id, text=messages.ENTER_TYPE, reply_markup=keyboard)
        globalBot.register_next_step_handler(message, set_opif)
    else:
        globalBot.send_message(message.from_user.id, messages.ENTERING_PROGRESS_MESSAGE_1)
        globalBot.send_message(message.from_user.id, messages.ENTER_FIO)
        globalBot.register_next_step_handler(message, set_full_name)


def set_iis(message):
    if message.text == messages.BACK:
        init_holding(message, globalBot)
    else:
        globalBot.send_message(message.from_user.id, messages.ENTERING_PROGRESS_MESSAGE_1)
        globalBot.send_message(message.from_user.id, messages.ENTER_FIO)
        globalBot.register_next_step_handler(message, set_full_name)


def set_opif(message):
    if message.text == messages.BACK:
        init_holding(message, globalBot)
    else:
        globalBot.send_message(message.from_user.id, messages.ENTERING_PROGRESS_MESSAGE_1)
        globalBot.send_message(message.from_user.id, messages.ENTER_FIO)
        globalBot.register_next_step_handler(message, set_full_name)


def set_full_name(message):
    globalBot.send_message(message.from_user.id, messages.ENTER_PHONE_NUMBER)
    globalBot.register_next_step_handler(message, set_phone)


def set_phone(message):
    globalBot.send_message(message.from_user.id, 'Мы с вами свяжемся')
    telegram_main.start(message)
