from icq.card_base import CardBase
import datetime
import messages
import requests
import json

import data


def date_is_valid(value):
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False


class DebitCard(CardBase):

    def __init__(self, bot, event, id):
        bot.send_text(chat_id=event.data['from']['userId'], text=messages.ENTER_FIRST_NAME)
        self.telegramId = id

    def set_field(self, bot, event, value):
        if self.firstName is None:
            self.firstName = value
            bot.send_text(chat_id=event.data['from']['userId'], text=messages.ENTER_MIDDLE_NAME)
        elif self.middleName is None:
            self.middleName = value
            bot.send_text(chat_id=event.data['from']['userId'], text=messages.ENTER_LAST_NAME)
        elif self.lastName is None:
            self.lastName = value
            bot.send_text(chat_id=event.data['from']['userId'], text=messages.ENTER_BIRTHDATE)
        elif self.birthDate is None:
            if date_is_valid(value):
                self.birthDate = value
                bot.send_text(chat_id=event.data['from']['userId'], text=messages.ENTER_PHONE_NUMBER)
            else:
                bot.send_text(chat_id=event.data['from']['userId'], text=messages.WRONG_DATE)
        elif self.phoneNumber is None:
            self.phoneNumber = value
            bot.send_text(chat_id=event.data['from']['userId'], text=messages.ENTER_EMAIL)
        elif self.email is None:
            self.email = value
            bot.send_text(chat_id=event.data['from']['userId'], text=messages.ENTER_ADDRESS)
        elif self.address is None:
            self.address = value
            bot.send_text(chat_id=event.data['from']['userId'], text=messages.ENTER_PASSPORT_DATA)
        elif self.passportNumber is None:
            data = value.split()
            self.passportNumber = data[1]
            self.passportSerial = data[0]
            bot.send_text(chat_id=event.data['from']['userId'], text=messages.ENTER_PASSPORT_DATE)
        elif self.passportDate is None:
            if date_is_valid(value):
                self.passportDate = value
                bot.send_text(chat_id=event.data['from']['userId'],
                              text=messages.ENTER_PASSPORT_ORGANIZATION)
            else:
                bot.send_text(chat_id=event.data['from']['userId'], text=messages.WRONG_DATE)
        elif self.passportOrganization is None:
            self.passportOrganization = value
        # result = {'debitCard': json.dumps(self.__dict__)}
        # response = \
        #     requests.post(data.HOST + data.CREATE_DEBIT_URL, json=result, headers={'content-type': 'application/json'})
        # code = response.status_code
        # print(code)