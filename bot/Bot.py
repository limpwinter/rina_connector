from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import re
import requests
import threading
import datetime
import asyncio
import time
import numpy as np
import ast
import math

import Buttons
import DataBase


#region Начальное
BOT_TOKEN = None

def ConvertStringToType(string):
    # Try to parse the string as a literal
    try:
        return ast.literal_eval(string)
    except:
        # If it fails, it means the string is a date
        return datetime.datetime.strptime(string, '%Y-%m-%d %H:%M')
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
        DataBase.InsertUser(message.from_user.id)
        await message.answer('Добро пожаловать, ' + message.from_user.full_name + '!', reply_markup=keyboard)
#endregion


#region Кнопки
@dp.message_handler(Text(equals='Назад  🔙'))
async def Back(message:types.Message):    
    keyboard = types.ReplyKeyboardMarkup(keyboard=Buttons.main, resize_keyboard = True)
    await message.answer('Основная страница', reply_markup=keyboard)

@dp.message_handler(Text(equals='Инфо о ресторане'))
async def MarketPage(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(keyboard=Buttons.market, resize_keyboard = True)
    await message.answer('Страница инфы о ресторане', reply_markup=keyboard)
#endregion


bot_event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(bot_event_loop)
bot_event_loop.run_until_complete(executor.start_polling(dp, skip_updates=True))