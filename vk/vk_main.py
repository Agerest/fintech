import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import data
import messages
from vk.debit_card import DebitCard

vk_session = None
vk_long_poll = None


def init():
    get_session()
    get_longpoll()
    vk = vk_session.get_api()
    for event in vk_long_poll.listen():
        print(event.type)
        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event.obj.text)
            if event.obj.text == '/start':
                vk.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id,
                                 message=messages.GREETING_NEW_USERS)
                debit_card_data_grabbing(vk, event)
            else:
                inputer(vk, event)


def get_session():
    global vk_session

    if vk_session is None:
        vk_session = vk_api.VkApi(token=data.GROUP_TOKEN)
        return vk_session
    else:
        return vk_session


def get_longpoll():
    global vk_long_poll

    if vk_long_poll is None:
        vk_long_poll = VkBotLongPoll(get_session(), data.GROUP_ID, 60)
        return vk_long_poll
    else:
        return vk_long_poll


list_debits = []


def inputer(bot, event):
    appllience = get_debit_appllience(event.obj.from_id)
    if appllience == None:
        bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id,
                          message='Я не понимаю что вы хотите. Вы можете оформить заявку'
                                  ' на продукты банка введя команду ')
    else:
        appllience.set_field(bot, event, event.obj.text)


def get_debit_appllience(id):
    for x in list_debits:
        if x.telegramId == id:
            return x
    return None


def debit_card_data_grabbing(bot, event):
    if (get_debit_appllience(event.obj.from_id) == None):
        new_appllience = DebitCard(bot, event, event.obj.from_id)
        list_debits.append(new_appllience)
    else:
        bot.messages.send(user_id=event.obj.from_id, random_id=event.obj.random_id,
                          message='У вас уже оформлена заявка. Введите запрошенное поле.')
