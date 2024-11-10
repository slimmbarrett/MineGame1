from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Вставьте ваш токен сюда
BOT_TOKEN = '7537994303:AAG15uJYwAmzVINLchNmzIjZ7So95RdkpdI'

# URL вашего Web App
WEB_APP_URL = 'https://mine-game1.vercel.app/'

def start(update: Update, context: CallbackContext) -> None:
    # Кнопка с веб-приложением
    keyboard = [
        [InlineKeyboardButton("Начать игру", web_app={"url": WEB_APP_URL})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем приветственное сообщение с кнопкой
    update.message.reply_text(
        'Добро пожаловать в MineGames! Нажмите кнопку, чтобы начать игру.',
        reply_markup=reply_markup
    )

def main() -> None:
    # Создаем экземпляр бота и передаем токен
    updater = Updater(BOT_TOKEN)

    # Получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Обрабатываем команду /start
    dispatcher.add_handler(CommandHandler('start', start))

    # Запускаем бота
    updater.start_polling()

    # Ожидаем завершения
    updater.idle()

if __name__ == '__main__':
    main()
