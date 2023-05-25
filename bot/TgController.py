from aiogram import types
from TgView import TgView
import DataBase
import Buttons
from typing import Callable

class TgController:
    def __init__(self, view: Callable):
        self.tg_view = view

    def try_create_db():
        if not DataBase.check_if_db_exists():
            DataBase.create_db()
            DataBase.create_tables()






    async def handle_auth(self, telegram_id):
        exists, authorized = DataBase.get_user_auth_status(telegram_id)
        
        if not exists:
            DataBase.add_new_user(telegram_id)
            exists = True
        
        if exists and not authorized:
            await self.tg_view.on_auth_new(telegram_id)

        if authorized:
            await self.tg_view.on_auth_existing(telegram_id)

    async def handle_contact(self, message):
        phone_number = message.contact.phone_number
        DataBase.set_user_authorized(message.from_user.id)
        await self.tg_view.change_keyboard(message.from_user.id, Buttons.main, "Успешная авторизация.")

    async def handle_decline(self, message):
        keyboard = types.ReplyKeyboardMarkup(keyboard=Buttons.main_nonauth, resize_keyboard=True)
        await message.answer('Основная страница', reply_markup=keyboard)

    async def handle_back(self, message):
        _, authorized = DataBase.get_user_auth_status(message.from_user.id)

        if authorized:
            await self.tg_view.change_keyboard(message.from_user.id, Buttons.main, 'Основная страница')

        if not authorized:
            await self.tg_view.change_keyboard(message.from_user.id, Buttons.main_nonauth, 'Основная страница (ограниченный функционал))')

    async def handle_info(self, message):
        await self.tg_view.change_keyboard(message.from_user.id, Buttons.rest_info, 'Страница инфы о ресторане')

    async def handle_table_typo(self, message):
        await self.tg_view.send_message_to_user(message.from_user.id, '''Закажите столик командой: /table (людей) (время) (день)\nПример: /table 2 18:30 22.05''')

    async def handle_table(self, message):
        TgController.send_request(message.from_user.id, message.text)
        await self.tg_view.send_message_to_user(message.from_user.id, '''Запрос о бронировании направлен в Рину!''')

    async def handle_info_about(self, message):
        TgController.send_request(message.from_user.id, message.text)
        await self.tg_view.send_message_to_user(message.from_user.id, '''Сейчас расскажем о ресторане!''')





    async def send_request(telegram_id, text):
            command = text.split()[0]
            args = text.split()[1:]

            request_type = command_to_request_dict[command]
            print(telegram_id, request_type, args)
            # RequestController.construct_request(telegram_id, request_type, args)
            

    # # В RequestController-е:
    # def send_response_to_telegram(ResponseSample):
    #     TgController.recieve_response(ResponseSample.telegram_id, ResponseSample.text, ResponseSample.image)
    def recieve_response(telegram_id, text, image=None):
        TgView.send_message_to_user(telegram_id, text, image)





    async def run(self):
        TgController.try_create_db()
        await self.tg_view.run()
