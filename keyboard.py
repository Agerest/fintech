import telebot

WELCOME = telebot.types.ReplyKeyboardMarkup(True, True)
WELCOME.row("Кредитная карта", "Дебетовая карта", "Потребительский кредит")
