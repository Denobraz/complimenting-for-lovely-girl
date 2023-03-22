import os
import asyncio
import random
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import openai
from dotenv import load_dotenv
import schedule
import time

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone_number = os.getenv("PHONE_NUMBER")
contact_phone_number = os.getenv("CONTACT_PHONE_NUMBER")
openai.api_key = os.getenv("OPENAI_API_KEY")
girl_name = os.getenv("GIRL_NAME")

async def generate_compliment(name: str) -> str:
    prompt = f"Создай небольшой комплимент для девушки по имени {name}."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text

async def send_compliment():
    client = TelegramClient('anon', api_id, api_hash)

    await client.start(phone_number)

    if await client.is_user_authorized():
        print("Авторизация успешна")
    else:
        print("Авторизация не удалась")

    try:
        # Получаем информацию о контакте
        contact = await client.get_entity(contact_phone_number)

        # Генерируем комплимент и отправляем его контакту
        compliment = await generate_compliment(girl_name)
        await client.send_message(contact, compliment)
        print(f"Отправлено сообщение: {compliment}")

    finally:
        await client.disconnect()

def job():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_compliment())

# Запланировать отправку комплимента каждый день в определенное время (например, 12:00)
schedule.every(3).hours.do(job)

job()

while True:
   schedule.run_pending()
   time.sleep(1)