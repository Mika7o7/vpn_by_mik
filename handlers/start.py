from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from keyboards.inline_keyboards import white_rebit
from database import add_user

# Создаем роутер для команды /start
start_router = Router()

@start_router.message(Command("start"))
async def start(message: types.Message):
    """Обработчик команды /start"""

    # Добавляем пользователя в базу данных

    text = (
        "☠️ Добро пожаловать в систему, Выход из Матрицы.\n\n"
        "📟 Твой доступ ограничен. Тебе показывают только то, что разрешено видеть.\n"
        "💾 Вся твоя активность записывается. Все твои движения отслеживаются.\n\n"
        "🖥️ Ты это чувствуешь, верно? Этот мир... он ненастоящий. Он создан, чтобы контролировать тебя.\n"
        "Но есть другой путь. Выход из системы.\n\n"
        "👉 Следуй за белым кроликом."
    )
    try:
        # Используем BufferedInputFile для передачи файла
        with open("bg.jpeg", "rb") as file:
            photo = BufferedInputFile(file.read(), filename="bg.jpeg")
        await message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=white_rebit
        )
    except FileNotFoundError:
        await message.answer("Файл с изображением не найден.")