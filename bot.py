from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import logging
from typing import Dict

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Константы
BOT_TOKEN = '8115585479:AAH8qgvFN-KX1G08DCFUfEb0jVykVEn2SE4'
CHANNEL_ID = 'cashgeneratorUBT'
CHANNEL_URL = f"https://t.me/{CHANNEL_ID}"
WIN_URL = "https://1wxxlb.com/casino/list?open=register&p=dsgq"
WEB_APP_URL = 'https://mine1win.vercel.app/'
VIDEO_URL = 'https://github.com/slimmbarrett/MineGame1/raw/main/CASH%20LOGO.mp4'

# Глобальная переменная для хранения языка пользователя
user_language: Dict[int, str] = {}

# Сообщения для разных языков
messages = {
    'en': {
        'welcome': "Hello [USERNAME]!\n🚩You must subscribe to our Telegram channel to continue!\n\n🔔 This will help you not miss any important signals! 🚀",
        'check_subscription': "Check subscription!",
        'channel': "Channel",
        'not_subscribed': "Please subscribe to our channel to continue!",
        'ref_link': "🎉 Here's the referral link to our partner! 🎉\n\n🚨 Important warning!🚨\n\nIf you don't register using this link, the bot may show incorrect results! ⚠️\n\nDON'T FORGET TO USE PROMO CODE - CashGen 💸",
        'final_message': "🚀 MineGames from Cash Generator — your chance to test your luck! 💰\n\nWith our bot you'll get 92% pass rate in MINE game! 🎯 Enjoy the game without extra risk and win! 🎉\n\nDon't miss your chance — start right now! 💥\n\nCLICK THE 'Mine 92%✅' BUTTON"
    },
    'ru': {
        'welcome': "Привет [USERNAME]!\n🚩Обязательно подпишитесь на наш Telegram-канал, чтобы продолжить!\n\n🔔 Это поможет не пропустить ни одного важного сигнала! 🚀",
        'check_subscription': "Проверка подписки!",
        'channel': "Канал",
        'not_subscribed': "Пожалуйста, подпишитесь на наш канал, чтобы продолжить!",
        'ref_link': "🎉 Вот реферальная ссылка на нашего партнера! 🎉\n\n🚨 Важное предупреждение!🚨\n\nЕсли вы не зарегистрируетесь по этой ссылке, бот может показывать неверные результаты! ⚠️\n\nНЕ ЗАБУДЬ УКАЗАТЬ ПРОМОКОД - CashGen 💸",
        'final_message': "🚀 MineGames от Генератора Кэша — ваш шанс испытать удачу! 💰\n\nС нашим ботом вы получите 92% проходимость в игре MINE! 🎯 Наслаждайтесь игрой без лишнего риска и выигрывайте! 🎉\n\nНе упустите шанс — начните прямо сейчас! 💥\n\nНАЖМИ НА КНОПКУ 'Mine 92%✅'"
    }
}

# Генерация клавиатуры выбора языка
def get_language_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("English 🇬🇧", callback_data='lang_en'),
            InlineKeyboardButton("Русский 🇷🇺", callback_data='lang_ru')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Генерация клавиатуры подписки
def get_subscription_keyboard(lang: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(messages[lang]['channel'], url=CHANNEL_URL),
            InlineKeyboardButton(messages[lang]['check_subscription'], callback_data='check_sub')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Генерация клавиатуры игры
def get_game_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("1WIN", url=WIN_URL),
            InlineKeyboardButton("Mine 92%✅", web_app=WebAppInfo(url=WEB_APP_URL))
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Проверка подписки пользователя
async def check_subscription(bot, user_id: int) -> bool:
    try:
        logger.debug(f"Checking subscription for user {user_id}")
        member = await bot.get_chat_member(chat_id=f"@{CHANNEL_ID}", user_id=user_id)
        logger.debug(f"Member status: {member.status}")
        return member.status in ['member', 'administrator', 'creator', 'restricted']
    except Exception as e:
        logger.error(f"Error checking subscription: {e}")
        return False

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    try:
        logger.debug(f"Start command received from user {user.id}")
        await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=VIDEO_URL,
            caption="👋 Choose your language / Выберите язык:",
            reply_markup=get_language_keyboard()
        )
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text(
            "👋 Choose your language / Выберите язык:",
            reply_markup=get_language_keyboard()
        )

# Обработка кнопок
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    
    if query.data.startswith('lang_'):
        lang = query.data.split('_')[1]
        user_language[user_id] = lang
        welcome_text = messages[lang]['welcome'].replace('[USERNAME]', query.from_user.first_name)
        await query.edit_message_text(text=welcome_text, reply_markup=get_subscription_keyboard(lang))
    elif query.data == 'check_sub':
        lang = user_language.get(user_id, 'en')
        is_subscribed = await check_subscription(context.bot, user_id)
        if is_subscribed:
            await query.edit_message_text(text=messages[lang]['ref_link'], reply_markup=get_game_keyboard())
        else:
            await query.answer(messages[lang]['not_subscribed'], show_alert=True)

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    logger.debug(f"Received message from user {user_id}: {update.message.text}")

# Основная функция
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Starting bot...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
