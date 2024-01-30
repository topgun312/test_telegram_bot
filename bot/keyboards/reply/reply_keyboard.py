from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def start_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard = KeyboardButton("Создать")
    markup.add(keyboard)
    return markup


