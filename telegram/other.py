import telebot

import messages
from telegram import telegram_main, voice_assistant
from telegram.debit_card import phone_is_valid

globalBot = telebot.TeleBot


def init_holding(message, bot):
    global globalBot
    globalBot = bot
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.add('вклады', 'брокерский счет', 'иис', 'опиф', 'подбор инвестиционной программы', messages.BACK)
    globalBot.send_message(message.from_user.id, text=messages.ENTER_TYPE, reply_markup=keyboard)
    voice_assistant.send_voice_message(message, messages.ENTER_TYPE)
    globalBot.register_next_step_handler(message, set_type_holding)


def set_type_holding(message):
    if message.text == messages.BACK:
        telegram_main.start(message)
    elif message.text == 'иис':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.add('сейф', 'простое решение', 'иис', messages.BACK)
        globalBot.send_message(message.from_user.id, text=messages.ENTER_TYPE, reply_markup=keyboard)
        voice_assistant.send_voice_message(message, messages.ENTER_TYPE)
        globalBot.register_next_step_handler(message, set_iis)
    elif message.text == 'опиф':
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.add('опиф', 'опиф Лалэ', messages.BACK)
        globalBot.send_message(message.from_user.id, text=messages.ENTER_TYPE, reply_markup=keyboard)
        voice_assistant.send_voice_message(message, messages.ENTER_TYPE)
        globalBot.register_next_step_handler(message, set_opif)
    else:
        globalBot.send_message(message.from_user.id, messages.ENTERING_PROGRESS_MESSAGE_1)
        voice_assistant.send_voice_message(message, messages.ENTERING_PROGRESS_MESSAGE_1)
        globalBot.send_message(message.from_user.id, messages.ENTER_FIO)
        voice_assistant.send_voice_message(message, messages.ENTER_FIO)
        globalBot.register_next_step_handler(message, set_full_name)


def set_iis(message):
    if message.text == messages.BACK:
        init_holding(message, globalBot)
    else:
        globalBot.send_message(message.from_user.id, messages.ENTERING_PROGRESS_MESSAGE_1)
        voice_assistant.send_voice_message(message, messages.ENTERING_PROGRESS_MESSAGE_1)
        globalBot.send_message(message.from_user.id, messages.ENTER_FIO)
        voice_assistant.send_voice_message(message, messages.ENTER_FIO)
        globalBot.register_next_step_handler(message, set_full_name)


def set_opif(message):
    if message.text == messages.BACK:
        init_holding(message, globalBot)
    else:
        globalBot.send_message(message.from_user.id, messages.ENTERING_PROGRESS_MESSAGE_1)
        voice_assistant.send_voice_message(message, messages.ENTERING_PROGRESS_MESSAGE_1)
        globalBot.send_message(message.from_user.id, messages.ENTER_FIO)
        voice_assistant.send_voice_message(message, messages.ENTER_FIO)
        globalBot.register_next_step_handler(message, set_full_name)


def set_full_name(message):
    if len(message.text.split()) != 3:
        globalBot.send_message(message.from_user.id, messages.ENTER_FIO)
        voice_assistant.send_voice_message(message, messages.ENTER_FIO)
        globalBot.register_next_step_handler(message, set_full_name)
        return
    globalBot.send_message(message.from_user.id, messages.ENTER_PHONE_NUMBER)
    voice_assistant.send_voice_message(message, messages.ENTER_PHONE_NUMBER)
    globalBot.register_next_step_handler(message, set_phone)


def set_phone(message):
    if not phone_is_valid(message.text):
        globalBot.send_message(message.from_user.id, messages.WRONG_PHONE_FORMAT)
        voice_assistant.send_voice_message(message, messages.WRONG_PHONE_FORMAT)
        globalBot.register_next_step_handler(message, set_phone)
        return
    globalBot.send_message(message.from_user.id, messages.GOOD)
    voice_assistant.send_voice_message(message, messages.GOOD)
    telegram_main.start(message)
