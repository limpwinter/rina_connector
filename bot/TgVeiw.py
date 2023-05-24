from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text

import asyncio
import ast

import Buttons
import DataBase
from TgController import TgController 



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




class UserInput:

    def __init__(self,
                 command, 
                 requires_auth = False, 
                 controller_method = None,
                 activated_button_layout = None,
                 reply = None,
                 ):
        self.command = command
        self.requires_auth = requires_auth
        self.controller_method = controller_method
        self.activated_button_layout = activated_button_layout
        self.reply = reply

    def reg_check(self):
        _, authorized = DataBase.get_user_auth_status(self.telegram_id)
        return authorized
    
    async def change_keyboard_and_reply(self):    
        keyboard = types.ReplyKeyboardMarkup(keyboard=self.activated_button_layout, resize_keyboard=True)
        await bot.send_message(self.telegram_id, self.reply, reply_markup=keyboard)
    
    async def try_execute(self, message:types.Message):

        self.telegram_id = message.from_id
        self.invoke_text = message.text

        if self.requires_auth:

            success = self.reg_check()
            if success:
                await self.execute()
            else:
                await bot.send_message(self.telegram_id, 'Недоступно для неавторизованных пользователей.')

        else:
            await self.execute()

    async def execute(self):

        self.controller_method()

        if self.activated_button_layout:
            await self.change_keyboard_and_reply()

# user_inputs = []
# user_inputs.append( UserInput('/start'), TgController.try_reg_user)

# for user_input in user_inputs:

#     @dp.message_handler(Text(equals='/start'))



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
        await change_keyboard(message, Buttons.main_nonauth, 'Основная страница (ограниченный функционал))')

@dp.message_handler(Text(equals='Инфо о ресторане'))
async def on_info(message:types.Message):
    await change_keyboard(message, Buttons.rest_info, 'Страница инфы о ресторане')
    
@dp.message_handler(Text(equals='Заказать столик'))
async def on_table_typo(message:types.Message):
    await message.answer(f'''Закажите столик командой: /table (людей) (время) (день)
    Пример: /table 2 18:30 22.05''')

#endregion


#region Реквесты

@dp.message_handler(commands='table')
async def on_table(message:types.Message):
    _, number_of_guests, time, day = message.text.split()
    # TODO Send request to rina
    await message.answer(f'''Запрос отправлен в Рину: {[number_of_guests, time, day]}''')

@dp.message_handler(Text(equals='О ресторане'))
async def on_info_about(message:types.Message):
    # TODO Send request to rina
    await message.answer(f'''Сейчас расскажем о ресторане!''')

#endregion  


#region Запуск бота

bot_event_loop = asyncio.new_event_loop()
asyncio.set_event_loop(bot_event_loop)
bot_event_loop.run_until_complete(executor.start_polling(dp, skip_updates=True))

#endregion  