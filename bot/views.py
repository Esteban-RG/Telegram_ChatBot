from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv
import os
import json

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
        # Decodificar el cuerpo de la solicitud
        json_data = request.body.decode("utf-8")
        
        # Convertir la cadena JSON a un diccionario de Python
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            # Si hay un error en la conversión, devolver un error
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Procesar la actualización con el objeto Update
        update = Update.de_json(data, application.bot)

        # Poner la actualización en la cola para ser procesada
        application.update_queue.put_nowait(update)

    # Responder con un mensaje de éxito
    return JsonResponse({"status": "ok"})
