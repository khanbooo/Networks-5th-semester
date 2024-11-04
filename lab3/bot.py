import asyncio
import sys
from aiogram import Bot, Dispatcher, types
from handlers import router
from config import TG_BOT_TOKEN

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("interrupted")
        sys.exit(0)
