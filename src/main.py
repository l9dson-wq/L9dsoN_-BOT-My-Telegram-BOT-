"""
Este software fue creado por Andelson Lopez. 
This software was created by Andelson Lopez.
Correo electronico o Email: andelsonprogrammer@gmail.com
"""

import os
import sys 
import logging #Para ver lo que hace el bot
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from funciones import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger()

#consiguiendo las credenciales con mi token
TOKEN = os.getenv('TOKEN')

eventos = "El evento es: "

#verificar si el usuario que envio el comando es admin o no
def user_is_admin(chatId, userId, bot):
    try:
        groupAdmins = bot.get_chat_administrators(chatId)
        for admin in groupAdmins:
            if admin.user.id == userId:
                isAdmin = True #si sale verdadero quiere decir que el usuario tiene permisos de administrador en el grupo
            else:
                isAdmin = False

        return isAdmin
    except Exception as es:
        print("No se pudo completar por alguna razon")

def addEvent(update, context):
    global eventos
    bot = context.bot
    chatId = update.message.chat_id
    userName = update.effective_user["first_name"]
    userId = update.effective_user['id']
    args = context.args

    if user_is_admin(chatId, userId, bot) == True:
        if len(args) == 0:
            logger.info(f"el usuario {userName} no ha ingresado argumentos")
            context.bot.sendAnimation(
                chat_id = chatId,
                animation = "https://tenor.com/buApE.gif",
                caption=f"{userName} debes ingresar mas informacion para agregar el evento"
            )
        else:
            evento = ' '.join(args)
            eventos = eventos + '\n>>' + evento

            logger.info(f'el usuario {userName} ha ingresado un nuevo envento')

            context.bot.sendAnimation(
                chat_id = chatId,
                animation="https://tenor.com/ZD80.gif",
                caption=f"El admin {userName} ha ingresado un evento"
            )
    else:
        logger.info(f"{userName} ha intentado agregar un evento pero no tiene permisos")
        context.bot.sendAnimation(
            chat_id = chatId,
            animation="https://tenor.com/YxQD.gif",
            caption=f"El usuario {userName} no tiene permisos para ejecutar este comando 🛑"
        )        

#imprimir todos los eventos que se han ingresado
def event(update,context):
    chatId = update.message.chat_id
    userName = update.effective_user['first_name']
    bot = context.bot

    logger.info(f"el usuario {userName} ha solicitado eventos")
    bot.sendMessage(
        chat_id = chatId,
        text = eventos
    )

#funcion para dar la bienvenido a los usuarios nuevos
def welcomeUser(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    updateMsg = getattr(update, "message", None)
    for user in updateMsg.new_chat_members:
        userName = user.first_name

    logger.info(f"El usuario {userName} ha ingresado al grupo")

    context.bot.sendAnimation(
        chat_id=chatId,
        animation="https://tenor.com/view/party-time-jolly-cheerful-confetti-gif-16628356",
        caption=f"Bievenido al grupo! {userName} 🥳🥳"
    )

#funcion para eliminar el mensaje enviado desde la funcion echo
def deleteMessage(bot, chatId, messageId, usrName):
    try:
        bot.delete_message(chatId, messageId)
        logger.info(f"el mensaje del usuario {userName} se elimino porque contenia malas palabras")
    except Exception as e:
        print(e)



#funcion para la palabra reservado echo
def echo(update, context):
    bot = context.bot
    updateMsg = getattr(update, "message", None)
    messageId = updateMsg.message_id #obtener el id del mensaje
    chatId = update.message.chat_id
    userName = update.effective_user["first_name"]
    text = update.message.text #obtener el texto que envio el usuario al chat
    logger.info(f" el usuario {userName} ha enviado un nuevo mensaje al grupo {chatId}")

    #Palabras groseras para eliminar del chat
    badWord = [
        'singa tu madre',
        "Mmg",
        'mmg',
        'idiota',
        'ridiculo',
        'buen mmg',
        'buen singa tu madre',
        'singa perra',
        'loco el diablo',
        'hijo e perra'
        ]

    for x in badWord:
        if x in text:
            deleteMessage(bot, chatId, messageId, userName)
            context.bot.sendAnimation(
                chat_id=chatId, 
                animation="https://tenor.com/bbpYs.gif",
                caption=f"el mensaje del usuario {userName} se ha eliminado por que contenia malas palabras"
                )

    if 'hola' in text and 'bot' in text:
        context.bot.sendAnimation(
            chat_id=chatId,
            animation="https://tenor.com/bfd0n.gif",
            caption=f"Hola {userName}! gracias por saludas."
        )
    elif 'Hola' in text and 'bot' in text:
        context.bot.sendAnimation(
            chat_id=chatId,
            animation="https://tenor.com/bfd0n.gif",
            caption=f"Hola {userName}! gracias por saludas."
        )



if __name__ == "__main__":
    #obtener informacion del bot
    myBot = telegram.Bot(token = TOKEN)
    #print(myBot.getMe())

#update se conecta y recibe los mensajes
updater = Updater(myBot.token, use_context=True)

#create dispatcher
dp = updater.dispatcher

#manejador, create command
dp.add_handler(CommandHandler("github", githubCretor))
dp.add_handler(CommandHandler("help", helpBot))
dp.add_handler(CommandHandler("creator", infoCreator))
dp.add_handler(CommandHandler("botInfo", getBotInfo))
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("addEvent", addEvent, pass_args=True))
dp.add_handler(CommandHandler("events", event))
#obtener el status de los nuevos miembros del chat
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcomeUser))
#para estar leyendo los mensajes
dp.add_handler(MessageHandler(Filters.text, echo))


updater.start_polling() #estar preguntando por mensajes entrantes
print("BOT RUNNING") # para saber si el bot esta corriendo correctamente
updater.idle() #terminar bot con ctrl + e
