from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Tu token de bot
BOT_TOKEN = os.getenv('telegram_api_key')

# Crea la aplicación del bot
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Comando /start
async def start(update, context):
    await update.message.reply_text("¡Hola! Este bot usa Django y un webhook.")

# Registrar el comando
application.add_handler(CommandHandler("start", start))

# Vista para manejar el webhook
@csrf_exempt
def webhook(request):
    if request.method == "POST":
        json_data = request.body.decode("utf-8")
        update = Update.de_json(json_data, application.bot)
        # Procesa la actualización con la aplicación
        application.update_queue.put_nowait(update)
    return JsonResponse({"status": "ok"})
