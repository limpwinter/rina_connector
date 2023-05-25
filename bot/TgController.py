from aiogram import types

import DataBase
import Buttons
import TgView

# class Command:
#     def __init__(self, invoke_text, requires_auth):
#         self.invoke_text = invoke_text
#         self.requires_auth = requires_auth

#     # def execute

command_to_request_dict = {
    '/table': 'Book',
    'О ресторане': 'RestaurantInfo',
    'Меню еды': 'Menu',
    'Оставить обратную связь': 'Feedback',
}

class TgController:

    async def try_reg_user(message: types.Message):
        exists, authorized = DataBase.get_user_auth_status(message.from_id)
        
        if not exists:
            DataBase.add_new_user(message.from_id)
            exists = True
        
        if exists and not authorized:
            keyboard = types.ReplyKeyboardMarkup(keyboard=Buttons.accept_decline, resize_keyboard=True, selective=True)
            await message.reply("Нажмите кнопку 'Принять' чтобы передать ваш номер телефона.", reply_markup=keyboard)
        
        if authorized:
            await message.reply('Вы уже авторизованы.')

    # # В RequestController-е:
    # def construct_request(telegram_id, command, args):
    #     request = Request(telegram_id, command)
    #     request.set_params(args)
    #     request.to_json()
    #     request.send_to_rmq()
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