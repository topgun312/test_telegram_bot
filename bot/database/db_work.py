from database.postgres_db import Club, Match, ProfileUser, Proposals, MyProposals, session
from sqlalchemy_file import File


def create_person(data):
    """
    Функция для создания пользователя.
    """
    data_person = ProfileUser(
        city=data["city"],
        name=data["name"],
        surname=data["surname"],
        birthday=data["birthday"],
        gender=data["gender"],
        live_communication=data["live_communication"],
        work=data["work"],
        knowledge=data["knowledge"],
        pride=data["pride"],
        politics_conversations=data["politics_conversations"],
        tg_id=data["tg_id"],
        tg_account=data["tg_account"],
        photo=data["photo"],
        status=data["status"],
    )
    session.add(data_person)
    session.commit()
    print(f"Данные пользователя добавлены")


def create_club(data):
    """
    Функция для создания клуба.
    """
    data_club = Club(
        profileusers=[data["profile"]],
        id_creator=data["id_creator"],
        admin=[data["admin"]],
        club_name=data["club_name"],
    )

    session.add(data_club)
    session.commit()
    print(f"Данные нового клуба добавлены")


def create_proposals(data):
    """
    Функция для создания запроса на знакомства.
    """
    proposals_data = Proposals(
        receiving_user=data["receiving_user"], sending_user=data["sending_user"]
    )
    session.add(proposals_data)
    session.commit()
    print(f"Данные запроса добавлены")


def create_myproposals(data):
    """
    Функция для создания запроса на знакомства.
    """
    proposals_data = MyProposals(
        receiving_user=data["receiving_user"], sending_user=data["sending_user"]
    )
    session.add(proposals_data)
    session.commit()
    print(f"Данные моего запроса добавлены")


def create_match(data):
    """
    Функция для создания мэтча.
    """
    match_data = Match(
        sending_user=data["sending_user"], receiving_user=data["receiving_user"]
    )
    session.add(match_data)
    session.commit()
    print(f"Данные мэтча добавлены")


def create_default_profiles():
    """
    Функция для создания тестовых пользователей.
    """
    photo_1 = {
        "file_id": "AgACAgIAAxkBAAIU92WriFcqTqht2Rb68NLZTQayi4JBAAL_2jEbLHhgSbIYpvTdwFXQAQADAgADcwADNAQ",
        "file_unique_id": "AQAD_9oxGyx4YEl4",
        "width": 58,
        "height": 90,
        "file_size": 1010,
    }
    photo_2 = {
        "file_id": "AgACAgIAAxkBAAIVEGWriSh2NnGIPrquwSCAC-QGzP4hAAIL2zEbLHhgSRFUldpTH1vpAQADAgADcwADNAQ",
        "file_unique_id": "AQADC9sxGyx4YEl4",
        "width": 68,
        "height": 90,
        "file_size": 1284,
    }
    photo_3 = {
        "file_id": "AgACAgIAAxkBAAIVPmWrixVN1d7UCH5V0ETqgit7BYO3AAIY2zEbLHhgSWRS3mep7JEEAQADAgADcwADNAQ",
        "file_unique_id": "AQADGNsxGyx4YEl4",
        "width": 79,
        "height": 90,
        "file_size": 1343,
    }
    photo_4 = {
        "file_id": "AgACAgIAAxkBAAIVnmWrj_IRya3CvAeKOgMneQtLRKyaAAIt2zEbLHhgSeHQozOjoKGHAQADAgADcwADNAQ",
        "file_unique_id": "AQADLdsxGyx4YEl4",
        "width": 90,
        "height": 90,
        "file_size": 1357,
    }
    photo_5 = {
        "file_id": "AgACAgIAAxkBAAIVhmWrj2hsC6Ghy7v_5PHF15ihFVjOAAIr2zEbLHhgSS6dYcmeFVwaAQADAgADcwADNAQ",
        "file_unique_id": "AQADK9sxGyx4YEl4",
        "width": 60,
        "height": 90,
        "file_size": 1377,
    }
    data_person = [
        ProfileUser(
            city="Москва",
            name="Иван",
            surname="Иванов",
            birthday="22.04.1989",
            gender="Мужской",
            live_communication="Да",
            work="Учитель английского языка",
            knowledge="Знаю все об Англии и США",
            pride="Целеустремленный",
            politics_conversations="Нет",
            photo=File(
                content_type="image/jpeg",
                filename=f'{photo_1["file_unique_id"]}',
                content=f"{photo_1}",
            ),
            tg_id="1235234421",
            tg_account="ivanivanov",
            status="member",
        ),
        ProfileUser(
            city="Ростов",
            name="Егор",
            surname="Петров",
            birthday="12.09.1985",
            gender="Мужской",
            live_communication="Да",
            work="Космонавт",
            knowledge="Космонавтика и астрофизика",
            pride="Знания",
            politics_conversations="Нет",
            photo=File(
                content_type="image/jpeg",
                filename=f'{photo_2["file_unique_id"]}',
                content=f"{photo_2}",
            ),
            tg_id="1235256021",
            tg_account="egorpetrov",
            status="member",
        ),
        ProfileUser(
            city="Санкт-Петербург",
            name="Алена",
            surname="Борисова",
            birthday="22.03.1992",
            gender="Женский",
            live_communication="Да",
            work="Стюардесса",
            knowledge="О самолетах",
            pride="Внешность",
            politics_conversations="Да",
            photo=File(
                content_type="image/jpeg",
                filename=f'{photo_3["file_unique_id"]}',
                content=f"{photo_3}",
            ),
            tg_id="1389011022",
            tg_account="alenaborisova",
            status="member",
        ),
        ProfileUser(
            city="Москва",
            name="Ольга",
            surname="Петровна",
            birthday="22.04.1996",
            gender="Женский",
            live_communication="Да",
            work="Учительница",
            knowledge="Биология и химия",
            pride="Знания",
            politics_conversations="Да",
            photo=File(
                content_type="image/jpeg",
                filename=f'{photo_4["file_unique_id"]}',
                content=f"{photo_4}",
            ),
            tg_id="1669061022",
            tg_account="olgapetrovna",
            status="member",
        ),
        ProfileUser(
            city="Санкт-Петербург",
            name="Руслан",
            surname="Сидоров",
            birthday="10.02.1997",
            gender="Мужской",
            live_communication="Да",
            work="Менеджер",
            knowledge="Товары для дома",
            pride="Коммуникабельность",
            politics_conversations="нет",
            photo=File(
                content_type="image/jpeg",
                filename=f'{photo_5["file_unique_id"]}',
                content=f"{photo_5}",
            ),
            tg_id="1489991022",
            tg_account="ruslansidirov",
            status="member",
        ),
    ]
    session.add_all(data_person)
    session.commit()
    print(f"Данные 5-х пользователей по умолчанию добавлены")


def create_default_club():
    """
    Функция для создания тестовых клубов.
    """
    persons = session.query(ProfileUser).all()
    data_club = [
        Club(
            profileusers=[persons[0], persons[1]],
            id_creator=persons[0].id,
            admin=[f"{persons[0]}"],
            club_name="Программисты",
        ),
        Club(
            profileusers=[persons[1], persons[2], persons[3], persons[4]],
            id_creator=persons[3].id,
            admin=[f"{persons[3]}"],
            club_name="Книголюбы",
        ),
    ]
    session.add_all(data_club)
    session.commit()
    print(f"Добавлены 2 клуба")


def create_default_data():
    """
    Основная функция для создания тестовых данных.
    """
    create_default_profiles()
    create_default_club()
    print("Данные по умолчанию созданы")
