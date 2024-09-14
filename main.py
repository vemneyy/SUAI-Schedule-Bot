# main.py

import asyncio
from loader import dp, bot
from config import DATABASE_CONFIG
from database import init_db_pool

import handlers  # noqa


async def main():
    await init_db_pool(DATABASE_CONFIG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
