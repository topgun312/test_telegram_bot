from telebot.handler_backends import State, StatesGroup


class ChatsFriendInfo(StatesGroup):
    """
    Класс состояний пользователя.
    """

    city = State()
    name = State()
    surname = State()
    birthday = State()
    gender = State()
    live_communication = State()
    work = State()
    knowledge = State()
    pride = State()
    politics_conversations = State()
    photo = State()
