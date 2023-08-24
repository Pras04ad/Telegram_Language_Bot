from telegram import Update, ReplyKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from googletrans import Translator

SELECT_LANGUAGE, ENTER_TEXT,ANOTHER_TRANSLATION = range(3)
# Initialize the translator
translator = Translator()


# Define a function to handle the /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Translation Bot! Send me a message to translate.")
    update.message.reply_text("Which language would you like to translate to?",reply_markup=ReplyKeyboardMarkup([['English', 'Spanish'], ['French', 'German']], one_time_keyboard=True))
    return SELECT_LANGUAGE

def translate_text(update: Update, context: CallbackContext):
    context.user_data['target_language']=update.message.text.lower()
    update.message.reply_text("Please enter the text:")
    return ENTER_TEXT

# Define a function to handle text messages
def perform_translate(update: Update, context: CallbackContext):
    text = update.message.text
    target_language = context.user_data.get('target_language','en')
    translated_text = translator.translate(text, dest=target_language)  # Translate to English by default
    context.user_data['translated_text'] = translated_text.text
    update.message.reply_text(f"Translated Text:\n {translated_text.text}")
    update.message.reply_text("do you want to translate again? (yes/no)",reply_markup=ReplyKeyboardMarkup([['Yes','No']],one_time_keyboard=True))
    return ANOTHER_TRANSLATION

def ask_another_translation(update: Update, context: CallbackContext):
    choice = update.message.text.lower()
    if choice == 'yes':
        update.message.reply_text("Which language would you like to translate to?",reply_markup=ReplyKeyboardMarkup([['English', 'Spanish'], ['French', 'German']], one_time_keyboard=True))
        return SELECT_LANGUAGE
    else:
        update.message.reply_text("Goodbye!",reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

def main():
    updater = Updater("6483556471:AAFpLEpVwLNSZ9o62mnurUFhK0aUDgW2L1M")
    dispatcher = updater.dispatcher
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start",start)],
        states={
            SELECT_LANGUAGE: [MessageHandler(Filters.text & ~Filters.command, translate_text)],
            ENTER_TEXT: [MessageHandler(Filters.text & ~Filters.command, perform_translate)],
            ANOTHER_TRANSLATION: [MessageHandler(Filters.text & ~Filters.command,ask_another_translation)],
        },
                fallbacks=[]
    )
    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()