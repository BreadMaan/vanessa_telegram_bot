# -*- coding: utf-8 -*-

import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3
from datetime import datetime

token = '6158080727:AAGvVdq3U2JJMrYbs89PBSkXag7jUTezo3E'
openai.api_key = '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'

bot = Bot(token)
dp = Dispatcher(bot)

conn = sqlite3.connect('bot_db.db', check_same_thread=False)
cursor = conn.cursor()

#Приветственное сообщение, при нажатии на кнопку start
@dp.message_handler(commands=['start'])
async def start_message(message):
	await bot.send_message(message.chat.id, 'Добро пожаловать!\nМы можем общаться на любые темы! Но помни, что я ещё учусь, поэтому, иногда, могу отвечать не совсем правильно с точки зрения грамматики. Но я обещаю, что я буду усердно развиваться в этом направлении!\nНу что, поговорим?:)')

#Вставляем нужные данные в таблицу Info
async def db_table_val(user_id: int, user_name: str, user_text: str, bot_answear: str, datetime: str):
	cursor.execute('INSERT INTO Info (user_id, user_name, user_text, bot_answear, datetime) VALUES (?, ?, ?, ?, ?)', (user_id, user_name, user_text, bot_answear, datetime))
	conn.commit()

#Отправка сообщения
@dp.message_handler()
async def send(message : types.Message):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=message.text,
    temperature=0.9,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=["You:"]
)
    #переменные для записи в БД, и справа получаемые данные
    us_id = message.from_user.id
    username = message.from_user.username
    user_message = message.text
    bot_text = response['choices'][0]['text']
    time = datetime.now()

    await db_table_val(user_id=us_id, user_name=username, user_text=user_message, bot_answear=bot_text, datetime=time)
    if message.text.lower() == 'как тебя зовут?' or message.text.lower() == 'как твое имя?' or message.text.lower() == 'как твое имя' or message.text.lower() == 'как тебя зовут' or message.text.lower() == 'твое имя?' or message.text.lower() == 'твое имя':
        await message.answer('Меня зовут Ванесса :)')
    elif message.text.lower() == 'кто тебя создал?' or message.text.lower() == 'кто тебя создал' or message.text.lower() == 'кто твой создатель?' or message.text.lower() == 'кто твой создатель' or message.text.lower() == 'кто тебя сделал?' or message.text.lower() == 'кто тебя сделал':
        await message.answer('Меня создал разработчик Vladislav Borodin :)\nЕсли вы хотите связаться с ним, напишите ему на почту - breadman.v96@gmail.com')
    elif message.text.lower() == 'ты девушка?' or message.text.lower() == 'ты девушка' or message.text.lower() == 'ты девочка?' or message.text.lower() == 'ты девочка' or message.text.lower() == 'ты женщина?' or message.text.lower() == 'ты женщина' or message.text.lower() == 'какого ты пола?' or message.text.lower() == 'какого ты пола' or message.text.lower() == 'ты женского пола?' or message.text.lower() == 'ты женского пола':
        await message.answer('Я девушка!')
    else:
        await message.answer(response['choices'][0]['text'])

executor.start_polling(dp, skip_updates=True)
