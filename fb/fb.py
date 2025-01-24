from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
import requests

USER_CREDENTIALS = {}

# Этапы диалога
WAITING_FOR_LOGIN, WAITING_FOR_PASSWORD, AUTHORIZED = range(3)

def authenticate(login, password):
    """Попытка авторизации на указанном сайте."""
    url = "https://xenforo.com/community/login/"
    session = requests.Session()

    try:
        response = session.get(url)
        if response.status_code != 200:
            return False

        # XenForo требует отправки данных авторизации вместе с токеном формы
        # Токен парсится из HTML страницы (упрощено для примера)
        token = "dummy_token"  # Заменить на реальный парсер токена

        data = {
            "login": login,
            "password": password,
            "_xfToken": token
        }
        login_response = session.post(url, data=data)
        return "Logout" in login_response.text
    except Exception as e:
        print(f"Ошибка при авторизации: {e}")
        return False

async def start(update: Update, context: CallbackContext):
    """Запрос логина у пользователя после старта."""
    await update.message.reply_text("Пожалуйста, введите ваш логин:")
    return WAITING_FOR_LOGIN

async def get_login(update: Update, context: CallbackContext):
    """Получение логина от пользователя."""
    USER_CREDENTIALS['login'] = update.message.text
    await update.message.reply_text("Теперь введите ваш пароль:")
    return WAITING_FOR_PASSWORD

async def get_password(update: Update, context: CallbackContext):
    """Получение пароля от пользователя."""
    USER_CREDENTIALS['password'] = update.message.text
    await update.message.reply_text("Проверяю данные...")

    if authenticate(USER_CREDENTIALS['login'], USER_CREDENTIALS['password']):
        await update.message.reply_text("Успешный вход! Вы можете загружать файлы.")
        return AUTHORIZED
    else:
        await update.message.reply_text("Ошибка входа. Пожалуйста, введите логин заново.")
        return WAITING_FOR_LOGIN

async def handle_file_upload(update: Update, context: CallbackContext):
    """Обработка загрузки файлов."""
    if not USER_CREDENTIALS.get('login') or not USER_CREDENTIALS.get('password'):
        await update.message.reply_text("Сначала необходимо авторизоваться. Введите /start для начала.")
        return

    file = update.message.document
    if file:
        await update.message.reply_text(f"Файл {file.file_name} успешно загружен!")
    else:
        await update.message.reply_text("Файл не обнаружен. Пожалуйста, отправьте документ.")

def run_application():
    """Запуск бота."""
    application = Application.builder().token("7577810924:AAFUJe7IbePe6ePUu2cXVlMLiGqOOyrg0BI").build()

    # Обработчик состояний
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_FOR_LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_login)],
            WAITING_FOR_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
            AUTHORIZED: [MessageHandler(filters.Document.ALL, handle_file_upload)],
        },
        fallbacks=[CommandHandler("start", start)]
    )

    application.add_handler(conv_handler)

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    run_application()