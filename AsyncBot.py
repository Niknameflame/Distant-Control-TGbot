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
    "Lock pc🔄": {"msg": "Lock screen...", "func": BotFunctional.LockPc},
    "Take screenshot📺": {"msg": "Taked screenshoot...", "func": BotFunctional.TakeScreenshot},
}

@bot.message_handler(commands=["start"])
async def AlreadyConnected(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    TestFunc1 = types.KeyboardButton("Lock pc🔄")
    TestFunc2 = types.KeyboardButton("Take screenshot📺")
    TestFunc3 = types.KeyboardButton("Shutdown pc🚫")
    markup.row(TestFunc1,TestFunc2)
    markup.row(TestFunc3)

    if BotFunctional.Check(message.from_user.id):
        await bot.send_message(message.chat.id,"Hello owner🙂", reply_markup=markup)     
    else:
        await bot.send_message(message.chat.id,"Sorry, bot created only for owner!")

@bot.message_handler(content_types="text")
async def Commands(message: types.Message):
    await bot.reply_to(message, "Check...")

    if BotFunctional.Check(message.from_user.id):
        bot_function = FunctionsList[message.text]
        await bot.send_message(message.chat.id, bot_function["msg"])

        result = bot_function["func"]()
        if str(result).endswith(".png"):
            with open(result, "rb") as photo:
                await bot.send_photo(message.chat.id,photo)
            os.remove(rf"D:\\Coding\\TelegramBot\\DistantControlBot\\{result}")
    else:
        bot.send_message(message.chat.id, "You are not owner.")

asyncio.run(bot.infinity_polling())