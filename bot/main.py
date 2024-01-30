import handlers
from database.db_work import create_default_data
from database.postgres_db import create_db, delete_db
from loader import bot
from loguru import logger
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands

if __name__ == "__main__":
    delete_db()
    create_db()
    create_default_data()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    logger.add(
        "logs/logs_{time}.log",
        format="{time} {level} {message}",
        level="DEBUG",
        rotation="08:00",
        compression="zip",
    )
    logger.debug("Error")
    logger.info("Information message")
    logger.warning("Warning")
    bot.infinity_polling()
