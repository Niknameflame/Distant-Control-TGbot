import asyncio
import os
import BotFunctional
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from pathlib import Path
from dotenv import load_dotenv

path = Path(__file__).resolve().parent
load_dotenv(dotenv_path=path/"Bot.env")

bot = AsyncTeleBot(str(os.getenv("Key")))

FunctionsList = {
    "Shutdown pc🚫": {"msg": "Shutdown pc...", "func": BotFunctional.ShutdownPc},
    "Lock pc🔄": {"msg": "Locking screen...", "func": BotFunctional.LockPc},
    "Take screenshot📺": {"msg": "Taking screenshoot...", "func": BotFunctional.TakeScreenshot},
    "Launch Site🌐": {"msg": "Launching site...", "func": BotFunctional.LaunchSite}
}

@bot.message_handler(commands=["start"])
async def AlreadyConnected(message):
    markup = types.InlineKeyboardMarkup()
    Btn1 = types.InlineKeyboardButton("Lock pc🔄", callback_data="Lock pc🔄")
    Btn2 = types.InlineKeyboardButton("Take screenshot📺", callback_data="Take screenshot📺")
    Btn3 = types.InlineKeyboardButton("Launch Site🌐", callback_data="Launch Site🌐")
    Btn4 = types.InlineKeyboardButton("Shutdown pc🚫", callback_data="Shutdown pc🚫")
    markup.add(Btn1,Btn2,Btn3,Btn4)

    if BotFunctional.Check(message.from_user.id):
        await bot.send_message(message.chat.id,"Hello mr. flame:", reply_markup=markup)  
        await bot.delete_message(message.chat.id, message.message_id)   
    else:
        await bot.send_message(message.chat.id,"Sorry, bot created only for owner")

@bot.callback_query_handler(func=lambda call: True)
async def Commands(call: types.CallbackQuery):
    Func_Info = FunctionsList[call.data]
    await bot.edit_message_text(Func_Info["msg"],call.message.chat.id, call.message.message_id)
    Result = Func_Info["func"]()

    if Result and path/Result:
        image = path/Result
        if isinstance(Result,str) and Result.endswith(".png"):
            with open(image, "rb") as photo:
                await bot.send_photo(call.message.chat.id, photo)
            os.remove(image)

    await bot.delete_message(call.message.chat.id,call.message.message_id)

asyncio.run(bot.infinity_polling())