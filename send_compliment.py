import os
import asyncio
import random
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
import openai
from dotenv import load_dotenv
import time

load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
your_number = os.getenv("YOUR_PHONE_NUMBER")
her_number = os.getenv("HER_PHONE_NUMBER")
openai.api_key = os.getenv("OPENAI_API_KEY")
girl_name = os.getenv("GIRL_NAME")
girl_personality_traits = os.getenv("GIRL_PERSONALITY_TRAITS").split('|')
compliment_hours_array = [int(i) for i in os.getenv("COMPLIMENT_HOURS").split(',')]

async def generate_compliment(name: str, trait: str) -> str:
    prompt = f"Создай небольшой комплимент для девушки по имени {name}. Комплимент должен быть по тематике: {trait}"
    print(f"Запрос: {prompt}")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text

async def send_compliment():
    client = TelegramClient('anon', api_id, api_hash)

    await client.start(your_number)

    if await client.is_user_authorized():
        print("Авторизация успешна")
    else:
        print("Авторизация не удалась")

    try:
        # Получаем информацию о контакте
        contact = await client.get_entity(her_number)

        # Генерируем комплимент и отправляем его контакту
        random_trait = random.choice(girl_personality_traits)
        compliment = await generate_compliment(girl_name, random_trait)
        await client.send_message(contact, compliment)
        print(f"Отправлено сообщение: {compliment}")

    finally:
        await client.disconnect()

def should_send_compliment():
    current_hour = time.localtime().tm_hour
    return current_hour in compliment_hours_array

def job():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_compliment())

job()

while True:
    if should_send_compliment():
        job()
        time.sleep(3600)  # Sleep for an hour after sending a compliment
    else:
        time.sleep(60)  # Sleep for a minute before checking again