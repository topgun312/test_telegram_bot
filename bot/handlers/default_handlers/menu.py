import random
from datetime import date, datetime, timedelta
from database.db_work import create_club, create_match, create_person, create_proposals, create_myproposals
from database.postgres_db import Club, ProfileUser, session
from keyboards.inline.inline_keyboard import (
    club_selected,
    clubs_inline,
    coming_request,
    gender_inline,
    live_com_inline,
    match_inline,
    politics_inline,
    profile_inline,
    request_me_inline,
)
from loader import bot
from sqlalchemy import not_
from sqlalchemy_file import File
from states.chats_information import ChatsFriendInfo
from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove


proposals = {}
pr_time = date.today()
block_profile = []


def proposals_count(pr):
    res = pr + 1
    return res


@bot.message_handler(content_types=["text"])
def bot_start_message(message: Message):
    """
    Функция для обработки reply-кнопки начала создания анкеты.
    """
    if message.text == "Создать":
        bot.set_state(message.from_user.id, ChatsFriendInfo.city, message.chat.id)
        bot.send_message(
            message.from_user.id, "Выберите город:", reply_markup=ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(message, enter_city)


@bot.message_handler(state=ChatsFriendInfo.city)
def enter_city(message: Message):
    """
    Функция получения города проживания пользователя и сохранения в класс состояний пользователя.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isalpha():
            data["city"] = message.text
            bot.send_message(message.from_user.id, "Имя:")
            bot.set_state(message.from_user.id, ChatsFriendInfo.name, message.chat.id)
            bot.register_next_step_handler(message, enter_name)
        else:
            bot.send_message(
                message.from_user.id, "Город должен содержать только буквы"
            )


@bot.message_handler(state=ChatsFriendInfo.name)
def enter_name(message: Message) -> None:
    """
    Функция получения имени пользователя и сохранения в класс состояний пользователя.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isalpha():
            data["name"] = message.text
            bot.send_message(message.from_user.id, "Фамилия:")
            bot.set_state(
                message.from_user.id, ChatsFriendInfo.surname, message.chat.id
            )
            bot.register_next_step_handler(message, enter_surname)
        else:
            bot.send_message(message.from_user.id, "Имя должно содержать только буквы")


@bot.message_handler(state=ChatsFriendInfo.surname)
def enter_surname(message: Message):
    """
    Функция получения фамилии пользователя и сохранения в класс состояний пользователя.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isalpha():
            data["surname"] = message.text
            bot.send_message(
                message.from_user.id, "Дата рождения (формат - дд.мм.гггг):"
            )
            bot.set_state(
                message.from_user.id, ChatsFriendInfo.birthday, message.chat.id
            )
            bot.register_next_step_handler(message, enter_birthday)
        else:
            bot.send_message(
                message.from_user.id, "Фамилия должна содержать только буквы"
            )


@bot.message_handler(state=ChatsFriendInfo.birthday)
def enter_birthday(message: Message):
    """
    Функция получения даты рождения пользователя и сохранения в класс состояний пользователя.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        format = "%d.%m.%Y"
        today = datetime.today()
        true_date = datetime.strptime(message.text, format)
        result = True
        if result == bool(true_date) and true_date < today:
            data["birthday"] = message.text
            bot.send_message(message.from_user.id, "Пол:", reply_markup=gender_inline())
            bot.set_state(message.from_user.id, ChatsFriendInfo.gender, message.chat.id)
        else:
            bot.send_message(
                message.from_user.id,
                "Дата должна быть введена в формате дд.мм.гггг и не превышать текущую дату",
            )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith("gender"), state=ChatsFriendInfo.gender
)
def enter_gender(call: CallbackQuery):
    """
    Функция получения пола пользователя и сохранения в класс состояний пользователя.
    """
    if call.message:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            for row in call.message.json["reply_markup"]["inline_keyboard"]:
                data["gender"] = row[0]["text"]
            bot.send_message(
                call.message.chat.id,
                "Хотите общаться в живую?",
                reply_markup=live_com_inline(),
            )
            bot.set_state(
                call.message.from_user.id,
                ChatsFriendInfo.live_communication,
                call.message.chat.id,
            )


@bot.callback_query_handler(func=lambda call: call.data.startswith("answer"))
def enter_live_communication(call: CallbackQuery):
    """
    Функция получения желания общаться вживую и сохранения в класс состояний пользователя.
    """
    if call.data:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            for row in call.message.json["reply_markup"]["inline_keyboard"]:
                data["live_communication"] = row[0]["text"]
            bot.send_message(call.message.chat.id, "Кем и в ĸаĸой сфере вы работаете?")
            bot.set_state(
                call.message.from_user.id, ChatsFriendInfo.work, call.message.chat.id
            )
            bot.register_next_step_handler(call.message, enter_work)


