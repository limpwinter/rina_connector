from aiogram import types
import DataBase
import Buttons

command_to_request_dict = {
    '/table': 'Book',
    'О ресторане': 'RestaurantInfo',
    'Меню еды': 'Menu',
    'Оставить обратную связь': 'Feedback',
}

class TgController:
    def __init__(self, tg_view):
        self.tg_view = tg_view

    async def try_reg_user(self, telegram_id):
        exists, authorized = DataBase.get_user_auth_status(telegram_id)
        
        if not exists:
            DataBase.add_new_user(telegram_id)
            exists = True
        
        if exists and not authorized:
            await self.tg_view.on_auth_new()

        if authorized:
            await self.tg_view.on_auth_existing()

    async def send_request(self, telegram_id, text):
        command = text.split()[0]
        args = text.split()[1:]

        request_type = command_to_request_dict[command]
        print(telegram_id, request_type, args)
        # RequestController.construct_request(telegram_id, request_type, args)
        
    def recieve_response(self, telegram_id, text, image=None):
        self.tg_view.send_message_to_user(telegram_id, text, image)