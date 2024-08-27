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
#my_chat_id = -1001900713107
my_chat_id = -1001958494022




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
If message is not realated to "сдачи квартир / жилье" - send a pure message   "False"
if the price has nnot detected, put "Договор"
"""
example ="""
Instance:

🟢Сдаю в аренду🟢

Please format the response as follows, ensuring each piece of information is on a new line:

🏠Цена:\n{info_here}\n
📍Район:\n{info_here}\n
📝Описание:\n{info_here and other infos}\n
📞Контакты:\n{info_here_if_so}\n

\n
tags:

"""
rules_ai = """
rules:
No commands
no parse mode! <- this is important
send me python object,dictinary
also rate  this in 10. if structure quite good:10 othervise, your own by spell, scrupture, and by fields
"""


example_a = """
this is a instance:
🏠Цена:\n{info_here}\n
📍Район:\n{info_here}\n
📝Описание:\n{info_here and other infos}\n
📞Контакты:\n{info_here_if_so}\n
"""

ai_text =[
{"role": "user","content": f"Будешь помогать улучшать посты"},
{"role": "user","content": f"Правила:{rules_ai}"},
{"role": "user","content": f"{example_a}"},

{
  "role": "assistant",
  "content": "Вот шаги, которые я выполнял для улучшения и форматирования поста:\n\n1. **Получение исходного текста**: \n   - Получил текст объявления от пользователя.\n\n2. **Анализ текста**:\n   - Определил ключевые элементы поста: цена, район, описание, контакты.\n\n3. **Форматирование**:\n   - Разделил текст на логические блоки: цена, район, описание, контакты.\n   - Добавил разделительные пробелы и эмодзи для улучшения визуальной структуры.\n\n4. **Оптимизация формулировок**:\n   - Упростил и улучшил текст, чтобы он был более читабельным и понятным.\n\n5. **Создание JSON-структуры**:\n   - Форматировал текст в структуру JSON, объединив информацию под одним ключом \"post\".\n\n6. **Форматирование для передачи**:\n   - Убедился, что JSON-структура содержит текст в виде строки с правильными разделителями.\n\n**Итоговый пример JSON-объекта:**\n\n{\n rate:★ ?/10  \"post\": \"🏠 Цена: Цену тут\\n\\n📍 Район: Район тут\\n\\n📝 Описание: Описание тут.\\n\\n📞 Контакты: Информация тут\"\n}"
},
{"role": "user","content": f"Запомни! Без всяких комментариев"},
]


client_op = Client()
client_help = Client()



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




m_messages = []
async def verify_ai(text):
    result = None 
    global MODEL,PROVIDER,rules_ai, example_a, ai_text
    instance = ai_text
    instance.append({"role": "user","content": f"{text}"})
    response = client_help.chat.completions.create(
    model=MODEL,
    provider =PROVIDER,
    messages = instance,)
    result = response.choices[0].message.content
    data = result[8:len(result)-4]
    # my ai check code here
    return data

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

@dp.callback_query_handler(lambda call: True)
async def handle_callback(call: CallbackQuery):
    global m_messages,posts
    if call.message:
       if call.data.startswith("done"):
          await asyncio.sleep(10)
          for post in posts:
              if post.get(call.message.message_id) == post['id']:
                 print(post)
                 break
              await bot.edit_message_text('Ok',call.chat.id,call.message_id)


import json

posts = []

async def check_message(message, chat_id):
    global posts
    the_text = message.text
    the_message_id = message.message_id
    global m_messages
    reply_message = await message.reply('Оцениваем...',disable_notification=True,)
    # First verification
    text_ai = await verify_ai(the_text)
    verify_markup = InlineKeyboardMarkup()
    verify_button = InlineKeyboardButton("А, что лучшее?", callback_data=f'done_{the_message_id}')
    verify_markup.add(verify_button)
    posts.append({f'post':json.loads(text_ai)['post'],'id':reply_message.message_id,})
    print(posts)
    if text_ai == 'True':
        # If the message is fine, delete the "checking" reply
        await bot.delete_message(chat_id, reply_message.message_id)
    else:
        # If the message needs correction, notify the user
        await bot.edit_message_text(f"Meta rate: \n\n{json.loads(text_ai)['rate']}", 
                                    chat_id,
                                    reply_message.message_id,
                                    parse_mode="Markdown",
                                    reply_markup=verify_markup,
                                    )
        
        # Fetch the original message again (simulate delay)
        m_messages.append(the_message_id)
        # Wait for 30 seconds before second verification
#        await asyncio.sleep(25)  # Replaces threading with asyncio sleep
#        await bot.delete_message(chat_id,reply_message.message_id)

async def is_admin_or_creator(chat_id: int, user_id: int) -> bool:
    """
    Universal function to check if the user is an admin or creator in the chat.
    """
    # Get the chat member details
    chat_member = await bot.get_chat_member(chat_id, user_id)
    
    # Check if the user is an administrator or creator
    return chat_member.status in ['administrator', 'creator']

"""
@dp.edited_message_handler(content_types=types.ContentType.TEXT)
async def handle_edited_message(edited_message: types.Message):
    if await is_admin_or_creator(edited_message.chat.id,edited_message.from_user.id):
       return 
    global my_chat_id,m_messages
    message_id = edited_message.message_id
    new_text = edited_message.text
    if edited_message.chat.id == my_chat_id:
       response = await verify_ai(edited_message)
       print(response)
       if response == "True":
          m_messages.remove(edited_message.message_id)
    return
"""

@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    if await is_admin_or_creator(message.chat.id,message.from_user.id):
       return
    global my_chat_id,m_messages
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    if chat_id == my_chat_id:
       await check_message(message,chat_id)

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

