from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup

class KeyboardButtons:
    
    @staticmethod
    async def create_start_buttons():
        return ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text = 'Мій профіль 👤'), 
                KeyboardButton(text = 'Про профспілку ℹ️')
            ],
            [
                KeyboardButton(text = 'feedback ✉️'), 
                KeyboardButton(text = 'Івенти 🎉')
            ],
            [
                KeyboardButton(text="Розклад 🗓️")
            ]
            ], resize_keyboard=True)
    
    @staticmethod
    async def create_union_buttons():
        return ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text = 'Профком 🦁'),
                KeyboardButton(text = 'Профбюро 🔹')
            ],
            [
                KeyboardButton(text = 'Вступ в профспілку/профбюро 📜')
            ],
            [
                KeyboardButton(text="Назад 🔙")
            ]
            ], resize_keyboard=True)
    
    @staticmethod
    async def create_union_buttons():
        return ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text = 'Профком 🦁'),
                KeyboardButton(text = 'Профбюро 🔹')
            ],
            [
                KeyboardButton(text = 'Вступ в профспілку/профбюро 📜')
            ],
            [
                KeyboardButton(text="Назад 🔙")
            ]
            ], resize_keyboard=True)
    
    @staticmethod
    async def create_union_buttons():
        return ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text = 'Профком 🦁'),
                KeyboardButton(text = 'Профбюро 🔹')
            ],
            [
                KeyboardButton(text = 'Вступ в профспілку/профбюро 📜')
            ],
            [
                KeyboardButton(text="Назад 🔙")
            ]
            ], resize_keyboard=True)
    
    @staticmethod
    async def create_cancel_button():
         return ReplyKeyboardMarkup(keyboard=[
             [
                KeyboardButton(text = 'Скасувати ❌'),
             ]
            ], resize_keyboard=True)
    
    @staticmethod
    async def create_profile_buttons():
        return ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text = 'Змінити академічну групу ✍️')
            ],
            [
                KeyboardButton(text = 'Назад 🔙'),
            ]
            ], resize_keyboard=True)
    