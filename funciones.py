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
       ●▬▬▬▬▬ஜ۩INFORMACION۩ஜ▬▬▬▬▬●
        📝 /creator - Muestra el nombre de mi administrador.
        📝 /help - Muestra una lista de los comandos.
        📝 /botInfo - Muestra informacion acerca de mi.
        📝 /start - Imprime un breve mensaje de lo que seria iniciarla.
        📝 /github - Muestra el GitHub del desarrollador.
        ●▬▬▬▬▬ஜ۩EVENTS(admins)۩ஜ▬▬▬▬▬●  
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

    #enviando un gig con el bot con la etiqueta "sendAnimation" 
    context.bot.sendAnimation(chat_id=chatId, animation="https://tenor.com/bkqCq.gif",caption="Hola, soy un bot creado con el proposito de hacer la vida de un grupo un poco mas alegre")


def githubCretor(update, context):
    chatId = update.message.chat_id
    userName = update.effective_user['first_name']
    bot = context.bot

    logger.info(f"El usuario {userName} ha solicitado tu GitHub")
    bot.sendMessage(
        chat_id = chatId,
        text = """ Este es el GitHub del creador y administrador del Bot
        https://github.com/l9dson-wq"""
    )
