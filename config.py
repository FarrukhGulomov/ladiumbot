import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE', 'credentials.json')
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')

# Shop Configuration
UZUM_SHOP_URL = os.getenv('UZUM_SHOP_URL', 'https://uzum.uz/ru/shop/ladium')

# Admin Configuration
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))

# Bot Messages
WELCOME_MESSAGE = """
🎉 Добро пожаловать в наш магазин Ladium на Uzum!

Я помогу вам:
• Получить информацию о наших товарах
• Ответить на ваши вопросы
• Связать вас с нашим магазином

Нажмите кнопку ниже, чтобы перейти в наш магазин:
"""

SHOP_REDIRECT_MESSAGE = """
🛍️ Переходите в наш магазин на Uzum.uz!

Здесь вы найдете:
• Качественные товары
• Быструю доставку
• Отличные цены
• Скидки и акции

Нажмите кнопку, чтобы открыть магазин:
"""

QUESTION_RECEIVED_MESSAGE = """
✅ Ваш вопрос получен!

Мы ответим вам в ближайшее время. 
Спасибо за обращение! 🙏
"""

ADMIN_HELP_MESSAGE = """
🔧 Команды администратора:

/start - Запустить бота
/broadcast <сообщение> - Отправить сообщение всем пользователям
/stats - Показать статистику пользователей
/help - Показать это сообщение
"""
