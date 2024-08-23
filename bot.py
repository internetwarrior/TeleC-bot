from telethon.sync import TelegramClient, events
import asyncio
import g4f
from telethon.sync import TelegramClient, events
from g4f.client import Client
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TARGET_GROUPS = [1346340387,1325827931,1900280237,]
API_TOKEN = '7526226887:AAG7r_OMhWoT5OBUuk7X-8TZ87laQaLEPkY'
OPENAI_API_KEY = '42d516ee05fa42e08ce6497e5e40c161'
MODEL = "gpt-3.5-turbo"
PROVIDER = g4f.Provider.You
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

system_content = """
Rules:
Always Follow the instance
Only result.
No comments!
No parse mode!
Improve th post	
Lang targets:
Russian-Ru,
Kyrgyzstan-Kg
put some tages from key words: Adress/boys/girls/cityparts/family/some keyword. expample: #девушки #подселение
Choose between based by context and be carefully!:
- 🟡Ищу квартиру🟡
- 🟢Сдаю в аренду🟢
If message is not realated to "По аренды и сдачи квартир / жилье" - send a pure message   "False"
if the price has nnot detected, put "Договор"
"""
example ="""
Instance:

🟡Ищу квартиру🟡 || 🟢Сдаю в аренду🟢

Please format the response as follows, ensuring each piece of information is on a new line:

🏠Цена:\n{info_here}\n
📍Район:\n{info_here}\n
📝Описание:\n{info_here and other infos}\n
📞Контакты:\n{info_here_if_so}\n

\n
tags:

"""



client_op = Client()




@dp.message_handler(commands=['getid'])
async def send_chat_id(message: types.Message):
    chat_id = message.chat.id
    await message.reply(f"Chat ID: {chat_id}")



@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Видео вот тут @renting_kg")



async def generate(user_content):
    global system_content,example,MODEL,PROVIDER
    response = client_op.chat.completions.create(
    model=MODEL,
    provider =PROVIDER,
    messages=[{"role": "user", "content": f"{system_content} {example}. Target: {user_content}"}],)
    generated_text = response.choices[0].message.content
 
    result = types.InlineQueryResultArticle(
                id='2',
               
                title="Нажмите сюда",
                description=f"{generated_text}",
                input_message_content=types.InputTextMessageContent(
                    message_text=f"{generated_text}",
#parse_mode='Markdown',
),
)
    return generated_text
        

@dp.inline_handler()
async def inline_youtube_handler(query: types.InlineQuery):
    user_input = query.query    
    if user_input:
        result = types.InlineQueryResultArticle(
            id='1',
            title=f"Напишите объявление {len(user_input)} из 250",
            description="Если закончили, напишите подконец <=",
            input_message_content=types.InputTextMessageContent(
                message_text=f"Внимание\n {user_input}"
            ),
        )
        
        if user_input.strip().endswith('<='):
            finish = await generate(user_input)
            await query.answer([finish], cache_time=1)
        else:
            await query.answer([result], cache_time=1)
        
    else:
        await query.answer([], switch_pm_text="Как исползывать? Жми сюда", switch_pm_parameter="start")










async def send_message(chat_id: int, text: str):
    await bot.send_message(chat_id, text)




# Ваши API ID и hash
api_id = 21643158
api_hash = '3af2df2f47d3cad630e183c8d56a0ea5'

with TelegramClient('name', api_id, api_hash) as client:
    # Пример отправки сообщения себе
    client.send_message('me', 'Hello, myself!')

    # Обработчик новых сообщений
    @client.on(events.NewMessage)
    async def handler(event):
        # Получаем информацию о чате (группе) и отправителе
        chat = await event.get_chat()
        sender = await event.get_sender()
        # Проверяем, является ли сообщение из группы
        if chat.id in TARGET_GROUPS and event.is_group and sender.bot == False and event.text:
            if event.text and chat.id ==1325827931:
               text = await generate(event.text)
               if text != 'False':
                  await send_message(-1002215579508,text)

    if __name__ == '__main__':
        executor.start_polling(dp, skip_updates=True)
        client.run_until_disconnected()

