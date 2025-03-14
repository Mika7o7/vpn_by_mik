from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для тарифов
ikb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🟥 Годовой тариф', callback_data='yearly'),
        InlineKeyboardButton(text='🟦 Месячный тариф', callback_data='monthly')
    ]
])

# Клавиатура с белым кроликом
white_rebit = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🐰 Тарифы", callback_data="tariffs")]
])

def depkb(url, id):
    # Создаем список кнопок
    buttons = [
        [InlineKeyboardButton(text='💸 Оплатить услугу', url=url)],
        # Если нужно добавить кнопку для проверки оплаты, раскомментируйте:
        # [InlineKeyboardButton(text='Проверить оплату', callback_data=f'check_{id}')]
    ]
    
    # Создаем клавиатуру с кнопками
    depkbm = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    return depkbm