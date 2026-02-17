import asyncio
import os
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from dotenv import load_dotenv
load_dotenv("Bot.env")

Bot_token = str(os.getenv("Key"))
Myself = os.getenv("ID")
bot = AsyncTeleBot(Bot_token)

@bot.message_handler(commands=["start"])
async def AlreadyConnected(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    TestFunc1 = types.KeyboardButton("Untitled 1")
    TestFunc2 = types.KeyboardButton("Untitled 2")
    TestFunc3 = types.KeyboardButton("Выключение пк🚫")
    markup.row(TestFunc1,TestFunc2)
    markup.row(TestFunc3)

    if message.from_user.id == Myself:
        await bot.send_message(message.chat.id,"Здравствуйте создатель🙂", reply_markup=markup)     
    else:
        await bot.send_message(message.chat.id,"Здравствуйте, пока что бот находится в стадии разработки и не работает ни у кого, кроме создателя")

@bot.message_handler(content_types="text")
async def Commands(message: types.Message):
    await bot.reply_to(message, "Проверка...")
    if message.from_user.id == Myself:
        if message.text == "Выключение пк🚫":
            await bot.reply_to(message, "Выключение ПК...")
            os.system("shutdown /s")
        else:
            await bot.reply_to(message, "Что-то не так...")

asyncio.run(bot.infinity_polling())