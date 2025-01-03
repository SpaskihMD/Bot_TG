import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN
from app.handlers import router




async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO) # Подключение логирования
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Вы вышли из программы')