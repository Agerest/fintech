import datetime
import json

import requests
import telebot

import data
import messages
from telegram import telegram_main


class DebitCard:
    id = ''
    firstName = ''
    middleName = ''
    lastName = ''
    birthdate = ''
    phoneNumber = ''
    email = ''
    address = ''
    passportNumber = ''
    passportSerial = ''
    passportDate = ''
    passportOrganization = ''
    type = ''


application = DebitCard
globalBot = telebot.TeleBot


# init method
def init(message, bot):
    global application
    global globalBot
    globalBot = bot
    application = DebitCard()
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.add('aurum', 'evolution', 'generation', 'akbars premium', 'классическая карта', 'мир долголетия',
                 messages.BACK)
    globalBot.send_message(message.from_user.id, text=messages.ENTER_TYPE, reply_markup=keyboard)
    globalBot.register_next_step_handler(message, set_type)


def set_type(message):
    if message.text == messages.BACK:
        telegram_main.start(message)
    else:
        application.type = message.text
        globalBot.send_message(message.from_user.id, messages.ENTERING_PROGRESS_MESSAGE_1)
        globalBot.send_message(message.from_user.id, messages.ENTER_FIO)
        globalBot.register_next_step_handler(message, set_full_name)


def set_full_name(message):
    if message.text == messages.CANCEL:
        globalBot.send_message(message.from_user.id, messages.BREAK)
        telegram_main.start(message)
    else:
        split_message = message.text
        application.lastName = split_message[0]
        application.firstName = split_message[1]
        application.middleName = split_message[2]
        globalBot.send_message(message.from_user.id, messages.ENTER_BIRTHDATE)
        globalBot.register_next_step_handler(message, set_birthdate)


def set_birthdate(message):
    if message.text == messages.CANCEL:
        globalBot.send_message(message.from_user.id, messages.BREAK)
        telegram_main.start(message)
    else:
        try:
            datetime.datetime.strptime(message.text, '%Y-%m-%d')
            application.birthdate = message.text
            globalBot.send_message(message.from_user.id, messages.ENTER_PHONE_NUMBER)
            globalBot.register_next_step_handler(message, set_phone_number)
        except ValueError:
            globalBot.send_message(message.from_user.id, messages.WRONG_DATE)
            globalBot.register_next_step_handler(message, set_birthdate)


def set_phone_number(message):
    if message.text == messages.CANCEL:
        globalBot.send_message(message.from_user.id, messages.BREAK)
        telegram_main.start(message)
    else:
        application.phoneNumber = message.text
        result = {'debitCard': json.dumps(application.__dict__), 'telegramId': message.from_user.id, 'userType': 'tlg'}
        response = requests.post(data.CUBA_HOST + data.CREATE_DEBIT_URL,
                                 json=result, headers={'content-type': 'application/json'})
        code = response.status_code
        print(code)
        if code == 200:
            application.id = response.text
            globalBot.send_message(message.from_user.id, messages.HALF)
            globalBot.send_message(message.from_user.id, messages.ENTER_EMAIL)
            globalBot.register_next_step_handler(message, set_email)
        else:
            globalBot.send_message(message.from_user.id, messages.FAILED)


def set_email(message):
    if message.text == messages.CANCEL:
        send_application(message)
        telegram_main.start(message)
    else:
        application.email = message.text
        globalBot.send_message(message.from_user.id, messages.ENTER_ADDRESS)
        globalBot.register_next_step_handler(message, set_address)


def set_address(message):
    if message.text == messages.CANCEL:
        send_application(message)
        telegram_main.start(message)
    else:
        application.address = message.text
        globalBot.send_message(message.from_user.id, messages.ENTER_PASSPORT_DATA)
        globalBot.register_next_step_handler(message, set_passport_number_and_serial)


def set_passport_number_and_serial(message):
    if message.text == messages.CANCEL:
        send_application(message)
        telegram_main.start(message)
    else:
        if application.passportNumber == '':
            split_message = message.text
            application.passportNumber = split_message[0]
            application.passportSerial = split_message[1]
        globalBot.send_message(message.from_user.id, messages.ENTER_PASSPORT_DATE)
        globalBot.register_next_step_handler(message, set_passport_date)


def set_passport_date(message):
    if message.text == messages.CANCEL:
        send_application(message)
        telegram_main.start(message)
    else:
        try:
            datetime.datetime.strptime(message.text, '%Y-%m-%d')
            application.passportDate = message.text
            globalBot.send_message(message.from_user.id, messages.ENTER_PASSPORT_ORGANIZATION)
            globalBot.register_next_step_handler(message, set_passport_organization)
        except ValueError:
            globalBot.send_message(message.from_user.id, messages.WRONG_DATE)
            globalBot.register_next_step_handler(message, set_passport_date)


# final method
def set_passport_organization(message):
    if message.text == messages.CANCEL:
        send_application(message)
        telegram_main.start(message)
    else:
        application.passportOrganization = message.text
        application.telegramId = message.from_user.id
        send_application(message)
        telegram_main.start(message)


def send_application(message):
    result = {'debitCard': json.dumps(application.__dict__)}
    response = requests.post(data.CUBA_HOST + data.CREATE_DEBIT_FULL_URL,
                             json=result, headers={'content-type': 'application/json'})
    code = response.status_code
    print(code)
    if code == 200:
        json_response = response.json()
        globalBot.send_message(message.from_user.id, messages.SUCCESSFUL_APPLICATION + json_response['id'])
    else:
        globalBot.send_message(message.from_user.id, messages.FAILED)
