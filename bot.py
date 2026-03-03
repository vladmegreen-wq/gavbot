
import aiogram
from router import root_router


bot = aiogram.Bot(token='Your Token Here')
dp = aiogram.Dispatcher()


async def run_bot():
    dp.include_router(root_router)

    await dp.start_polling(bot)
