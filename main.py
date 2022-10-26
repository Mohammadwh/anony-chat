from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery

from utils.functionsBot import *
import re
# Initialize bot and dispatcher
functionsClass = functions()
bot = Bot(token=functionsClass.getToken(0))
dp = Dispatcher(bot)
functionsClass.setInfoBot(bot.get_me())

@dp.message_handler(content_types=types.ContentType.ANY)
async def message_handler(message):
    content_type = await functionsClass.get_content_type(message)
    user = await functionsClass.load_user(telegram_id=message.from_user.id, self_get=True)
    print(message)
    print(user['online_at'])
    for plugin in plugins:
        if user['step'] == plugin["step"]:
            for pattern in plugin['patterns_message']:
                if re.search(pattern, content_type, re.IGNORECASE | re.MULTILINE):
                    matches = re.findall(pattern, content_type, re.IGNORECASE)
                    if isinstance(matches[0],list) or isinstance(matches[0],tuple):
                        matches = matches[0]
                    await plugin['run'](message, matches,functionsClass,user,bot)
                    return

@dp.callback_query_handler()
async def inline_handler(message: CallbackQuery):
    for plugin in plugins:
        for pattern in plugin['patterns_callback']:
            if re.search(pattern, message.data, re.IGNORECASE | re.MULTILINE):
                matches = re.findall(pattern, message.data, re.IGNORECASE)
                if isinstance(matches[0],list) or isinstance(matches[0],tuple):
                    matches = matches[0]
                user = await functionsClass.load_user(telegram_id=message.from_user.id,self_get=True)
                await plugin['run_callback'](message, matches,functionsClass,user,bot)
                return

if __name__ == '__main__':
    if not os.path.exists("profiles"):
        os.mkdir("profiles")
    executor.start_polling(dp, skip_updates=True)