from aiogram import Router, types
from aiogram.types import BufferedInputFile
from keyboards.inline_keyboards import ikb, depkb
from database import add_user, add_subscription, add_payment
from payments import create, check
from datetime import datetime, timedelta
import asyncio

# Создаем роутер для обработки callback-запросов
tariffs_router = Router()



@tariffs_router.callback_query(lambda call: call.data == "tariffs")
async def tariffs_callback(call: types.CallbackQuery):
    """Обработчик кнопки 'Тарифы'"""
    print("CALLBACK ПОЛУЧЕН:", call.data)  # Логируем callback
    try:
        # Используем BufferedInputFile для передачи файла
        with open("matrix.jpeg", "rb") as file:
            photo = BufferedInputFile(file.read(), filename="matrix.jpeg")
        await call.message.answer_photo(
            photo=photo,
            caption="Выберите тариф:",
            reply_markup=ikb
        )
        await call.answer()  # Закрываем "часики" на кнопке
    except FileNotFoundError:
        await call.message.answer("Файл с изображением не найден.")
    except Exception as e:
        await call.message.answer("Ошибка при обработке запроса.")
        print(f"Ошибка в tariffs_callback: {e}")

async def process_payment(payment_id: str, chat_id: int, amount: float, bot, tariff: str, duration: timedelta, user_id: int):
    """Проверяет статус оплаты и активирует подписку"""
    for _ in range(10):  # Пробуем 10 раз с интервалом в 30 секунд
        payment_status = check(payment_id)  # Проверяем статус платежа
        if payment_status:
            # Активация подписки после успешной оплаты
            start_date = datetime.now()
            end_date = start_date + duration
            add_subscription(user_id, tariff, start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d %H:%M:%S"))
            add_payment(user_id, amount, "RUB")

            # Текст сообщения с ссылкой на скачивание приложения
            success_message = (
                f"✅ Оплата на сумму {amount:.2f} руб. успешно подтверждена! Подписка '{tariff}' активирована.\n\n"
                "📲 Скачайте приложение для подключения:\n"
                "👉 [App Store](https://apps.apple.com/app/id1441195209)\n\n"
                "⬇️ Ваш конфигурационный файл прикреплен ниже. Инструкция по подключению:\n"
                "1. Откройте приложение.\n"
                "2. Нажмите 'Добавить конфигурацию'.\n"
                "3. Выберите файл из этого сообщения.\n"
                "4. Подключитесь к серверу."
            )

            # Отправляем текстовое сообщение
            await bot.send_message(chat_id, success_message, parse_mode="Markdown")

            # Отправляем конфигурационный файл
            with open("config.ovpn", "rb") as config_file:  # Убедитесь, что файл config.ovpn существует
                await bot.send_document(chat_id, config_file, caption="Ваш конфигурационный файл для подключения.")

            return
        await asyncio.sleep(30)

    # Если оплата не подтверждена
    await bot.send_message(chat_id, "❌ Оплата не была подтверждена. Если проблема сохраняется, обратитесь в поддержку.")

    
@tariffs_router.callback_query(lambda call: call.data in ["yearly", "monthly"])
async def process_tariff(call: types.CallbackQuery):
    """Обработчик выбора тарифа"""
    user_id = call.from_user.id
    username = call.from_user.username
    full_name = call.from_user.full_name

    # Определяем тариф и стоимость
    if call.data == "yearly":
        tariff = "Годовой"
        amount = 12000  # Стоимость годового тарифа в рублях
        duration = timedelta(days=365)
    else:
        tariff = "Месячный"
        amount = 1000  # Стоимость месячного тарифа в рублях
        duration = timedelta(days=30)

    # Добавляем пользователя в базу данных
    add_user(user_id, username, full_name)
    # Создаем платеж и получаем payment_url и payment_id
    payment_url, payment_id = create(amount=amount, chat_id=call.message.chat.id)

    # Отправляем пользователю ссылку для оплаты
    await call.message.answer(
        text=(
            f"✨ Вы выбрали подписку: {tariff}\n"
            f"💳 Стоимость: {amount} рублей\n\n"
            f"Перейдите по ссылке для оплаты:"
        ),
        reply_markup=depkb(payment_url, payment_id)  # Используйте вашу клавиатуру для оплаты
    )
    await call.answer()
    

    # Ожидаем подтверждение оплаты
    asyncio.create_task(process_payment(payment_id, call.message.chat.id, amount, call.bot, tariff, duration, user_id))

