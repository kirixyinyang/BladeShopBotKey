from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import os

TOKEN = os.environ.get("TOKEN")  # сюда токен бота вставлять не нужно, мы будем через Railway

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = {}

# Главное меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🛒 Купить ключ")],
        [KeyboardButton("👤 Профиль")],
        [KeyboardButton("💰 Пополнить баланс")],
        [KeyboardButton("💳 Способы оплаты")]
    ],
    resize_keyboard=True
)

# Меню выбора софта
buy_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Blade Soft 7 дней — 199₽")],
        [KeyboardButton("Blade Soft 30 дней — 499₽")],
        [KeyboardButton("⬅ Назад")]
    ],
    resize_keyboard=True
)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {"balance": 0}
    await message.answer("🔥 Blade Shop лучший магазин,\nс быстрой выдачей ключей!", reply_markup=main_menu)

@dp.message_handler(lambda m: m.text == "👤 Профиль")
async def profile(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    balance = users[user_id]["balance"]
    await message.answer(f"👤 Ваш профиль\n\nID: {user_id}\nUsername: @{username}\nБаланс: {balance} рублей")

@dp.message_handler(lambda m: m.text == "💰 Пополнить баланс")
async def deposit(message: types.Message):
    await message.answer("💰 Пополнение временно недоступно.")

@dp.message_handler(lambda m: m.text == "💳 Способы оплаты")
async def payments(message: types.Message):
    await message.answer("💳 Способы оплаты скоро появятся.")

@dp.message_handler(lambda m: m.text == "🛒 Купить ключ")
async def buy_key(message: types.Message):
    await message.answer("Выберите софт:", reply_markup=buy_menu)

@dp.message_handler(lambda m: m.text in ["Blade Soft 7 дней — 199₽", "Blade Soft 30 дней — 499₽"])
async def send_key(message: types.Message):
    await message.answer(f"Вы выбрали {message.text}.\n(Тестовый ключ: TEST-1234)", reply_markup=main_menu)

@dp.message_handler(lambda m: m.text == "⬅ Назад")
async def back(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_menu)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)