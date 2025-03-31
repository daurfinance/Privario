import os
import logging
import re
import random
import json
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from tronpy import Tron
from tronpy.keys import PrivateKey

# Инициализация
API_TOKEN = os.getenv("BOT_TOKEN", "7383930929:AAGqCyYG0OGr2bXvbsoH9Ywb37Wcf2Q1nH0")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# FSM
class Register(StatesGroup):
    name = State()
    email = State()
    phone = State()
    confirm = State()

class InternalTransfer(StatesGroup):
    phone = State()
    amount = State()

users = {}
languages = ["ru", "kz", "en"]

# Переводы
def get_translation(lang):
    path = f"languages/{lang}.json"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# TRON кошелек
def create_tron_wallet():
    priv_key = PrivateKey.random()
    address = priv_key.public_key.to_base58check_address()
    return {
        "address": address,
        "private_key": priv_key.hex()
    }

def get_tron_balance(address):
    try:
        client = Tron(network='nile')
        balance = client.get_account_balance(address)
        return float(balance)
    except:
        return 0.0
# Главное меню
def main_menu(lang):
    t = get_translation(lang)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(t["card"], t["balance"])
    kb.row(t["transfer"], t["deposit"])
    kb.row(t["history"], t["settings"])
    kb.row(t["wallet"], t["manager"])
    return kb

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    lang = message.from_user.language_code if message.from_user.language_code in languages else "ru"
    if user_id in users:
        t = get_translation(lang)
        card_balance = users[user_id]["balance"]
        crypto_balance = get_tron_balance(users[user_id]["wallet"]["address"])
        await message.answer(
            f"{t['welcome_back']}\n"
            f"💳 {t['card_balance']}: {card_balance}$\n"
            f"🪙 {t['crypto_balance']}: {crypto_balance} USDT",
            reply_markup=main_menu(lang)
        )
        return
    users[user_id] = {"lang": lang}
    await message.answer("👤 Введите имя и фамилию:")
    await Register.name.set()

