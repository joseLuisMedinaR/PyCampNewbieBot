import logging
from telegram.ext import ApplicationBuilder
from config import TOKEN
#from base import start_handler, echo_handler
import base 
from ejemplo import ejemplo_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    
    #application.add_handler(start_handler)
    base.set_handlers(application)
    application.add_handler(ejemplo_handler)
    application.run_polling()