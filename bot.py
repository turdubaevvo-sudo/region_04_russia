from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from datetime import datetime
import pytz

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "9192939591:AAExZhpLXcEWIqiRdslErVY-BmN8kwTZOU4"   # получите у @BotFather

# Часовой пояс (Москва). Список: pytz.all_timezones
TIMEZONE = "Asia/Barnaul"

# Текст автоответа
AUTO_REPLY = (
    "🌿 Здравствуйте! Сейчас выходные дни — я не работаю, и редко отвечаю.\n"
    "Пожалуйста, напишите в будние дни (пн–пт).\n"
    "Спасибо за понимание! 🙏"
)

# Рабочие дни: 0 = понедельник, ..., 6 = воскресенье
# По умолчанию выходные — суббота (5) и воскресенье (6)
WEEKEND_DAYS = {5, 6}

# Чтобы не спамить одному и тому же человеку — храним тех, кому уже ответили
# (сбрасывается при перезапуске бота; для продакшена используйте БД)
replied_users = set()
# =====================


def is_weekend() -> bool:
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    return now.weekday() in WEEKEND_DAYS


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отвечает на любое входящее сообщение в выходные."""
    if not update.message or not update.effective_user:
        return

    if not is_weekend():
        return  # в будни бот молчит

    user_id = update.effective_user.id

    # Ответить один раз за выходные (чтобы не спамить)
    if user_id in replied_users:
        return

    replied_users.add(user_id)
    await update.message.reply_text(AUTO_REPLY)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Ловим все текстовые сообщения (можно расширить на любые типы)
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

    print("Бот запущен. Ожидаю сообщения...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