@dp.message_handler(state=Register.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📧 Введите email:")
    await Register.email.set()

@dp.message_handler(state=Register.email)
async def get_email(message: types.Message, state: FSMContext):
    email = message.text
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        await message.answer("❌ Неверный email. Попробуйте снова:")
        return
    await state.update_data(email=email)
    await message.answer("📱 Введите номер телефона в формате +77012345678:")
    await Register.phone.set()

@dp.message_handler(state=Register.phone)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.text
    if not re.match(r"^\+\d{10,15}$", phone):
        await message.answer("❌ Неверный формат номера. Попробуйте снова:")
        return
    code = str(random.randint(100000, 999999))
    await state.update_data(phone=phone, code=code)
    await message.answer(f"🔐 Код подтверждения: {code}")
    await Register.confirm.set()
@dp.message_handler(state=Register.confirm)
async def confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text != data['code']:
        await message.answer("❌ Неверный код, попробуйте снова:")
        return
    user_id = message.from_user.id
    wallet = create_tron_wallet()
    users[user_id].update({
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "wallet": wallet,
        "card": {
            "number": "4444 5555 6666 7777",
            "exp": "12/28",
            "cvc": "123",
            "holder": data["name"],
            "pin": "0000",
            "limit": 10000,
            "blocked": False
        },
        "balance": 500.00
    })
    lang = users[user_id]["lang"]
    t = get_translation(lang)
    crypto_balance = get_tron_balance(wallet["address"])
    await message.answer(
        f"{t['registered']}\n\n"
        f"💳 {t['card']}: {users[user_id]['card']['number']}\n"
        f"👤 {t['name']}: {data['name']}\n"
        f"💰 {t['card_balance']}: 500.00$\n"
        f"🪙 {t['crypto_balance']}: {crypto_balance} USDT",
        reply_markup=main_menu(lang)
    )
    await state.finish()
@dp.message_handler(lambda m: m.text.startswith("💳"))
async def card_menu(message: types.Message):
    user = users.get(message.from_user.id)
    lang = user["lang"]
    t = get_translation(lang)
    card = user["card"]

    if card["blocked"]:
        await message.answer(f"{t['card_blocked']}")
        return

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🔒 Заблокировать", "📉 Лимит")
    kb.row("🔐 Сменить PIN", "⬅️ Назад")
    msg = (
        f"{t['card_number']}: {card['number']}\n"
        f"{t['exp']}: {card['exp']}\n"
        f"CVC: {card['cvc']}\n"
        f"{t['holder']}: {card['holder']}\n"
        f"{t['limit']}: {card['limit']}$\n"
        f"{t['pin']}: {card['pin']}"
    )
    await message.answer(msg, reply_markup=kb)

@dp.message_handler(lambda m: m.text == "🔒 Заблокировать")
async def block_card(message: types.Message):
    user = users.get(message.from_user.id)
    user["card"]["blocked"] = True
    await message.answer("✅ Карта успешно заблокирована.")

@dp.message_handler(lambda m: m.text == "📉 Лимит")
async def set_limit(message: types.Message):
    await message.answer("💼 Введите новый лимит в $ (например: 10000):")

    @dp.message_handler()
    async def limit_value(msg: types.Message):
        try:
            new_limit = float(msg.text)
            users[msg.from_user.id]["card"]["limit"] = new_limit
            await msg.answer(f"✅ Лимит обновлён: {new_limit}$")
        except:
            await msg.answer("❌ Неверный формат. Введите число.")

@dp.message_handler(lambda m: m.text == "🔐 Сменить PIN")
async def change_pin(message: types.Message):
    await message.answer("🔢 Введите новый 4-значный PIN:")

    @dp.message_handler()
    async def pin_value(msg: types.Message):
        if re.match(r"^\d{4}$", msg.text):
            users[msg.from_user.id]["card"]["pin"] = msg.text
            await msg.answer("✅ PIN обновлён.")
        else:
            await msg.answer("❌ PIN должен состоять из 4 цифр.")
@dp.message_handler(lambda m: m.text == "💰 Баланс")
async def balance(message: types.Message):
    user = users.get(message.from_user.id)
    lang = user["lang"]
    t = get_translation(lang)
    card_balance = user["balance"]
    crypto_balance = get_tron_balance(user["wallet"]["address"])
    await message.answer(
        f"💳 {t['card_balance']}: {card_balance}$\n"
        f"🪙 {t['crypto_balance']}: {crypto_balance} USDT"
    )

@dp.message_handler(lambda m: m.text == "📤 Перевести")
async def transfer_menu(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("💳 На карту", "🌍 SWIFT")
    kb.row("💸 USDT TRC20", "🔁 Внутри Privaro")
    kb.row("⬅️ Назад")
    await message.answer("📤 Выберите тип перевода:", reply_markup=kb)

@dp.message_handler(lambda m: m.text == "💳 На карту")
async def transfer_to_card(message: types.Message):
    await message.answer("💳 Введите номер карты и сумму через пробел (пример: `4111222233334444 100`)")

@dp.message_handler(lambda m: m.text == "🌍 SWIFT")
async def swift_transfer(message: types.Message):
    await message.answer("🌍 Введите SWIFT-код и сумму (пример: `DEUTDEFF 2500`)")

@dp.message_handler(lambda m: m.text == "💸 USDT TRC20")
async def crypto_transfer(message: types.Message):
    await message.answer("💸 Введите адрес TRON и сумму (пример: `TXYZ... 50`)")

@dp.message_handler(lambda m: m.text == "🔁 Внутри Privaro")
async def transfer_inside(message: types.Message):
    await message.answer("📱 Введите номер телефона получателя:")
    await InternalTransfer.phone.set()

@dp.message_handler(state=InternalTransfer.phone)
async def check_internal_phone(message: types.Message, state: FSMContext):
    phone = message.text
    recipient_id = None
    for uid, data in users.items():
        if data.get("phone") == phone:
            recipient_id = uid
            break
    if not recipient_id:
        await message.answer("❌ Пользователь с таким номером не найден.")
        await state.finish()
        return
    await state.update_data(recipient=recipient_id)
    await message.answer("💰 Введите сумму для перевода:")
    await InternalTransfer.amount.set()

@dp.message_handler(state=InternalTransfer.amount)
async def confirm_internal_transfer(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        sender = users[message.from_user.id]
        data = await state.get_data()
        recipient_id = data["recipient"]

        if sender["balance"] < amount:
            await message.answer("❌ Недостаточно средств.")
        elif sender["card"]["limit"] < amount:
            await message.answer("❌ Превышен лимит карты.")
        elif sender["card"]["blocked"]:
            await message.answer("❌ Карта заблокирована.")
        else:
            sender["balance"] -= amount
            users[recipient_id]["balance"] += amount
            await message.answer(f"✅ Переведено {amount}$ пользователю по номеру телефона.")
        await state.finish()
    except:
        await message.answer("❌ Неверная сумма.")
        await state.finish()
@dp.message_handler(lambda m: m.text == "⚙️ Настройки")
async def settings_menu(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🌐 Сменить язык", "🔐 Мой кошелёк")
    kb.row("⬅️ Назад")
    await message.answer("⚙️ Настройки:", reply_markup=kb)

@dp.message_handler(lambda m: m.text == "🌐 Сменить язык")
async def change_language(message: types.Message):
    lang_switch = ReplyKeyboardMarkup(resize_keyboard=True)
    lang_switch.row("🇷🇺 Русский", "🇰🇿 Қазақша", "🇬🇧 English")
    await message.answer("🌍 Выберите язык:", reply_markup=lang_switch)

@dp.message_handler(lambda m: m.text.startswith("🇷🇺") or m.text.startswith("🇰🇿") or m.text.startswith("🇬🇧"))
async def set_language(message: types.Message):
    user = users.get(message.from_user.id)
    if "Русский" in message.text:
        user["lang"] = "ru"
    elif "Қазақша" in message.text:
        user["lang"] = "kz"
    else:
        user["lang"] = "en"
    await message.answer("✅ Язык обновлён.", reply_markup=main_menu(user["lang"]))

@dp.message_handler(lambda m: m.text == "🔐 Мой кошелёк")
async def my_wallet(message: types.Message):
    user = users.get(message.from_user.id)
    await message.answer(
        f"🔑 Приватный ключ:\n`{user['wallet']['private_key']}`\n\n"
        f"📬 Адрес TRON (Nile):\n`{user['wallet']['address']}`",
        parse_mode="Markdown"
    )

@dp.message_handler(lambda m: m.text == "📞 Менеджер")
async def contact_manager(message: types.Message):
    await message.answer("👨‍💼 Связь с менеджером: [нажмите здесь](tg://user?id=7155546894)", parse_mode="Markdown")

# Назад
@dp.message_handler(lambda m: m.text == "⬅️ Назад")
async def back(message: types.Message):
    lang = users[message.from_user.id]["lang"]
    await message.answer("↩️ Главное меню:", reply_markup=main_menu(lang))

# Обработка всех остальных сообщений
@dp.message_handler()
async def fallback(message: types.Message):
    await message.answer("⚠️ Неизвестная команда. Пожалуйста, используйте кнопки меню.")

# Запуск
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
