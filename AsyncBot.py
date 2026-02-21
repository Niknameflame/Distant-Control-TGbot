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
    markup = types.InlineKeyboardMarkup()
    Btn1 = types.InlineKeyboardButton("Lock pc🔄", callback_data="cmd")
    Btn2 = types.InlineKeyboardButton("Take screenshot📺", callback_data="cmd")
    Btn3 = types.InlineKeyboardButton("Launch App📂", callback_data="cmd")
    Btn4 = types.InlineKeyboardButton("Launch Site🌐", callback_data="cmd")
    Btn5 = types.InlineKeyboardButton("Shutdown pc🚫", callback_data="cmd")
    markup.add(Btn1,Btn2,Btn3,Btn4,Btn5)
    if BotFunctional.Check(message.from_user.id):
        await bot.send_message(message.chat.id,"Hello mr. flame:", reply_markup=markup)     
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