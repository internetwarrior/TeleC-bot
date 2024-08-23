from telethon.sync import TelegramClient, events

# Ваши API ID и hash
api_id = 21643158
api_hash = '3af2df2f47d3cad630e183c8d56a0ea5'

with TelegramClient('name', api_id, api_hash) as client:
    # Пример отправки сообщения себе
    client.send_message('me', 'Hello, myself!')
    print(client.download_profile_photo('me'))

    # Обработчик новых сообщений
    @client.on(events.NewMessage)
    async def handler(event):
        # Получаем информацию об отправителе сообщения
        sender = await event.get_sender()
        sender_name = sender.username if sender.username else sender.first_name

        # Проверяем, является ли сообщение из группы
        if event.is_group:
            print(f'Новое сообщение в группе от {sender_name}: {event.text}')

    # Ожидание событий и поддержка соединения
    client.run_until_disconnected()
