from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Записать 📝'),
    KeyboardButton(text='Найти 🔍')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню.',
                           one_time_keyboard=True,)
