import asyncio
from django.apps import AppConfig
from telegram import Bot
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()



class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'


    def ready(self):
        BOT_TOKEN = os.getenv('telegram_api_key')
        WEBHOOK_URL = "https://telegram-chatbot-3g83.onrender.com/webhook/"  # Cambia esto a tu dominio
        
        async def set_webhook():
            bot = Bot(token=BOT_TOKEN)
            await bot.set_webhook(WEBHOOK_URL)

        asyncio.run(set_webhook())