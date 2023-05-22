from aiogram import types

import DataBase
import Buttons


class Command:
    def __init__(self, invoke_text, requires_auth):
        self.invoke_text = invoke_text
        self.requires_auth = requires_auth

    # def execute


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