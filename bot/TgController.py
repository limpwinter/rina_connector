from aiogram import types
from TgView import TgView
import DataBase
import Buttons
from typing import Callable

class TgController:
    def __init__(self, view: Callable):
        self.tg_view = view

    async def try_reg_user(self, telegram_id):
        exists, authorized = DataBase.get_user_auth_status(telegram_id)
        
        if not exists:
            DataBase.add_new_user(telegram_id)
            exists = True
        
        if exists and not authorized:
            await self.tg_view.on_auth_new(telegram_id)

        if authorized:
            await self.tg_view.on_auth_existing(telegram_id)

    # ... continue with your handlers

    async def run(self):
        await self.tg_view.run()
