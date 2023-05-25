from aiogram import Bot, types, Dispatcher, executor
from aiogram.dispatcher.filters import Text
import asyncio
from typing import Callable

import Buttons 

class TgView:
    def __init__(self, BOT_TOKEN):
        self.bot = Bot(BOT_TOKEN)
        self.dp = Dispatcher(self.bot)

    async def set_controller(self, controller: Callable):
        self.controller = controller




    async def change_keyboard(self, telegram_id, activated_button_layout, reply):
        keyboard = types.ReplyKeyboardMarkup(keyboard=activated_button_layout, resize_keyboard=True)
        await self.bot.send_message(telegram_id, reply, reply_markup=keyboard)

    async def send_message_to_user(self, telegram_id, text, image=None):
        if image:
            await self.bot.send_photo(telegram_id, photo=image, caption=text)
        else:
            await self.bot.send_message(telegram_id, text)





    def register_handlers(self):

        @self.dp.message_handler(commands='start')
        async def on_start(message: types.Message):
            await self.controller.handle_auth(message.from_user.id)

        @self.dp.message_handler(Text(equals='Авторизоваться'))
        async def on_late_auth(message: types.Message):
            await self.controller.handle_auth(message.from_user.id)

        @self.dp.message_handler(content_types=types.ContentType.CONTACT)
        async def on_contact_received(message: types.Message):
            await self.controller.handle_contact(message)

        @self.dp.message_handler(Text(equals='Не принимаю'))
        async def on_contact_declined(message: types.Message):
            await self.controller.handle_decline(message)




        @self.dp.message_handler(Text(equals='Назад'))
        async def on_back(message: types.Message):
            await self.controller.handle_back(message)

        @self.dp.message_handler(Text(equals='Инфо о ресторане'))
        async def on_info(message: types.Message):
            await self.controller.handle_info(message)

        @self.dp.message_handler(Text(equals='Заказать столик'))
        async def on_table_typo(message: types.Message):
            await self.controller.handle_table_typo(message)




        @self.dp.message_handler(commands='table')
        async def on_table(message: types.Message):
            await self.controller.handle_table(message)

        @self.dp.message_handler(Text(equals='О ресторане'))
        async def on_info_about(message: types.Message):
            await self.controller.handle_info_about(message)





    async def on_auth_new(self, telegram_id):
        await self.change_keyboard(telegram_id, Buttons.accept_decline, "Нажмите кнопку 'Принять' чтобы передать ваш номер телефона.")                       
        
    async def on_auth_existing(self, telegram_id):
        await self.send_message_to_user(telegram_id, "Вы уже авторизованы.")






    async def start_bot(self):
        await self.dp.start_polling()

    async def run(self):
        self.register_handlers()
        await self.start_bot()
