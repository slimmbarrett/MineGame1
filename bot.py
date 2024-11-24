from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import logging
from typing import Dict

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Константы
BOT_TOKEN = '7537994303:AAG15uJYwAmzVINLchNmzIjZ7So95RdkpdI'
CHANNEL_ID = 'cashgeneratorUBT'
CHANNEL_URL = f"https://t.me/{CHANNEL_ID}"
WIN_URL = "https://1wxxlb.com/casino/list?open=register&p=dsgq"
WEB_APP_URL = 'https://mine1win.vercel.app/'

# Словарь для хранения языка пользователей
user_language: Dict[int, str] = {}

# Многоязычные сообщения
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
    },
    'hi': {
        'welcome': "नमस्ते [USERNAME]!\n🚩जारी रखने के लिए हमारे टेलीग्राम चैनल को सब्सक्राइब करें!\n\n🔔 यह आपको कोई महत्वपूर्ण सिग्नल न छूटने में मदद करेगा! 🚀",
        'check_subscription': "सदस्यता की जाँच करें!",
        'channel': "चैनल",
        'not_subscribed': "जारी रखने के लिए कृपया हमारे चैनल को सब्सक्राइब करें!",
        'ref_link': "🎉 यहाँ हमारे पार्टनर का रेफरल लिंक है! 🎉\n\n🚨 महत्वपूर्ण चेतावनी!🚨\n\nअगर आप इस लिंक से रजिस्टर नहीं करते हैं, तो बॉट गलत परिणाम दिखा सकता है! ⚠️\n\nप्रोमो कोड भूलें नहीं - CashGen 💸",
        'final_message': "🚀 कैश जेनरेटर से MineGames — आपका भाग्य आजमाने का मौका! 💰\n\nहमारे बॉट के साथ आपको MINE गेम में 92% पास रेट मिलेगा! 🎯 बिना अतिरिक्त जोखिम के गेम का आनंद लें और जीतें! 🎉\n\nमौका न छोड़ें — अभी शुरू करें! 💥\n\n'Mine 92%✅' बटन पर क्लिक करें"
    },
    'pt': {
        'welcome': "Olá [USERNAME]!\n🚩Você deve se inscrever em nosso canal do Telegram para continuar!\n\n🔔 Isso ajudará você a não perder nenhum sinal importante! 🚀",
        'check_subscription': "Verificar inscrição!",
        'channel': "Canal",
        'not_subscribed': "Por favor, inscreva-se em nosso canal para continuar!",
        'ref_link': "🎉 Aqui está o link de referência para nosso parceiro! 🎉\n\n🚨 Aviso importante!🚨\n\nSe você não se registrar usando este link, o bot pode mostrar resultados incorretos! ⚠️\n\nNÃO ESQUEÇA DE USAR O CÓDIGO PROMOCIONAL - CashGen 💸",
        'final_message': "🚀 MineGames do Gerador de Dinheiro — sua chance de testar sua sorte! 💰\n\nCom nosso bot você terá 92% de taxa de aprovação no jogo MINE! 🎯 Aproveite o jogo sem risco extra e ganhe! 🎉\n\nNão perca sua chance — comece agora! 💥\n\nCLIQUE NO BOTÃO 'Mine 92%✅'"
    }
}

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру выбора языка"""
    keyboard = [
        [
            InlineKeyboardButton("English 🇬🇧", callback_data='lang_en'),
            InlineKeyboardButton("Русский 🇷🇺", callback_data='lang_ru')
        ],
        [
            InlineKeyboardButton("हिंदी 🇮🇳", callback_data='lang_hi'),
            InlineKeyboardButton("Português 🇵🇹", callback_data='lang_pt')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_subscription_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Создает клавиатуру для проверки подписки"""
    keyboard = [
        [
            InlineKeyboardButton(messages[lang]['channel'], url=CHANNEL_URL),
            InlineKeyboardButton(messages[lang]['check_subscription'], callback_data='check_sub')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_game_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для игры"""
    keyboard = [
        [
            InlineKeyboardButton("1WIN", url=WIN_URL),
            InlineKeyboardButton("Mine 92%✅", web_app=WebAppInfo(url=WEB_APP_URL))
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def check_subscription(bot, user_id: int) -> bool:
    """Проверяет подписку пользователя на канал"""
    try:
        logger.debug(f"Checking subscription for user {user_id}")
        member = await bot.get_chat_member(chat_id=f"@{CHANNEL_ID}", user_id=user_id)
        logger.debug(f"Member status: {member.status}")
        return member.status in ['member', 'administrator', 'creator', 'restricted']
    except Exception as e:
        logger.error(f"Error checking subscription: {str(e)}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    try:
        user = update.effective_user
        logger.info(f"Start command received from user {user.id}")
        
        # Отправляем клавиатуру выбора языка
        await update.message.reply_text(
            "👋 Choose your language / Выберите язык:",
            reply_markup=get_language_keyboard()
        )
        logger.info(f"Language keyboard sent to user {user.id}")
        
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}")
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="An error occurred. Please try /start again."
            )
        except Exception as retry_error:
            logger.error(f"Failed to send error message: {str(retry_error)}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    try:
        query = update.callback_query
        await query.answer()  # Сразу отвечаем на callback query
        
        user_id = query.from_user.id
        logger.info(f"Button callback from user {user_id}: {query.data}")
        
        if query.data.startswith('lang_'):
            lang = query.data.split('_')[1]
            user_language[user_id] = lang
            welcome_text = messages[lang]['welcome'].replace('[USERNAME]', query.from_user.first_name)
            await query.edit_message_text(text=welcome_text, reply_markup=get_subscription_keyboard(lang))
            logger.info(f"Language {lang} set for user {user_id}")
            
        elif query.data == 'check_sub':
            lang = user_language.get(user_id, 'en')
            is_subscribed = await check_subscription(context.bot, user_id)
            logger.info(f"Subscription check for user {user_id}: {is_subscribed}")
            
            if is_subscribed:
                await query.edit_message_text(text=messages[lang]['ref_link'], reply_markup=get_game_keyboard())
                await context.bot.send_message(chat_id=user_id, text=messages[lang]['final_message'])
                logger.info(f"Game keyboard sent to user {user_id}")
            else:
                await query.answer(messages[lang]['not_subscribed'], show_alert=True)
                logger.info(f"Subscription check failed for user {user_id}")
                
    except Exception as e:
        logger.error(f"Error in button callback: {str(e)}")
        try:
            await query.answer("An error occurred. Please try again.", show_alert=True)
        except:
            pass

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик всех текстовых сообщений"""
    try:
        user_id = update.effective_user.id
        logger.debug(f"Received message from user {user_id}: {update.message.text}")
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")

def main() -> None:
    """Запуск бота"""
    try:
        # Создаем приложение
        logger.info("Starting bot application...")
        application = Application.builder().token(BOT_TOKEN).build()

        # Добавляем обработчики
        logger.info("Adding handlers...")
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Запускаем бота
        logger.info("Starting bot polling...")
        application.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"Critical error: {str(e)}")
        raise

if __name__ == '__main__':
    main()
