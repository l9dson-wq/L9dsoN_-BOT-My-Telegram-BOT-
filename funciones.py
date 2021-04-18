import os
import sys 
import logging #Para ver lo que hace el bot
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger()

#funcion para decir el nombre del creado
def infoCreator(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    userName = update.effective_user["first_name"]
    text = update.message.text

    bot.sendMessage(
        chat_id = chatId,
        text = f"{userName} mi creador es Andelson Lopez!"
    )

#funcion para mostrar los comandos del bot
def helpBot(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    userName = update.effective_user["first_name"]
    text = update.message.text

    bot.sendMessage(
        chat_id = chatId,
        parse_mode = 'HTML',
        text = f""" COMANDOS:
        ███▓▒░░informacion 🤔░░▒▓███  
        📝 /creator - Muestra el nombre de mi administrador.
        📝 /help - Muestra una lista de los comandos.
        📝 /botInfo - Muestra informacion acerca de mi.
        📝 /start - Imprime un breve mensaje de lo que seria iniciarla.
        ███▓▒░░curiosos 🙃░░▒▓███  
        📝 /addEvent - agregar un evento.
        📝 /events - ver todos los eventos agregados.


        @l9dson - Andelson Lopez
        """
    )

#creando la funcion para la palabra clave start
def start(update, context):
    bot = context.bot
    userName = update.effective_user["first_name"]
    update.message.reply_text(f"hola {userName} gracias por invocarme")



#creando la funcion para la palabra getInfo
def getBotInfo(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f'El usuario {userName} ha solicitado informacion sobre el bot')
 
    context.bot.sendPhoto(chat_id=chatId, photo="https://i.imgur.com/7zb9ED3.jpeg", caption="Hola, soy un bot creado con el proposito de hacer la vida de un grupo un poco mas alegre'")
    #bot.send_photo(chat_id, '')


def addEvent(update, context):
    global evento
    bot = context.bot
    chatId = update.message.chat_id
    userName = update.effective_user["first_name"]
    userId = update.effective_user['id']
    args = context.args

    if user_is_admin(chatId, userId, bot) == True:
        if len(args) == 0:
            logger.info(f"el usuario {userName} no ha ingresado argumentos")
            bot.sendMessage(
                chat_id= chatId,
                text=f"{userName} por favor ingrese mas informacion para agregar el evento"
            )
        else:
            evento = ' '.join(args)
            eventos = eventos + '\n>>' + evento

            logger.info(f'el usuario {userName} ha ingresado un nuevo envento')

            bot.sendMessage(
                chat_id = chatId,
                text=f"{userName} has ingresado un evento correctamente"
            )
    else:
        bot.sendMessage(
            chat_id = chatId,
            text = f"el usuario {userName} no tiene permisos para ejecutar este comando"
        )

def event(update,context):
    chatId = update.message.chat_id
    userName = update.effective_user['first_name']
    bot = context.bot

    logger.info(f"el usuario {userName} ha solicitado eventos")
    bot.sendMessage(
        chat_id = chatId,
        text = eventos
    )
