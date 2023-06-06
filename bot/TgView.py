from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher.filters import Text
from typing import Callable


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


    COMMANDS_TEXTS_TO_HANDLER_NAMES = {
        '/start': 'handle_auth',
        'Авторизоваться': 'handle_auth',
        'Не принимаю': 'handle_contact_declined',
        'Назад': 'handle_back',
        'Инфо о ресторане': 'handle_info',
        'Заказать столик': 'handle_table_typo',
        'Ввести данные о себе': 'handle_data_typo',

        types.ContentType.CONTACT: 'handle_contact_recieved',

        'О ресторане': 'handle_info_about',
        'Рабочие часы': 'handle_hours',
        'Объявления': 'handle_news',
        'Меню еды': 'handle_menu',
        '/table': 'handle_table',
        '/data': 'handle_data'
    }
    COMMANDS_INCLUDING_MESSAGE_TEXT = [
        'О ресторане',
        'Рабочие часы',
        'Объявления',
        'Меню еды',
        '/table',
        '/data',
        ]

    # Вспомогательная функция, создаёт детектор сообщений пользователя и что с ними делать 
    def make_handler_with_args(self, handler, include_message_text=False, include_phone_number=False):
        if include_phone_number:
            async def handler_with_args(message: types.Message):
                await handler(message.from_user.id, message.contact.phone_number)
        elif include_message_text:
            async def handler_with_args(message: types.Message):
                await handler(message.from_user.id, message.text)
        else:
            async def handler_with_args(message: types.Message):
                await handler(message.from_user.id)

        return handler_with_args

    # При запуске добавляет все детекторы сообщений
    def register_handlers(self):
        
        for command, handler_name in self.COMMANDS_TEXTS_TO_HANDLER_NAMES.items():
            # Получаем ссылку на метод в контроллере
            handler = self.controller.__getattribute__(handler_name)

            # По списку смотрим, передавать ли текст
            include_message_text = command in self.COMMANDS_INCLUDING_MESSAGE_TEXT  
            
            if command == types.ContentType.CONTACT:
                handler_with_args = self.make_handler_with_args(handler, include_phone_number=True)
                # Передаём handler в dispatcher телеграма
                self.dp.message_handler(content_types=command)(handler_with_args)

            elif command.startswith('/'):
                handler_with_args = self.make_handler_with_args(handler, include_message_text=include_message_text)
                self.dp.message_handler(commands=command.lstrip('/'))(handler_with_args)
            
            else:
                handler_with_args = self.make_handler_with_args(handler, include_message_text=include_message_text)
                self.dp.message_handler(Text(equals=command))(handler_with_args)




    async def start_bot(self):
        await self.dp.start_polling()

    async def run(self):
        self.register_handlers()
        await self.start_bot()
