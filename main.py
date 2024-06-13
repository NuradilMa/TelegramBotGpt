import asyncio
import logging
import random
import openai

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from aiogram import F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Telegram Bot Token
BOT_TOKEN = "7000222767:AAH-_2RhEGFL5gztXsVeEHd6pPdBwRTbHrU"
# OpenAI API Key
OPENAI_API_KEY = "sk-proj-dDN9BZk5Uo5TPB8LBi4cT3BlbkFJkYpP0GDVLhXC3OcFvBSA"

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Movie lists
horror = ['https://www.kinopoisk.ru/film/1191026/', 'https://www.kinopoisk.ru/film/453397/', 'https://www.kinopoisk.ru/film/977288/', 'https://www.kinopoisk.ru/film/427122/', 'https://www.kinopoisk.ru/film/386/']
romantic = ['https://www.kinopoisk.ru/film/430/', 'https://www.kinopoisk.ru/film/492/', 'https://www.kinopoisk.ru/film/3090/', 'https://www.kinopoisk.ru/film/444/', 'https://www.kinopoisk.ru/film/2047/']
humor = ['https://www.kinopoisk.ru/film/42664/', 'https://www.kinopoisk.ru/film/8124/', 'https://www.kinopoisk.ru/film/42782/', 'https://www.kinopoisk.ru/film/44386/', 'https://www.kinopoisk.ru/film/46225/']
action = ['https://www.kinopoisk.ru/film/406408/', 'https://www.kinopoisk.ru/film/389/', 'https://www.kinopoisk.ru/film/420923/', 'https://www.kinopoisk.ru/film/41520/', 'https://www.kinopoisk.ru/film/1318972/']

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    url = "https://w7.pngwing.com/pngs/547/380/png-transparent-robot-waving-hand-bot-ai-robot-thumbnail.png"
    await message.answer(
        text=f"{markdown.hide_link(url)}Hello, {markdown.hbold(message.from_user.full_name)}!",
        parse_mode=ParseMode.HTML,
    )

    await message.answer("Напиши /film и выбирай фильм")

@dp.message(Command("film"))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Horror"),
        types.KeyboardButton(text="Romantic"),
        types.KeyboardButton(text="Юмор"),
        types.KeyboardButton(text="Боевик")
    )
    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

@dp.message(F.text.lower() == "horror")
async def show_horror(message: types.Message):
    await message.answer("Держи ужастик: " + random.choice(horror))

@dp.message(F.text.lower() == "romantic")
async def show_romantic(message: types.Message):
    await message.answer("Держи романтический фильм: " + random.choice(romantic))

@dp.message(F.text.lower() == "юмор")
async def show_humor(message: types.Message):
    await message.answer("Держи юмор фильм: " + random.choice(humor))

@dp.message(F.text.lower() == "боевик")
async def show_action(message: types.Message):
    await message.answer("Держи экшн фильм: " + random.choice(action))

@dp.message(Command("chatgpt"))
async def ask_chatgpt(message: types.Message):
    await message.answer("Ask something:")

@dp.message(F.text)
async def handle_gpt_request(message: types.Message):
    if message.text.startswith("/chatgpt"):
        return  # Avoid looping on the /chatgpt command itself
    
    user_question = message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can replace with "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are ChatGPT, a helpful assistant."},
            {"role": "user", "content": user_question}
        ]
    )
    
    await message.answer(response.choices[0].message['content'].strip())

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
