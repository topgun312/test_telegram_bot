from datetime import date, datetime
from config_data import config
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    create_engine,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_file import FileField
from sqlalchemy_file.storage import StorageManager
from sqlalchemy_file.validators import ContentTypeValidator


container = LocalStorageDriver("./upload_dir").get_container("profiledata")
StorageManager.add_storage("default", container)


def connect_db():
    """
    Создаем пул соединения
    :return: engine
    """
    engine = create_engine(
        URL(**config.DATABASE_DATA), echo=True, pool_size=6, max_overflow=10
    )
    return engine


Base = declarative_base()
Session = sessionmaker(autoflush=False, bind=connect_db())
session = Session()


profile_club_table = Table(
    "profile_club",
    Base.metadata,
    Column("profile_id", Integer(), ForeignKey("profileusers.id")),
    Column("club_id", Integer(), ForeignKey("clubs.id")),
)


class ProfileUser(Base):
    """
    Модель пользователя
    """

    __tablename__ = "profileusers"
    id = Column(Integer(), primary_key=True)
    city = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    birthday = Column(String(100), nullable=False)
    gender = Column(String(100), nullable=False)
    live_communication = Column(String(100), nullable=False)
    work = Column(String(100), nullable=False)
    knowledge = Column(String(200), nullable=False)
    pride = Column(String(100), nullable=False)
    politics_conversations = Column(String(100), nullable=False)
    photo = Column(
        FileField(validators=[ContentTypeValidator(["image/jpeg", "image/png"])])
    )
    created_on = Column(DateTime(), default=datetime.now())
    tg_id = Column(BigInteger(), nullable=False)
    tg_account = Column(
        String(100),
        nullable=False,
    )
    status = Column(String(100), nullable=False, default="member")
    clubs = relationship(
        "Club", secondary=profile_club_table, back_populates="profileusers"
    )

    def get_age(self):
        birth_ls = self.birthday.split(".")
        today = date.today()
        day, month, year = birth_ls[0], birth_ls[1], birth_ls[2]
        age = (
            today.year - int(year) - ((today.month, today.day) < (int(month), int(day)))
        )
        return age


class Club(Base):
    """
    Модель клуба
    """

    __tablename__ = "clubs"
    id = Column(Integer(), primary_key=True)
    id_creator = Column(Integer(), nullable=False)
    admin = Column(ARRAY(String), nullable=False)
    club_name = Column(String(100), nullable=False)
    created_on = Column(DateTime(), default=datetime.now())
    profileusers = relationship(
        "ProfileUser", secondary=profile_club_table, back_populates="clubs"
    )

    def profile_quantity(self):
        return len(self.profileusers)


class Proposals(Base):
    """
    Модель запроса на знаĸомства
    """

    __tablename__ = "proposals"
    id = Column(Integer(), primary_key=True)
    sending_user = Column(String(100), nullable=True)
    receiving_user = Column(String(100), nullable=True)
    created_on = Column(DateTime(), default=datetime.now())


class MyProposals(Base):
    """
    Модель моих запросов на знаĸомства
    """

    __tablename__ = "myproposals"
    id = Column(Integer(), primary_key=True)
    sending_user = Column(String(100), nullable=True)
    receiving_user = Column(String(100), nullable=True)
    created_on = Column(DateTime(), default=datetime.now())

class Match(Base):
    """
    Модель мэтча
    """

    __tablename__ = "match"
    id = Column(Integer(), primary_key=True)
    sending_user = Column(String(100), nullable=False)
    receiving_user = Column(String(100), nullable=False)
    created_on = Column(DateTime(), default=datetime.now())


def create_db():
    """
    Функция для создания таблиц БД
    """
    engine = connect_db()
    Base.metadata.create_all(engine)
    print("Таблицы БД созданы")


def delete_db():
    """
    Функция для удаления таблиц БД
    """
    engine = connect_db()
    Base.metadata.drop_all(engine)
    print("Таблицы удалены!")