@bot.message_handler(state=ChatsFriendInfo.work)
def enter_work(message: Message):
    """
    Функция получения профессии пользователя и сохранения в класс состояний пользователя.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isalpha():
            data["work"] = message.text
            bot.send_message(
                message.from_user.id, "О чем вы много знаете и будете рады поделиться?"
            )
            bot.set_state(
                message.from_user.id, ChatsFriendInfo.knowledge, message.chat.id
            )
            bot.register_next_step_handler(message, enter_knowledge)
        else:
            bot.send_message(message.from_user.id, "Введите данные о работе текстом")


@bot.message_handler(state=ChatsFriendInfo.knowledge)
def enter_knowledge(message: Message):
    """
    Функция получения знаний пользователя и сохранения в класс состояний пользователя.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isalpha():
            data["knowledge"] = message.text
            bot.send_message(
                message.from_user.id, "За что вы гордитесь собой больше всего?"
            )
            bot.set_state(message.from_user.id, ChatsFriendInfo.pride, message.chat.id)
            bot.register_next_step_handler(message, enter_pride)
        else:
            bot.send_message(
                message.from_user.id, "Опишите текстом пожалуйста свои знания"
            )


@bot.message_handler(state=ChatsFriendInfo.pride)
def enter_pride(message: Message):
    """
    Функция получения достижений пользователя и сохранения в класс состояний пользователя.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isalpha():
            data["pride"] = message.text
            bot.send_message(
                message.from_user.id,
                "Любите поспорить о политиĸе?",
                reply_markup=politics_inline(),
            )
            bot.set_state(
                message.from_user.id,
                ChatsFriendInfo.politics_conversations,
                message.chat.id,
            )
        else:
            bot.send_message(
                message.from_user.id, "Опишите текстом пожалуйста свои достижения"
            )


@bot.callback_query_handler(func=lambda call: call.data.startswith("politics"))
def enter_politics(call: CallbackQuery):
    """
    Функция получения интереса в политических вопросах и сохранения в класс состояний пользователя.
    """
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        for row in call.message.json["reply_markup"]["inline_keyboard"]:
            data["politics_conversations"] = row[0]["text"]
        bot.send_message(call.message.chat.id, "Загрузите свое фото")
        bot.set_state(
            call.message.from_user.id, ChatsFriendInfo.photo, call.message.chat.id
        )
        bot.register_next_step_handler(call.message, enter_photo)


@bot.message_handler(content_types=["photo"], state=ChatsFriendInfo.photo)
def enter_photo(message: Message):
    """
    Функция получения изображения и создание анкеты пользователя.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.photo:
            file = File(
                content_type="image/jpeg",
                filename=f"{message.photo[0].file_unique_id}",
                content=f"{message.photo[0]}",
            )
            data["photo"] = file
            bot.send_message(
                message.from_user.id,
                "Отлично, ваша анĸета создана, вы всегда можете посмотреть ее и отредаĸтировать в настройĸах",
            )
            bot.send_message(
                message.from_user.id,
                "Теперь выберите ĸлубы по интересам, в ĸоторых вы будете знаĸомиться. \n"
                "Чем больше узĸий будет интерес, тем больше вероятность, что вы найдете общий языĸ.\n"
                "Вступите в ĸлубы:",
                reply_markup=clubs_inline(),
            )
            person_data = {
                "city": data["city"],
                "name": data["name"],
                "surname": data["surname"],
                "birthday": data["birthday"],
                "gender": data["gender"],
                "live_communication": data["live_communication"],
                "work": data["work"],
                "knowledge": data["knowledge"],
                "pride": data["pride"],
                "status": "admin",
                "politics_conversations": data["politics_conversations"],
                "tg_id": message.chat.id,
                "tg_account": message.chat.first_name,
                "photo": data["photo"],
            }
            create_person(person_data)
        else:
            bot.send_message(message.from_user.id, "Загрузите свое фото пожалуйста")


@bot.callback_query_handler(func=lambda call: call.data.startswith("club"))
def clubs_choosing(call: CallbackQuery):
    """
    Функция для выбора клуба и вступления в него.
    """
    if call.data:
        club_id = call.data.split("-")[1]
        for row in call.message.json["reply_markup"]["inline_keyboard"]:
            if call.data == row[0]["callback_data"]:
                bot.send_message(
                    call.message.chat.id,
                    f'Вы вступили в ĸлуб «{row[0]["text"].split(",")[0]}»!',
                    reply_markup=club_selected(club_id),
                )
                club = session.query(Club).get(club_id)
                my_profile = session.query(ProfileUser).filter(
                    ProfileUser.tg_id == call.message.chat.id
                )
                club.profileusers.extend(my_profile)
                session.commit()


