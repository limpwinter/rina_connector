from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

import asyncio
import ast

import Buttons
import DataBase
from TgController import TgController 


async def change_keyboard(message:types.Message, button_layout:types.KeyboardButton, reply:str):    
    keyboard = types.ReplyKeyboardMarkup(keyboard=button_layout, resize_keyboard=True)
    await message.answer(reply, reply_markup=keyboard)


#region Начало

# Загрузка параметров
def ConvertStringToType(string):
    return ast.literal_eval(string)
def LoadParametersFromFile():
    # Open the constants file
    with open('constants.txt') as f:
        # Read the contents of the file
        contents = f.read()

    # Split the contents into lines
    lines = contents.split('\n')

    # Iterate over the lines
    for line in lines:
        # Split the line into the constant name and value
        name, value = line.split(' = ')

        # Parse the value as the appropriate data type
        value = ConvertStringToType(value)

        # Assign the value to a variable with the name of the constant
        globals()[name] = value
BOT_TOKEN = None
LoadParametersFromFile()

# Объявление бота
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

# Создание БД
if not DataBase.check_if_db_exists():
    DataBase.create_db()
    DataBase.create_tables()

#endregion


#region Регистрация

@dp.message_handler(commands='start')
async def on_start(message:types.Message):
    await TgController.try_reg_user(message)
    
@dp.message_handler(Text(equals='Авторизоваться'))
async def on_late_auth(message:types.Message):    
    await TgController.try_reg_user(message)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def on_contact_recieved(message:types.Message):
    
    phone_number = message.contact.phone_number    
    # TODO Send request to rina    
    DataBase.set_user_authorized(message.from_id)

    await change_keyboard(message, Buttons.main, f"Успешная авторизация.")

@dp.message_handler(Text(equals='Не принимаю'))
async def on_contact_declined(message:types.Message):    
    keyboard = types.ReplyKeyboardMarkup(keyboard=Buttons.main_nonauth, resize_keyboard=True)
    await message.answer('Основная страница', reply_markup=keyboard)

#endregion


#region Получение сообщений от пользователя

@dp.message_handler(Text(equals='Назад'))
async def on_back(message:types.Message):
    _, authorized = DataBase.get_user_auth_status(message.from_id)
    
    if authorized:
        await change_keyboard(message, Buttons.main, 'Основная страница')
    
    if not authorized:
        await change_keyboard(message, Buttons.main, 'Основная страница')

@dp.message_handler(Text(equals='Инфо о ресторане'))
async def on_info(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=Buttons.rest_info, resize_keyboard=True)
    await message.answer('Страница инфы о ресторане', reply_markup=keyboard)

#endregion


# Запуск бота
bot_event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(bot_event_loop)
bot_event_loop.run_until_complete(executor.start_polling(dp, skip_updates=True))