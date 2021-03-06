import datetime
import json

import phonenumbers
import requests
import telebot

import data
import messages
from telegram import telegram_main, voice_assistant


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
    voice_assistant.send_voice_message(message, messages.ENTER_TYPE)
    globalBot.register_next_step_handler(message, set_type)


def set_type(message):
    if message.text == messages.BACK:
        telegram_main.start(message)
    else:
        application.type = message.text
        globalBot.send_message(message.from_user.id, messages.ENTERING_PROGRESS_MESSAGE_1)
        voice_assistant.send_voice_message(message, messages.ENTERING_PROGRESS_MESSAGE_1)
        globalBot.send_message(message.from_user.id, messages.ENTER_FIO)
        voice_assistant.send_voice_message(message, messages.ENTER_FIO)
        globalBot.register_next_step_handler(message, set_full_name)


def set_full_name(message):
    if message.text == messages.CANCEL:
        globalBot.send_message(message.from_user.id, messages.BREAK)
        voice_assistant.send_voice_message(message, messages.BREAK)
        telegram_main.start(message)
    else:
        split_message = message.text.split()
        if len(split_message) != 3:
            globalBot.send_message(message.from_user.id, messages.ENTER_FIO)
            voice_assistant.send_voice_message(message, messages.ENTER_FIO)
            globalBot.register_next_step_handler(message, set_full_name)
            return
        application.lastName = split_message[0]
        application.firstName = split_message[1]
        application.middleName = split_message[2]
        globalBot.send_message(message.from_user.id, messages.ENTER_BIRTHDATE)
        voice_assistant.send_voice_message(message, messages.ENTER_BIRTHDATE)
        globalBot.register_next_step_handler(message, set_birthdate)


def set_birthdate(message):
    if message.text == messages.CANCEL:
        globalBot.send_message(message.from_user.id, messages.BREAK)
        voice_assistant.send_voice_message(message, messages.BREAK)
        telegram_main.start(message)
    else:
        try:
            datetime.datetime.strptime(message.text, '%Y-%m-%d')
            application.birthdate = message.text
            globalBot.send_message(message.from_user.id, messages.ENTER_PHONE_NUMBER)
            voice_assistant.send_voice_message(message, messages.ENTER_PHONE_NUMBER)
            globalBot.register_next_step_handler(message, set_phone_number)
        except ValueError:
            globalBot.send_message(message.from_user.id, messages.WRONG_DATE)
            voice_assistant.send_voice_message(message, messages.WRONG_DATE)
            globalBot.register_next_step_handler(message, set_birthdate)


def phone_is_valid(value):
    try:
        x = phonenumbers.parse(value)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False
    return True


def set_phone_number(message):
    if message.text == messages.CANCEL:
        globalBot.send_message(message.from_user.id, messages.BREAK)
        voice_assistant.send_voice_message(message, messages.BREAK)
        telegram_main.start(message)
    else:
        if not phone_is_valid(message.text):
            globalBot.send_message(message.from_user.id, messages.WRONG_PHONE_FORMAT)
            voice_assistant.send_voice_message(message, messages.WRONG_PHONE_FORMAT)
            globalBot.register_next_step_handler(message, set_phone_number)
            return
        application.phoneNumber = message.text
        result = {'debitCard': json.dumps(application.__dict__), 'telegramId': message.from_user.id, 'userType': 'tlg'}
        response = requests.post(data.CUBA_HOST + data.CREATE_DEBIT_URL,
                                 json=result, headers={'content-type': 'application/json'})
        code = response.status_code
        print(code)
        if code == 200:
            application.id = response.text
            globalBot.send_message(message.from_user.id, messages.HALF)
            voice_assistant.send_voice_message(message, messages.HALF)
            globalBot.send_message(message.from_user.id, messages.ENTER_EMAIL)
            voice_assistant.send_voice_message(message, messages.ENTER_EMAIL)
            globalBot.register_next_step_handler(message, set_email)
        else:
            globalBot.send_message(message.from_user.id, messages.FAILED)
            voice_assistant.send_voice_message(message, messages.FAILED)


def set_email(message):
    if message.text == messages.CANCEL:
        send_application(message)
        telegram_main.start(message)
    else:
        application.email = message.text
        globalBot.send_message(message.from_user.id, messages.ENTER_ADDRESS)
        voice_assistant.send_voice_message(message, messages.ENTER_ADDRESS)
        globalBot.register_next_step_handler(message, set_address)


def set_address(message):
    if message.text == messages.CANCEL:
        send_application(message)
        telegram_main.start(message)
    else:
        application.address = message.text
        globalBot.send_message(message.from_user.id, messages.ENTER_PASSPORT_DATA)
        voice_assistant.send_voice_message(message, messages.ENTER_PASSPORT_DATA)
        globalBot.register_next_step_handler(message, set_passport_number_and_serial)


def set_passport_number_and_serial(message):
    if message.text == messages.CANCEL:
        send_application(message)
        telegram_main.start(message)
    else:
        if application.passportNumber == '':
            split_message = message.text.split()
            if len(split_message) != 2 or len(split_message[0]) > 4 or len(split_message[1]) > 6:
                globalBot.send_message(message.from_user.id, messages.ENTER_PASSPORT_DATA)
                voice_assistant.send_voice_message(message, messages.ENTER_PASSPORT_DATA)
                globalBot.register_next_step_handler(message, set_passport_number_and_serial)
                return
            application.passportSerial = split_message[0]
            application.passportNumber = split_message[1]
        globalBot.send_message(message.from_user.id, messages.ENTER_PASSPORT_DATE)
        voice_assistant.send_voice_message(message, messages.ENTER_PASSPORT_DATE)
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
            voice_assistant.send_voice_message(message, messages.ENTER_PASSPORT_ORGANIZATION)
            globalBot.register_next_step_handler(message, set_passport_organization)
        except ValueError:
            globalBot.send_message(message.from_user.id, messages.WRONG_DATE)
            voice_assistant.send_voice_message(message, messages.WRONG_DATE)
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
        voice_assistant.send_voice_message(message, messages.SUCCESSFUL_APPLICATION)
    else:
        globalBot.send_message(message.from_user.id, messages.FAILED)
        voice_assistant.send_voice_message(message, messages.FAILED)
