from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import filters, ConversationHandler, ApplicationBuilder, MessageHandler, CallbackQueryHandler, CommandHandler, ContextTypes

PUNTUADO, ENCUESTA, RESPUESTA, SALUDO = ["puntuado", "encuesta","respuesta", "saludo"]

#Definimos el botón para poder usarlo en las opciones
async def button(update, context):
    query = update.callback_query
    if query.data == "SI":
        print("si")
        result = f"✅ Sumade a !"
        
    else:
        print("NO")
        result = f'❌ Proyecto salteado.'
        text = "no"

    await context.bot.edit_message_text(text=result,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)

#Saludamos y preguntamos si quieren hacer la encuesta
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hola! Soy un bot amigable y muy curioso :)"
    )
    
    return await crear_boton(update, context,
                                 "Te gustaría completar una pequeña encuesta?", "Me Sumo!", 
                                 "Paso", RESPUESTA)

async def respuesta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text=update.callback_query.data
    query = update.callback_query

    if text == "SI" or text =="S":
        result = f"✅ Sumade a la encuesta!"
        await context.bot.edit_message_text(text=result,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)

        username = update.callback_query.from_user.username

        await context.bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text= username + """, si tuvieras que calificar el PyCamp 2024, que puntaje le pondrías del 1 al 5 ?
            1 = no me gusto, no vengo nunca más
            2 = no estoy seguro si volvería
            3 = zafa
            4 = Muy BUENO
            5 = CUANDO ES EL PROXIMO QUE QUIERO ESTARRRRR ?
            0 = Terminar la encuesta
            """
        )
        return ENCUESTA
    elif text == "NO" or text == "N":
        await context.bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text="Quizás la puedas completar más adelante."
        )
        result = f'❌ Descartade de la encuesta.'
        await context.bot.edit_message_text(text=result,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        return ConversationHandler.END
    else:
        await context.bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text="La respuesta debería ser SI o NO."
        )
        return RESPUESTA

async def puntaje_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    text = update.message.text

    if text in ["1", "2", "3"]:
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Ok {}! Tu puntaje es: {}".format(username, text)
        )

        return await crear_boton(update, context,
                                    "Te gustaría explicarnos tu calificación?",
                                    "Claro que si!", "Paso", PUNTUADO)
    elif text == "4":
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Ok {}! Tu puntaje es: {}".format(username, text)
        )

        return await crear_boton(update, context,
                                    "Nos vemos en la próxima PyCamp. Nos ayudas con algunos tips?",
                                    "Claro que si!", "Paso", PUNTUADO)
    elif text == "5":
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Ok {}! Tu puntaje es: {}".format(username, text)
        )

        return await crear_boton(update, context,
                                    "Gracias por tu respuesta " + username + ".\nTe gustaría dejarnos alguna sugerencia para el próximo PyCamp?",
                                    "Claro que si!", "Paso", PUNTUADO)
    elif text == "0":
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Decidiste terminar la encuesta. Gracias {} por participar.".format(username)
        )
        return ConversationHandler.END
    else:
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Nooooooo la opción elegida no existe, por favor ingresá 1, 2, 3, 4, 5 o 0 (para salir)"
        )
        return ENCUESTA
    
async def respuesta_puntaje(update, context):
    username = update.callback_query.from_user.username
    text=update.callback_query.data
    query = update.callback_query

    if text == "SI" or text =="S":
        result = f"✅ Tus consejos suman!"
        await context.bot.edit_message_text(text=result,
                            chat_id=query.message.chat_id,
                            message_id=query.message.message_id)
        username = update.callback_query.from_user.username

        await context.bot.send_message(
        chat_id=update.callback_query.from_user.id,
        text= username + ", escribe a continuación, te leemos:"
        )
        return SALUDO
    elif text == "NO" or text == "N":
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Gracias por tu tiempo. Ojalá te volvamos a ver el año que viene."
        )
        result = f'❌ Descartade de la encuesta.'
        await context.bot.edit_message_text(text=result,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id)
        return ConversationHandler.END
    else:
        await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="La respuesta debería ser SI o NO."
        )
        return PUNTUADO
    
async def saludo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Gracias, tu respuesta nos ayuda a mejorar, nos vemos pronto " + username + "."
        )
    return ConversationHandler.END

async def cancel(update, context):
    await context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Has cancelado")
    return ConversationHandler.END

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=update.message.text)
    
async def descargaryoutube(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="No AMIGUE, eso es ilegal, no es por acá :)"
        )
    
async def crear_boton(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text, texto_si, texto_no, next_state):
    keyboard = [[InlineKeyboardButton(texto_si, callback_data="SI"),
                 InlineKeyboardButton(texto_no, callback_data="NO")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text,
        reply_markup=reply_markup
    )
    return next_state

echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
descargaryoutube_handler = CommandHandler('descargaryoutube', descargaryoutube)

load_project_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        RESPUESTA: [MessageHandler(CallbackQueryHandler(button), respuesta)],
        ENCUESTA: [MessageHandler(filters.TEXT, puntaje_level)],
        PUNTUADO: [MessageHandler(CallbackQueryHandler(button), respuesta_puntaje)],
        SALUDO: [MessageHandler(filters.TEXT, saludo)]
        },
    fallbacks=[CommandHandler('cancel', cancel)])
    
def set_handlers(application):
    application.add_handler(load_project_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(echo_handler)
    application.add_handler(descargaryoutube_handler)