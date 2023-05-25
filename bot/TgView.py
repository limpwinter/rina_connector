from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import asyncio
import Buttons
import DataBase
from TgController import TgController


class TgView:

    def __init__(self):
        BOT_TOKEN = '6025774622:AAHHZjjL3ZiIXC9WhNgkhm_c_Gtuu5ieYis'
        self.bot = Bot(BOT_TOKEN)
        self.dp = Dispatcher(self.bot)

    def change_keyboard(self, telegram_id, activated_button_layout, reply):
        keyboard = types.ReplyKeyboardMarkup(keyboard=activated_button_layout, resize_keyboard=True)
        self.bot.send_message(telegram_id, reply, reply_markup=keyboard)

    def send_message_to_user(self, telegram_id, text, image):
        if image:
            self.bot.send_photo(telegram_id, photo=image, caption=text)
        else:
            self.bot.send_message(telegram_id, text)

    # Регистрация
    def register_handlers(self):
        @self.dp.message_handler(commands='start')
        async def on_start(message: types.Message):
            await TgController.try_reg_user(message.from_id)

        @self.dp.message_handler(Text(equals='Авторизоваться'))
        async def on_late_auth(message: types.Message):
            await TgController.try_reg_user(message.from_id)

        @self.dp.message_handler(content_types=types.ContentType.CONTACT)
        async def on_contact_received(message: types.Message):
            phone_number = message.contact.phone_number
            # TODO: Send request to rina
            DataBase.set_user_authorized(message.from_id)
            await self.change_keyboard(message, Buttons.main, "Успешная авторизация.")

        @self.dp.message_handler(Text(equals='Не принимаю'))
        async def on_contact_declined(message: types.Message):
            keyboard = types.ReplyKeyboardMarkup(keyboard=Buttons.main_nonauth, resize_keyboard=True)
            await message.answer('Основная страница', reply_markup=keyboard)

        async def on_auth_new(telegram_id):
            self.change_keyboard(telegram_id,
                                 Buttons.accept_decline, 
                                 "Нажмите кнопку 'Принять' чтобы передать ваш номер телефона.")                       
            
        async def on_auth_existing(telegram_id):
            self.send_message_to_user(telegram_id, "Вы уже авторизованы.")


    # Получение сообщений от пользователя
    def message_handlers(self):
        @self.dp.message_handler(Text(equals='Назад'))
        async def on_back(message: types.Message):
            _, authorized = DataBase.get_user_auth_status(message.from_id)

            if authorized:
                await self.change_keyboard(message, Buttons.main, 'Основная страница')

            if not authorized:
                await self.change_keyboard(message, Buttons.main_nonauth, 'Основная страница (ограниченный функционал))')

        @self.dp.message_handler(Text(equals='Инфо о ресторане'))
        async def on_info(message: types.Message):
            await self.change_keyboard(message, Buttons.rest_info, 'Страница инфы о ресторане')

        @self.dp.message_handler(Text(equals='Заказать столик'))
        async def on_table_typo(message: types.Message):
            await message.answer(
                f'''Закажите столик командой: /table (людей) (время) (день)
                Пример: /table 2 18:30 22.05''')

    # Реквесты
    def request_handlers(self):
        @self.dp.message_handler(commands='table')
        async def on_table(message: types.Message):
            TgController.send_request(message.from_id, message.text)
            await message.answer(f'''Запрос о бронировании направлен в Рину!''')

        @self.dp.message_handler(Text(equals='О ресторане'))
        async def on_info_about(message: types.Message):
            TgController.send_request(message.from_id, message.text)
            await message.answer(f'''Сейчас расскажем о ресторане!''')

    def start_bot(self):
        bot_event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(bot_event_loop)
        bot_event_loop.run_until_complete(executor.start_polling(self.dp, skip_updates=True))

    def run(self):
        self.register_handlers()
        self.message_handlers()
        self.request_handlers()
        self.start_bot()


# Create an instance of the TgView class
tg_view = TgView()
tg_view.run()