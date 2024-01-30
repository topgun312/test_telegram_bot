from database.postgres_db import Club, Match, ProfileUser, Proposals, MyProposals, session
from loader import bot
from telebot.types import Message


@bot.message_handler(
    commands=["clubs", "myclubs", "proposals", "myproposals", "myfriends", "settings"]
)
def menu_commands(message: Message):
    if message.text == "/clubs":
        clubs = session.query(Club).all()
        if clubs:
            bot.send_message(message.from_user.id, "Список всех клубов:")
            for club in clubs:
                print(club.profile_quantity())
                bot.send_message(
                    message.from_user.id,
                    f"Клуб «{club.club_name}» - {club.profile_quantity()} 👤",
                )
        else:
            bot.send_message(message.from_user.id, "Список клубов пуст")
    elif message.text == "/myclubs":
        pr = session.query(ProfileUser).filter(ProfileUser.tg_id == message.chat.id).first()
        clubs = pr.clubs
        if clubs:
            bot.send_message(message.from_user.id, "Список всех моих клубов:")
            for club in clubs:
                bot.send_message(
                    message.from_user.id,
                    f"Клуб «{club.club_name}» - {club.profile_quantity()} 👤",
                )
        else:
            bot.send_message(message.from_user.id, "Список клубов пуст")
    elif message.text == "/proposals":
        proposals = (
            session.query(Proposals).all()
        )
        if proposals:
            for pr in proposals:
                bot.send_message(
                    message.from_user.id,
                    f"Предложение на знакомство от {pr.sending_user}",
                )
        else:
            bot.send_message(message.from_user.id, "Список предложений пуст")
    elif message.text == "/myproposals":
        proposals = (
            session.query(MyProposals).all()
        )
        if proposals:
            for pr in proposals:
                bot.send_message(
                    message.from_user.id,
                    f"Предложение на знакомство {pr.receiving_user}",
                )
        else:
            bot.send_message(message.from_user.id, "Список предложений пуст")
    elif message.text == "/myfriends":
        friends = session.query(Match).all()
        if friends:
            bot.send_message(message.from_user.id, "Список ваших друзей:")
            for f in friends:
                text = f"{f.receiving_user}"
                bot.send_message(message.from_user.id, text)
        else:
            bot.send_message(message.from_user.id, "Список друзей пуст")
    elif message.text == "/settings":
        bot.send_message(message.from_user.id, "Настройки бота")