@bot.callback_query_handler(func=lambda call: call.data.startswith("delete"))
def admin_delete_club(call: CallbackQuery):
    """
    Функция для удаления клуба администратором.
    """
    if call.data:
        club = session.query(Club).get(int(call.data.split("-")[1]))
        profile = session.query(ProfileUser).get(club.id_creator)
        bot.send_message(
            call.message.chat.id,
            f"{profile.name} {profile.surname} . Ваш ĸлуб {club.club_name} удален администратором, таĸ ĸаĸ нарушает правила использования ботов",
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("block"))
def admin_block_profile(call: CallbackQuery):
    """
    Функция для блокирования пользователей администратором.
    """
    if call.data:
        profile_id = call.data.split("-")[1]
        profile = (
            session.query(ProfileUser).filter(ProfileUser.id == profile_id).first()
        )
        block_profile.append(profile)
        bot.message_handler(
            call.message.chat.id,
            f"Пользователь {profile.name} {profile.surname} заблокирован.",
        )


@bot.callback_query_handler(func=lambda call: call.data == "new_club")
def clubs_enter(call: CallbackQuery):
    """
    Функция для получения названия при создании нового клуба.
    """
    if call.message:
        bot.send_message(call.message.chat.id, "Введите название клуба")
        bot.register_next_step_handler(call.message, create_new_club)


def create_new_club(message: Message):
    """
    Функция создания нового клуба.
    """
    profile = (
        session.query(ProfileUser)
        .filter(ProfileUser.tg_id == message.from_user.id)
        .first()
    )
    if message.text:
        club_data = {
            "profile": profile,
            "id_creator": profile.id,
            "admin": profile.name,
            "club_name": message.text,
        }
        create_club(club_data)
        bot.send_message(
            message.chat.id,
            f"Вы создали новый клуб - {message.text}! \n" "Вступите в ĸлубы:",
            reply_markup=clubs_inline(),
        )
    else:
        bot.send_message(message.from_user.id, "Введите название клуба пожалуйста")


@bot.callback_query_handler(func=lambda call: call.data.startswith("select"))
def go_clubs(call: CallbackQuery):
    """
    Функция для просмотра участников клуба.
    """
    if call.data:
        club = session.query(Club).get(int(call.data.split("-")[1]))
        bot.send_message(
            call.message.chat.id, f"Клуб «{club.club_name}» - {str(club.profile_quantity())} 👤"
        )
        club_profiles = club.profileusers
        for profile in club_profiles:
            if profile not in block_profile:
                club_name = ", ".join([pr.club_name for pr in profile.clubs])
                pr_info = (
                    f"{profile.name} {profile.surname}, {profile.gender}, {str(profile.get_age())} 🗣 \n"
                    + f"Работаю: {profile.work} \n"
                    + f"Знаю: {profile.knowledge} \n"
                    + f"Горжусь: {profile.pride} \n"
                    + f"Спорить о политике: {profile.politics_conversations} \n"
                    + f"Состоит в : {club_name}"
                )
                photo = eval(profile.photo.file.read())
                if profile.tg_id != call.message.chat.id:
                    bot.send_photo(
                        call.message.chat.id,
                        photo=photo["file_id"],
                        caption=pr_info,
                        reply_markup=profile_inline(str(profile.id)),
                    )
                else:
                    bot.send_photo(
                        call.message.chat.id,
                        photo=photo["file_id"],
                        caption=pr_info,
                        reply_markup=coming_request(),
                    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("profile"))
