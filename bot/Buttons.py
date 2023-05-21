from aiogram.types import KeyboardButton

accept_decline = [
    [KeyboardButton(text='Принимаю', request_contact=True)],
    [KeyboardButton(text='Не принимаю')],
]

main = [
    [KeyboardButton(text='Инфо о ресторане')],
    [KeyboardButton(text='Меню еды')],
    [KeyboardButton(text='Заказать столик')],
    [KeyboardButton(text='Ввести данные о себе')],
    ]

main_nonauth = [
    [KeyboardButton(text='Инфо о ресторане')],
    [KeyboardButton(text='Меню еды')],
    [KeyboardButton(text='Авторизоваться')],
    ]

rest_info = [
[KeyboardButton(text='Назад')],
[KeyboardButton(text='О ресторане')],
[KeyboardButton(text='Рабочие часы')],
[KeyboardButton(text='Объявления')],
]