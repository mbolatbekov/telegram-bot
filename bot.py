import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils.executor import start_polling
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Данные бота
TOKEN = "7970425858:AAGaz_RIO6FEDIogmTXLLepRAlTupD9uo5E"  # Токен из BotFather
GROUP_ID = -1002465564379  # ID группы

# Изначальный список чтецов
readers = [
    {"name": "Алмат", "range": "1-10"},
    {"name": "Абилкайыр", "range": "11-20"},
    {"name": "Ануар", "range": "21-30"},
    {"name": "Дархан", "range": "31-40"},
    {"name": "Мадияр", "range": "41-50"},
    {"name": "Абеке", "range": "51-60"},
    {"name": "Жаке", "range": "61-70"},
    {"name": "Фараби", "range": "71-80"},
    {"name": "Мансур", "range": "81-90"},
    {"name": "Алмаз", "range": "91-104"},
]

# Файл для хранения списка
FILE_PATH = "readers.json"

# Функция для загрузки списка
def load_readers():
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return readers  

# Функция для сохранения списка
def save_readers(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Функция для сдвига списка
def shift_readers():
    data = load_readers()
    data.append(data.pop(0))  # Перемещаем первого в конец
    save_readers(data)
    return data

# Функция для форматирования списка
def format_readers():
    data = load_readers()
    today = "📖 **График чтения на сегодня**\n\n"
    formatted_list = "\n".join([f"{i+1}️⃣ **{r['name']}** → {r['range']}" for i, r in enumerate(data)])
    return today + formatted_list

# Создание бота и диспетчера
bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()

# Команда для ручного обновления
@dp.message_handler(commands=["update"])
async def update_list(message: types.Message):
    if message.chat.id == GROUP_ID:
        shift_readers()
        await message.answer(format_readers())

# Функция для ежедневного обновления
async def daily_update():
    shift_readers()
    await bot.send_message(GROUP_ID, format_readers())

# Запуск планировщика
async def on_startup(_):
    scheduler.add_job(daily_update, "cron", hour=9, minute=0)
    scheduler.start()

if __name__ == "__main__":
    start_polling(dp, on_startup=on_startup)
