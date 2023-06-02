from typing import Callable
import asyncio

import TgDataBase
import TgButtons
from model.RequestController import RequestController
from model.JsonController import JsonController

from rmq.RmqController import RmqController


class TgController:

    def __init__(self, view: Callable):
        self.tg_view = view

    def try_create_db():
        if not TgDataBase.check_if_db_exists():
            TgDataBase.create_db()
            TgDataBase.create_tables()



    async def handle_auth(self, telegram_id):
        exists, authorized = TgDataBase.get_user_auth_status(telegram_id)
        if not exists:
            TgDataBase.add_new_user(telegram_id)
            exists = True
        if exists and not authorized:
            await self.tg_view.change_keyboard(telegram_id, 
                                       TgButtons.accept_decline, 
                                       "Нажмите кнопку 'Принять' чтобы передать ваш номер телефона.")
        if authorized:
            await self.tg_view.send_message_to_user(telegram_id, "Вы уже авторизованы.")

    async def handle_contact_recieved(self, telegram_id, phone_number):
        TgDataBase.set_user_authorized(telegram_id)
        await self.send_request(telegram_id, f'/send_number_to_rina {phone_number}')
        await self.tg_view.change_keyboard(telegram_id, TgButtons.main, "Успешная авторизация.")

    async def handle_contact_declined(self, telegram_id):
        await self.tg_view.change_keyboard(telegram_id, 
                                           TgButtons.main_nonauth, 
                                           'Основная страница (ограниченный функционал)')

    async def handle_back(self, telegram_id):
        _, authorized = TgDataBase.get_user_auth_status(telegram_id)
        if authorized:
            await self.tg_view.change_keyboard(telegram_id, 
                                               TgButtons.main, 
                                               'Основная страница')
        if not authorized:
            await self.tg_view.change_keyboard(telegram_id, 
                                               TgButtons.main_nonauth, 
                                               'Основная страница (ограниченный функционал)')

    async def handle_info(self, telegram_id):
        await self.tg_view.change_keyboard(telegram_id, 
                                           TgButtons.rest_info, 
                                           'Страница информации о ресторане')

    async def handle_table_typo(self, telegram_id):
        await self.tg_view.send_message_to_user(telegram_id, 
                                                f'Закажите столик командой: /table (людей) (время) (день)\n'
                                                f'Пример: /table 2 18:30 22.05')

    async def handle_table(self, telegram_id, input_text):
        _, authorized = TgDataBase.get_user_auth_status(telegram_id)
        if authorized:
            await self.send_request(telegram_id, input_text)
            await self.tg_view.send_message_to_user(telegram_id, '''Запрос о бронировании направлен в Рину!''')
        if not authorized:
            await self.tg_view.send_message_to_user(telegram_id, '''Авторизуйтесь чтобы заказывать столик!''')

    async def handle_data_typo(self, telegram_id):
        await self.tg_view.send_message_to_user(telegram_id, 
                                                f'Закажите столик командой: /data (пол) (веган) (аллергия на орегано)\n'
                                                f'Пример: /data Ж нет нет')

    async def handle_data(self, telegram_id, input_text):
        _, authorized = TgDataBase.get_user_auth_status(telegram_id)
        if authorized:
            await self.send_request(telegram_id, input_text)
            await self.tg_view.send_message_to_user(telegram_id, 'Рина надёжно сохранит и учтёт ваши данные!')
        if not authorized:
            await self.tg_view.send_message_to_user(telegram_id, '''Авторизуйтесь рассказать о себе!''')

    async def handle_info_about(self, telegram_id, input_text):
        await self.send_request(telegram_id, input_text)
        await self.tg_view.send_message_to_user(telegram_id, 'Сейчас расскажем о ресторане!')
        
    async def handle_hours(self, telegram_id, input_text):
        await self.send_request(telegram_id, input_text)
        await self.tg_view.send_message_to_user(telegram_id, 'Сейчас расскажем о часах работы!')
        
    async def handle_news(self, telegram_id, input_text):
        await self.send_request(telegram_id, input_text)
        await self.tg_view.send_message_to_user(telegram_id, 'Сейчас расскажем о новостях и акциях!')
        
    async def handle_menu(self, telegram_id, input_text):
        await self.send_request(telegram_id, input_text)
        await self.tg_view.send_message_to_user(telegram_id, 'Сейчас покажем меню!')



    command_request_dict = {
        '/table': 'Book',
        '/data': 'UserData',
        '/send_number_to_rina': 'Number',
        'О ресторане': 'RestaurantInfo',
        'Рабочие часы': 'WorkHours',
        'Объявления': 'Updates',
        'Меню еды': 'Menu',
        'Оставить обратную связь': 'Feedback',
    }

    async def send_request(self, telegram_id, input_text):
        command = None
        args = None

        if input_text in self.command_request_dict:
            command = input_text
        else:
            command, *args = input_text.split()

        request_type = self.command_request_dict.get(command)
        if request_type:
            print(f'Отправлен запрос: {telegram_id, request_type, args}.')
            request = RequestController(telegram_id, request_type)
            request.set_params(args)
            request_json = request.to_json()
            RmqController.send_to_rina(request_json)
        else:
            print(f'Команда {command} неизвестна.')
        
    async def receive_response(self, response_js_str):

        response_js = JsonController().str_to_dct(response_js_str)
        
        telegram_id = response_js['user_id']
        text = response_js['annotation']['text']
        image = response_js['annotation']['image']

        await self.tg_view.send_message_to_user(telegram_id, text, image)


    async def run(self):
        TgController.try_create_db()
        await self.tg_view.run()
