import asyncio
import logging


from aiogram import Dispatcher, Bot

from routers.command import command_router
from routers.gos_numder import gos_number_router
from routers.pre_report import pre_report_router

dp = Dispatcher()
bot = Bot(token="7256604422:AAFFAxojKkoFYT5zBbyGJ1ThbUyv-sQJEwo")

dp.include_router(command_router)
dp.include_router(gos_number_router)
dp.include_router(pre_report_router)


async def main():
    logging.basicConfig(level=logging.DEBUG)
    try:
        await dp.start_polling(bot)
    finally:
        pass


if __name__ == "__main__":
    asyncio.run(main())
