from database.postgres_db import Club, ProfileUser, session
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def gender_inline() -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры при выборе пола.
    """
    markup = InlineKeyboardMarkup(row_width=2)
    item_1 = InlineKeyboardButton(text="Мужской", callback_data="gender-man")
    item_2 = InlineKeyboardButton(text="Женский", callback_data="gender-woman")
    markup.add(item_1, item_2)
    return markup


def live_com_inline() -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры при выборе коммуникативности.
    """
    markup = InlineKeyboardMarkup(row_width=2)
    item_1 = InlineKeyboardButton(text="Да", callback_data="answer-yes")
    item_2 = InlineKeyboardButton(text="Нет", callback_data="answer-no")
    markup.add(item_1, item_2)
    return markup


def politics_inline() -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры при выборе политических интересов.
    """
    markup = InlineKeyboardMarkup(row_width=2)
    item_1 = InlineKeyboardButton(text="Да", callback_data="politics-yes")
    item_2 = InlineKeyboardButton(text="Нет", callback_data="politics-no")
    markup.add(item_1, item_2)
    return markup


def clubs_inline() -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры всех клубов.
    """
    markup = InlineKeyboardMarkup(row_width=1)
    clubs = session.query(Club).all()
    for i in range(0, len(clubs)):
        markup.add(
            InlineKeyboardButton(
                text=f"{clubs[i].club_name}, {str(clubs[i].profile_quantity())} 👤",
                callback_data=f"club-{str(clubs[i].id)}",
            )
        )
    item = InlineKeyboardButton(text="Создать новый", callback_data="new_club")
    markup.add(item)
    return markup


def club_selected(club_id) -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры при выборе определенного клуба.
    """
    admin = session.query(ProfileUser).filter(ProfileUser.status == "admin").all()
    markup = InlineKeyboardMarkup(row_width=1)
    item_1 = InlineKeyboardButton(
        text="Перейти в клуб", callback_data=f"select-{str(club_id)}"
    )
    item_2 = InlineKeyboardButton(text="Покинуть клуб", callback_data="leave")
    markup.add(item_1, item_2)
    if admin:
        item_3 = InlineKeyboardButton(
            text="Удалить", callback_data=f"delete-{str(club_id)}"
        )
        markup.add(item_3)
    return markup


def profile_inline(profile_id) -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры анкеты пользователя.
    """
    admin = session.query(ProfileUser).filter(ProfileUser.status == "admin").all()
    markup = InlineKeyboardMarkup(row_width=1)
    item_1 = InlineKeyboardButton(
        text="✅ Отправить запрос на знаĸомство",
        callback_data=f"profile-request-{profile_id}",
    )
    item_2 = InlineKeyboardButton(text="Предыдущая анĸета", callback_data=f"to-left")
    item_3 = InlineKeyboardButton(text="Следующая анĸета", callback_data=f"to-right")
    item_4 = InlineKeyboardButton(
        text="❌ Сĸрыть эту анĸету из поисĸа",
        callback_data=f"profile-close-{profile_id}",
    )
    item_5 = InlineKeyboardButton(
        text="Пожаловаться на анĸету", callback_data="profile-complain"
    )
    markup.add(item_1, item_2, item_3, item_4, item_5)
    if admin:
        item_7 = InlineKeyboardButton(
            text="Заблокировать", callback_data=f"block-{profile_id}"
        )
        markup.add(item_7)
    return markup


def coming_request() -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры для просмотра запроса.
    """
    markup = InlineKeyboardMarkup(row_width=1)
    item = InlineKeyboardButton(
        text="🫂 С вами хотят познакомиться", callback_data="profile-propolas"
    )
    markup.add(item)
    return markup


def request_me_inline(profile_id) -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры для принятия или отклонения дружбы.
    """
    markup = InlineKeyboardMarkup(row_width=1)
    item_1 = InlineKeyboardButton(
        text="✅ Обменяться ĸонтаĸтами", callback_data=f"request-contact-{profile_id}"
    )
    item_2 = InlineKeyboardButton(
        text="❌ Отĸлонить предложение", callback_data="request-decline"
    )
    markup.add(item_1, item_2)
    return markup


def match_inline(profile_id) -> InlineKeyboardMarkup:
    """
    Функция для формирования инлайн-клавиатуры при просмотре мэтча.
    """
    markup = InlineKeyboardMarkup(row_width=1)
    item = InlineKeyboardButton(
        text="Посмотреть запрос", callback_data=f"match-{profile_id}"
    )
    markup.add(item)
    return markup
