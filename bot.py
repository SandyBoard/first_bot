
from tk import TOKEN_API
from aiogram import Bot, Dispatcher, executor, types
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)

user_data = {}  # Здесь будем временно хранить данные пользователя

def is_valid_name(name):
    return name.isalpha()

def is_valid_phone(phone):
    if phone.startswith("+7"):
        phone = phone[2:]
    elif phone.startswith("7") or phone.startswith("8"):
        phone = phone[1:]
    return phone.isdigit() and phone.startswith("9") and len(phone) == 10

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    await message.answer("Привет! Давай знакомиться!")
    await message.answer("Как тебя зовут?")
    user_data[user_id]['step'] = 'name'

@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.answer("Пожалуйста, начни с команды /start")
        return
    
    step = user_data[user_id].get('step')

    if step == 'name':
        if not is_valid_name(message.text):
            await message.answer("Имя должно содержать только буквы. Попробуй снова.")
            return
        user_data[user_id]['name'] = message.text.capitalize()
        await message.answer("Какая у тебя фамилия?")
        user_data[user_id]['step'] = 'surname'

    elif step == 'surname':
        if not is_valid_name(message.text):
            await message.answer("Фамилия должна содержать только буквы. Попробуй снова.")
            return
        user_data[user_id]['surname'] = message.text.capitalize()
        await message.answer("Какой у тебя email?")
        user_data[user_id]['step'] = 'email'

    elif step == 'email':
        user_data[user_id]['email'] = message.text
        await message.answer("Какой у тебя номер телефона?")
        user_data[user_id]['step'] = 'phone'

    elif step == 'phone':
        if not is_valid_phone(message.text):
            await message.answer("Номер телефона должен начинаться с 8, 7 или +7 и содержать 11 цифр, либо начинаться с 9 и содержать 10 цифр. Попробуй снова.")
            return
        user_data[user_id]['phone'] = message.text
        await message.answer("Какая у тебя сфера деятельности?")
        user_data[user_id]['step'] = 'activity'

    elif step == 'activity':
        user_data[user_id]['activity'] = message.text
        await message.answer("Чем можешь быть полезен для клуба?")
        user_data[user_id]['step'] = 'usefulness'

    elif step == 'usefulness':
        user_data[user_id]['usefulness'] = message.text
        await message.answer(f"Приятно познакомиться, {user_data[user_id]['name']} :)")
        
        # Создаем кнопку с ссылкой на групповой чат
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Заходи в групповой чат", url="https://t.me/+SMsfGteEJAU9pEaw"))
        
        await message.answer("Заходи в групповой чат.", reply_markup=markup)
        # Здесь можно сохранить user_data в базу данных или выполнить другое действие

        # Сброс состояния пользователя
        user_data.pop(user_id, None)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)