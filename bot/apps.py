import os
import asyncio
import threading
from django.apps import AppConfig
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        # Token del bot de Telegram
        BOT_TOKEN = os.getenv('telegram_api_key')
        WEBHOOK_URL = "https://telegram-chatbot-3g83.onrender.com/webhook/"  # Cambia esto a tu dominio

        # Función para establecer el webhook
        async def set_webhook():
            bot = Bot(token=BOT_TOKEN)
            await bot.set_webhook(WEBHOOK_URL)

        # Ejecutar la configuración del webhook en un hilo separado para evitar bloquear el hilo principal de Django
        threading.Thread(target=lambda: asyncio.run(set_webhook())).start()
