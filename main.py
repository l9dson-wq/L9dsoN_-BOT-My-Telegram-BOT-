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
        groupAdmins = bot.get_chat_adminstrators(chatId)
        for admin in groupAdmins:
            if admin.user.id == userId:
                isAdmin = True
            else:
                isAdmin = False

        return isAdmin
    except Exception as es:
        print(es)


#funcion para dar la bienvenido a los usuarios nuevos
def welcomeUser(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    updateMsg = getattr(update, "message", None)
    for user in updateMsg.new_chat_members:
        userName = user.first_name

    logger.info(f"El usuario {userName} ha ingresado al grupo")

    bot.sendMessage(
        chat_id = chatId,
        parse_mode = "HTML",
        text = f"<b>Bienvenido al grupo! {userName} </b> \nespero que te la pases de maravilla con notros!!!</b>"
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

    badWord = ['singa tu madre',"Mmg",'mmg'] #palabrsa groseras, podria hacer una lista con esto
    for x in badWord:
        if x in text:
            deleteMessage(bot, chatId, messageId, userName)
            bot.sendMessage(
                chat_id = chatId,
                text=f"el mensaje del usuario {userName} se ha eliminado por que contenia malas palabras"
            )
    if 'hola' in text and 'bot' in text:
        bot.sendMessage(
            chat_id=chatId,
            text= f'Hola {userName}! gracias por saludar.'
        ) 
    elif 'Hola' in text and 'bot' in text:
        bot.sendMessage(
            chat_id=chatId,
            text= f'Hola {userName}! gracias por saludar.'
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
