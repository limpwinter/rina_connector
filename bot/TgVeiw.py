from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import asyncio
import ast

import Buttons
import DataBase


#region Начальное
BOT_TOKEN = None

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
LoadParametersFromFile()

# Объявление бота
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

# Создание БД
if not DataBase.CheckIfDBExists():
    DataBase.CreateDB()
    DataBase.CreateTables()

# Регистрация
@dp.message_handler(commands='start')
async def TryRegUser(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=Buttons.main, resize_keyboard=True)

    if DataBase.UserRegCheck(message.from_user.id):
        await message.answer('Вы уже есть среди пользователей.' , reply_markup=keyboard)
    else:
        DataBase.InsertUser(message.from_user.id, False)
        await message.answer('Добро пожаловать, ' + message.from_user.full_name + '! Вы ещё не авторизованы.', reply_markup=keyboard)
#endregion


#region Получение сообщений от пользователя
@dp.message_handler(Text(equals='Назад'))
async def Back(message:types.Message):    
    keyboard = types.ReplyKeyboardMarkup(keyboard=Buttons.main, resize_keyboard = True)
    await message.answer('Основная страница', reply_markup=keyboard)

@dp.message_handler(Text(equals='Инфо о ресторане'))
async def RestInfoPage(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=Buttons.rest_info, resize_keyboard = True)
    await message.answer('Страница инфы о ресторане', reply_markup=keyboard)


@dp.message_handler(Text(equals='Инфо о ресторане'))
async def RestInfoPage(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=Buttons.rest_info, resize_keyboard = True)
    await message.answer('Страница инфы о ресторане', reply_markup=keyboard)
#endregion


bot_event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(bot_event_loop)
bot_event_loop.run_until_complete(executor.start_polling(dp, skip_updates=True))