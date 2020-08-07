import datetime
import json

import requests

import data
import messages


class CardBase:
    telegramId = None
    firstName = None
    middleName = None
    lastName = None
    birthdate = None
    phoneNumber = None
    email = None
    address = None
    passportNumber = None
    passportSerial = None
    passportDate = None
    passportOrganization = None


def date_is_valid(value):
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False


class DebitCard(CardBase):

    def __init__(self, bot, event, id):
        bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id, message=messages.ENTER_FIRST_NAME)
        self.telegramId = id

    def set_field(self, bot, event, value):
        if self.firstName is None:
            self.firstName = value
            bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id,
                              message=messages.ENTER_MIDDLE_NAME)
        elif self.middleName is None:
            self.middleName = value
            bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id,
                              message=messages.ENTER_LAST_NAME)
        elif self.lastName is None:
            self.lastName = value
            bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id,
                              message=messages.ENTER_BIRTHDATE)
        elif self.birthdate is None:
            if date_is_valid(value):
                self.birthdate = value
                bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id,
                                  message=messages.ENTER_PHONE_NUMBER)
            else:
                bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id, message=messages.WRONG_DATE)
        elif self.phoneNumber is None:
            self.phoneNumber = value
            bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id, message=messages.ENTER_EMAIL)
        elif self.email is None:
            self.email = value
            bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id, message=messages.ENTER_ADDRESS)
        elif self.address is None:
            self.address = value
            bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id,
                              message=messages.ENTER_PASSPORT_DATA)
        elif self.passportNumber is None:
            local_data = value.split()
            self.passportNumber = local_data[1]
            self.passportSerial = local_data[0]
            bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id,
                              message=messages.ENTER_PASSPORT_DATE)
        elif self.passportDate is None:
            if date_is_valid(value):
                self.passportDate = value
                bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id,
                                  message=messages.ENTER_PASSPORT_ORGANIZATION)
            else:
                bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id, message=messages.WRONG_DATE)
        elif self.passportOrganization is None:
            self.passportOrganization = value
            result = {'debitCard': json.dumps(self.__dict__), 'telegramId': event.obj.from_id}
            response = requests.post(data.CUBA_HOST + data.CREATE_DEBIT_URL,
                                     json=result, headers={'content-type': 'application/json'})
            code = response.status_code
            print(code)
            if code == 200:
                bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id,
                                  message=messages.SUCCESSFUL_APPLICATION + response.text)
            else:
                bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id, message=messages.FAILED)
