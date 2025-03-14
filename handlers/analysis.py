from aiogram import Router, types
from aiogram.filters import Command
from database import get_analysis

# Создаем роутер для команды /analysis
analysis_router = Router()

@analysis_router.message(Command("analysis"))
async def analysis(message: types.Message):
    """Обработчик команды /analysis"""
    stats = get_analysis()
    response = (
        "📊 Статистика:\n"
        f"👤 Всего пользователей: {stats['total_users']}\n"
        f"📅 Всего подписок: {stats['total_subscriptions']}\n"
        f"💰 Общий доход: {stats['total_revenue']} RUB"
    )
    await message.answer(response)