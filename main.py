from aiogram import Bot,Dispatcher,F
from environs import Env

import asyncio
import logging

from handler import router



env=Env()
env.read_env()

dp=Dispatcher()






async def main():
    bot=Bot(token=env.str("TOKEN"))
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    
