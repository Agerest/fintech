import datetime
import json

import requests

import data
import messages


class CreditCard:
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
    workPlace = ''
    workExperience = ''
    monthlyIncome = ''
    employerAddress = ''
    employerPhoneNumber = ''
    maritalStatus = ''
    telegramId = ''


application = None
globalBot = None


# init method
def init(message, bot):
    global application
    global globalBot
    globalBot = bot
    application = CreditCard()
    globalBot.send_message(message.from_user.id, messages.ENTER_FIRST_NAME)
    globalBot.register_next_step_handler(message, set_first_name)


def set_first_name(message):
    global globalBot
    application.firstName = message.text
    globalBot.send_message(message.from_user.id, messages.ENTER_LAST_NAME)
    globalBot.register_next_step_handler(message, set_last_name)


def set_last_name(message):
    application.lastName = message.text
    globalBot.send_message(message.from_user.id, messages.ENTER_MIDDLE_NAME)
    globalBot.register_next_step_handler(message, set_middle_name)


def set_middle_name(message):
    if application.middleName == '':
        application.middleName = message.text
    globalBot.send_message(message.from_user.id, messages.ENTER_BIRTHDATE)
    globalBot.register_next_step_handler(message, set_birthdate)


def set_birthdate(message):
    try:
        datetime.datetime.strptime(message.text, '%Y-%m-%d')
        application.birthdate = message.text
        globalBot.send_message(message.from_user.id, messages.ENTER_PHONE_NUMBER)
        globalBot.register_next_step_handler(message, set_phone_number)
    except ValueError:
        globalBot.send_message(message.from_user.id, messages.WRONG_DATE)
        globalBot.register_next_step_handler(message, set_birthdate)


def set_phone_number(message):
    application.phoneNumber = message.text
    result = {'creditCard': json.dumps(application.__dict__)}
    response = requests.post(data.CUBA_HOST + data.CREATE_CREDIT_URL,
                             json=result, headers={'content-type': 'application/json'})
    code = response.status_code
    print(code)
    if code == 200:
        globalBot.send_message(message.from_user.id, messages.ENTER_EMAIL)
        globalBot.register_next_step_handler(message, set_email)
    else:
        globalBot.send_message(message.from_user.id, messages.FAILED)


def set_email(message):
    application.email = message.text
    globalBot.send_message(message.from_user.id, messages.ENTER_ADDRESS)
    globalBot.register_next_step_handler(message, set_address)


def set_address(message):
    application.address = message.text
    globalBot.send_message(message.from_user.id, messages.ENTER_PASSPORT_DATA)
    globalBot.register_next_step_handler(message, set_passport_number_and_serial)


def set_passport_number_and_serial(message):
    if application.passportNumber == '':
        split_message = message.text
        application.passportNumber = split_message[0]
        application.passportSerial = split_message[1]
    globalBot.send_message(message.from_user.id, messages.ENTER_PASSPORT_DATE)
    globalBot.register_next_step_handler(message, set_passport_date)


def set_passport_date(message):
    try:
        datetime.datetime.strptime(message.text, '%Y-%m-%d')
        application.passportDate = message.text
        globalBot.send_message(message.from_user.id, messages.ENTER_PASSPORT_ORGANIZATION)
        globalBot.register_next_step_handler(message, set_passport_organization)
    except ValueError:
        globalBot.send_message(message.from_user.id, messages.WRONG_DATE)
        globalBot.register_next_step_handler(message, set_passport_date)


def set_passport_organization(message):
    application.passportOrganization = message.text
    globalBot.send_message(message.from_user.id, messages.ENTER_WORK_PLACE)
    globalBot.register_next_step_handler(message, set_work_place)


def set_work_place(message):
    application.workPlace = message.text
    globalBot.send_message(message.from_user.id, messages.ENTER_WORK_EXPERIENCE)
    globalBot.register_next_step_handler(message, set_work_experience)


def set_work_experience(message):
    application.workExperience = message.text
    globalBot.send_message(message.from_user.id, messages.ENTER_MONTHLY_INCOME)
    globalBot.register_next_step_handler(message, set_monthly_income)


def set_monthly_income(message):
    application.monthlyIncome = message.text
    globalBot.send_message(message.from_user.id, messages.ENTER_EMPLOYER_ADDRESS)
    globalBot.register_next_step_handler(message, set_employer_address)


def set_employer_address(message):
    application.employerAddress = message.text
    globalBot.send_message(message.from_user.id, messages.ENTER_EMPLOYER_PHONE_NUMBER)
    globalBot.register_next_step_handler(message, set_employer_phone_number)


def set_employer_phone_number(message):
    application.employerPhoneNumber = message.text
    globalBot.send_message(message.from_user.id, messages.ENTER_MARITAL_STATUS)
    globalBot.register_next_step_handler(message, set_marital_status)


# final method
def set_marital_status(message):
    application.maritalStatus = message.text
    application.telegramId = message.from_user.id
    result = {'creditCard': json.dumps(application.__dict__)}
    response = requests.post(data.CUBA_HOST + data.CREATE_CREDIT_FULL_URL,
                             json=result, headers={'content-type': 'application/json'})
    code = response.status_code
    print(code)
    if code == 200:
        globalBot.send_message(message.from_user.id, messages.SUCCESSFUL_APPLICATION + response.text)
    else:
        globalBot.send_message(message.from_user.id, messages.FAILED)
