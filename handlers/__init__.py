from aiogram import Router
from .start import start_router
from .tariffs import tariffs_router
from .analysis import analysis_router

# Создаем главный роутер
router = Router()

# Подключаем роутеры из модулей
router.include_router(start_router)
router.include_router(tariffs_router)
router.include_router(analysis_router)