def knowledge_request(call: CallbackQuery):
    """
    Функция для отправки запроса на дружбу, игнорирования пользователя и просмотра запроса на знакомства от пользователей.
    """
    if call.data.startswith("profile-request"):
        global proposals
        global pr_time
        if pr_time != date.today():
            proposals = {}
        if call.message.from_user.id not in proposals:
            proposals[call.message.from_user.id] = 0
        if proposals[call.message.from_user.id] > 5:
            bot.send_message(
                call.message.from_user.id,
                f"Твой лимит в 5 запросов на дружбу исчерпан!\nПопробуй "
                + str(date.today() + timedelta(days=1)),
            )
        else:
            receiving_user = (
                session.query(ProfileUser)
                .filter(ProfileUser.id == call.data.split("-")[2])
                .first()
            )
            sending_user = (
                session.query(ProfileUser)
                .filter(ProfileUser.tg_id == call.message.chat.id)
                .first()
            )
            if receiving_user not in block_profile:
                bot.send_message(
                    call.message.chat.id,
                    f"Запрос на знаĸомство с {receiving_user.name} {receiving_user.surname} отправлен, "
                    "а он получит уведомление с вашей анĸетой",
                    reply_markup=match_inline(receiving_user.id),
                )
                proposals_count(proposals[call.message.from_user.id])
                proposals_data = {
                    "receiving_user": f"{receiving_user.name} {receiving_user.surname}",
                    "sending_user": f"{sending_user.name} {sending_user.surname}",
                }
                create_myproposals(proposals_data)

    elif call.data.startswith("profile-close"):
        bot.send_message(
            call.message.chat.id,
            "Вы больше не увидите этого пользователя в ваших ĸлубах, а он не будет видеть вас",
        )

    elif call.data == "profile-propolas":
        profiles = (
            session.query(ProfileUser)
            .filter(not_(ProfileUser.tg_id == call.message.chat.id))
            .all()
        )
        profile = random.choice(profiles)
        if profile not in block_profile:
            club_name = ", ".join([pr.club_name for pr in profile.clubs])
            pr_info = (
                f"{profile.name} {profile.surname}, {profile.gender}, {profile.get_age()} 🗣 \n"
                + f"Работаю: {profile.work} \n"
                + f"Знаю: {profile.knowledge} \n"
                + f"Горжусь: {profile.pride} \n"
                + f"Спорить о политике: {profile.politics_conversations} \n"
                + f"Состоит в : {club_name}"
            )
            photo = eval(profile.photo.file.read())
            bot.send_photo(
                call.message.chat.id,
                photo=photo["file_id"],
                caption="C вами хочет познакомиться: \n" + pr_info,
                reply_markup=request_me_inline(profile.id),
            )

            receiving_user = (
                session.query(ProfileUser)
                .filter(ProfileUser.tg_id == call.message.chat.id)
                .first()
            )
            proposals_data = {
                "receiving_user": f"{receiving_user.name} {receiving_user.surname}",
                "sending_user": f"{profile.name} {profile.surname}",
            }
            create_proposals(proposals_data)


@bot.callback_query_handler(func=lambda call: call.data.startswith("request"))
def me_request(call: CallbackQuery):
    """
    Функция для отображения согласия на дружбу.
    """
    if call.data.startswith("request-contact"):
        user = (
            session.query(ProfileUser)
            .filter(ProfileUser.id == call.data.split("-")[2])
            .first()
        )
        bot.send_message(
            call.message.chat.id,
            f"Вы согласились познаĸомиться с {user.name} {user.surname}.\
    Вот его ĸонтаĸт: @{user.tg_account}. Он будет рад увидеть ваше приветствие",
        )
    elif call.data == "request-decline":
        bot.send_message(call.message.chat.id, "Вы отклонили предложение о дружбе")


@bot.callback_query_handler(func=lambda call: call.data.startswith("match"))
def match(call: CallbackQuery):
    """
    Функция для просмотра мэтча.
    """
    receiving_user = (
        session.query(ProfileUser)
        .filter(ProfileUser.id == call.data.split("-")[1])
        .first()
    )
    sending_user = (
        session.query(ProfileUser)
        .filter(ProfileUser.tg_id == call.message.chat.id)
        .first()
    )
    if receiving_user not in block_profile:
        club_name = ", ".join([pr.club_name for pr in receiving_user.clubs])
        user_info = (
            f"{receiving_user.name} {receiving_user.surname}, {receiving_user.gender}, {receiving_user.get_age()} 🗣 \n"
            + f"Работаю: {receiving_user.work} \n"
            + f"Знаю: {receiving_user.knowledge} \n"
            + f"Горжусь: {receiving_user.pride} \n"
            + f"Спорить о политике: {receiving_user.politics_conversations} \n"
            + f"Состоит в :{club_name} \n"
            + f"Его ĸонтаĸт: @{receiving_user.tg_account}"
        )
        photo = eval(receiving_user.photo.file.read())
        bot.send_photo(
            call.message.chat.id,
            photo=photo["file_id"],
            caption="Ваше желание познаĸомиться поддержал: \n" + user_info,
            reply_markup=request_me_inline(receiving_user.id),
        )
        match_data = {
            "receiving_user": f"{receiving_user.name} {receiving_user.surname}",
            "sending_user": f"{sending_user.name} {sending_user.surname}",
        }
        create_match(match_data)
