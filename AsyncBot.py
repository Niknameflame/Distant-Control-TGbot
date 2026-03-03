import asyncio
import os
import BotFunctional
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from pathlib import Path
from dotenv import load_dotenv

path = Path(__file__).resolve().parent
load_dotenv(dotenv_path=path/"Bot.env")

YourInput = False
bot = AsyncTeleBot(str(os.getenv("Key")))

FunctionsList = {
    "shutdown": {"msg": "Shutdowning pc", "func": BotFunctional.ShutdownPc, "special": False},
    "lock": {"msg": "Locking screen", "func": BotFunctional.LockPc, "special": False},
    "screenshot": {"msg": "Screenshoting", "func": BotFunctional.TakeScreenshot, "special": False},
    "site": {"msg": "Send url to open:", "func": BotFunctional.LaunchSite, "special": True},
}

@bot.message_handler(commands=["start"])
async def AlreadyConnected(message):
    markup = types.InlineKeyboardMarkup()
    Btn1 = types.InlineKeyboardButton("Lock pc🔄", callback_data="lock")
    Btn2 = types.InlineKeyboardButton("Take screenshot📺", callback_data="screenshot")
    Btn3 = types.InlineKeyboardButton("Launch Site🌐", callback_data="site")
    Btn4 = types.InlineKeyboardButton("Shutdown pc🚫", callback_data="shutdown")
    markup.add(Btn1, Btn2, Btn3, Btn4)

    if BotFunctional.Check(message.from_user.id):
        await bot.send_message(message.chat.id, "Hello mr. flame:", reply_markup=markup)
        await bot.delete_message(message.chat.id, message.message_id)
    else:
        await bot.send_message(message.chat.id, "Sorry, bot created only for owner")

@bot.callback_query_handler(func=lambda call: True)
async def Commands(call: types.CallbackQuery):
    Func_Info = FunctionsList[call.data]
    global YourInput
    await bot.edit_message_text(Func_Info["msg"], call.message.chat.id, call.message.message_id)
    if not Func_Info["special"]:
        Result = Func_Info["func"]()
        if isinstance(Result, str) and Result.endswith(".png"):
            image = path / Result
            with open(image, "rb") as photo:
                await bot.send_photo(call.message.chat.id, photo)
            os.remove(image)
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        if not YourInput:
            YourInput = True

@bot.message_handler()
async def SendText(message: types.Message):
    global YourInput
    if YourInput and str(message.text):
        if BotFunctional.Check(message.from_user.id):
            YourInput = False
            await bot.reply_to(message, "Opening url")
            BotFunctional.LaunchSite(str(message.text))
            await asyncio.sleep(1)
            await bot.delete_message(message.chat.id,message.message_id)

asyncio.run(bot.infinity_polling())