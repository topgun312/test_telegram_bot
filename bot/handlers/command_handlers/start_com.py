from keyboards.reply.reply_keyboard import start_markup
from loader import bot
from telebot.types import Message


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    """
    Стартовая функция для начала работы бота.
    :param message: введеная команда пользователем.
    """
    bot.send_message(
        message.from_user.id,
        f"Здравствуйте ✌ {message.from_user.first_name}, "
        f" Вы находитесь в нашем телеграм для поиска друзей! Готовы создать бесплатную анкету?",
        reply_markup=start_markup(),
    )
    bot.delete_message(message.from_user.id, message.message_id)
