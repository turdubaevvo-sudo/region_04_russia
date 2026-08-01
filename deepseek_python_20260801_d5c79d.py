import asyncio
import logging
import os
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ======================================================
# 1. Функция проверки рабочего дня
# ======================================================
def is_working_day(check_date: datetime) -> bool:
    """
    Возвращает True, если день рабочий (пн-пт) и не праздничный.
    """
    # 1. Проверяем день недели (пн=0, вс=6)
    weekday = check_date.weekday()
    if weekday >= 5:  # Суббота (5) или Воскресенье (6)
        return False

    # 2. Список официальных праздников РФ (можно расширять)
    #    Важно: год динамический, чтобы не править каждый год вручную
    year = check_date.year
    holidays = [
        datetime(year, 1, 1),  # Новый год
        datetime(year, 1, 2),
        datetime(year, 1, 3),
        datetime(year, 1, 4),
        datetime(year, 1, 5),
        datetime(year, 1, 6),
        datetime(year, 1, 7),
        datetime(year, 1, 8),
        datetime(year, 2, 23), # День защитника Отечества
        datetime(year, 3, 8),  # 8 марта
        datetime(year, 5, 1),  # Первомай
        datetime(year, 5, 9),  # День Победы
        datetime(year, 6, 12), # День России
        datetime(year, 11, 4), # День народного единства
    ]
    
    # Проверяем, не праздник ли сегодня (сравниваем только день и месяц)
    for holiday in holidays:
        if check_date.month == holiday.month and check_date.day == holiday.day:
            return False

    return True


# ======================================================
# 2. Обработчик команды /start
# ======================================================
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот для приёма заказов.\n"
        "Отправьте /order, чтобы оформить заказ."
    )


# ======================================================
# 3. Основная логика заказа (проверка дня)
# ======================================================
@dp.message(Command("order"))
async def cmd_order(message: Message):
    now = datetime.now()
    
    if not is_working_day(now):
        # ---- Выходной или праздник ----
        weekday = now.weekday()
        if weekday == 5:
            day_name = "субботу"
        elif weekday == 6:
            day_name = "воскресенье"
        else:
            day_name = "праздничный день"
            
        await message.answer(
            f"⛔ Извините, сегодня {day_name}.\n"
            f"📅 Мы принимаем заказы только в рабочие дни (пн-пт) с 9:00 до 18:00.\n"
            f"🔄 Пожалуйста, повторите попытку в ближайший рабочий день."
        )
        return

    # ---- Рабочий день ----
    # Здесь можно добавить проверку времени (например, с 9 до 18)
    # if not (9 <= now.hour < 18):
    #     await message.answer("⏰ Мы работаем с 9:00 до 18:00. Приходите завтра!")
    #     return

    await message.answer(
        "✅ Сегодня рабочий день!\n"
        "Пожалуйста, напишите ваш заказ текстом.\n"
        "Менеджер свяжется с вами в ближайшее время."
    )


# ======================================================
# 4. Запуск бота
# ======================================================
async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())