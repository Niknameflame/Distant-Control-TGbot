import asyncio
import os
import BotFunctional
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from dotenv import load_dotenv
load_dotenv("Bot.env")

Bot_token = str(os.getenv("Key"))
bot = AsyncTeleBot(Bot_token)
FunctionsList = {
    "Shutdown pc🚫": {"msg": "Shutdown pc...", "func": BotFunctional.ShutdownPc},
    "Lock pc🔄": {"msg": "Locking screen...", "func": BotFunctional.LockPc},
    "Take screenshot📺": {"msg": "Taking screenshoot...", "func": BotFunctional.TakeScreenshot},
    "Launch App📂": {"msg": "Launching app...", "func": BotFunctional.LaunchApp},
    "Launch Site🌐": {"msg": "Launching site...", "func": BotFunctional.LaunchSite}
}

@bot.message_handler(commands=["start"])
async def AlreadyConnected(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    TestFunc1 = types.KeyboardButton("Lock pc🔄")
    TestFunc2 = types.KeyboardButton("Take screenshot📺")
    TestFunc3 = types.KeyboardButton("Launch App📂")
    TestFunc4 = types.KeyboardButton("Launch Site🌐")
    TestFunc5 = types.KeyboardButton("Shutdown pc🚫")
    markup.row(TestFunc1,TestFunc2)
    markup.row(TestFunc3,TestFunc4)
    markup.row(TestFunc5)

    if BotFunctional.Check(message.from_user.id):
        await bot.send_message(message.chat.id,"Hello owner", reply_markup=markup)     
    else:
        await bot.send_message(message.chat.id,"Sorry, bot created only for owner")

@bot.message_handler(content_types="text")
async def Commands(message: types.Message):
    temp_msg = await bot.reply_to(message, "Check...")
    if BotFunctional.Check(message.from_user.id):
        await asyncio.sleep(1)

        bot_function = FunctionsList[message.text]
        await bot.edit_message_text(bot_function["msg"], message.chat.id, temp_msg.message_id)

        result = bot_function["func"]()
        if str(result).endswith(".png"):
            with open(result, "rb") as photo:
                await bot.send_photo(message.chat.id,photo)
            os.remove(rf"D:\\Coding\\TelegramBot\\DistantControlBot\\{result}")

        await asyncio.sleep(1)
        await bot.delete_message(message.chat.id, temp_msg.message_id)
    else:
        await asyncio.sleep(0.5)
        await bot.edit_message_text("You not owner.", message.chat.id, temp_msg.message_id)

asyncio.run(bot.infinity_polling())