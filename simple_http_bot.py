#!/usr/bin/env python3
"""
Simple HTTP-based Uzum Shop Bot - Guaranteed to work
"""

import logging
import os
import requests
import json
import time
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get configuration from .env file
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))
UZUM_SHOP_URL = os.getenv('UZUM_SHOP_URL', 'https://uzum.uz/ru/shop/ladium')

# Messages
WELCOME_MESSAGE = """
🎉 Добро пожаловать в наш магазин Ladium на Uzum!

Я помогу вам:
• Получить информацию о наших товарах
• Ответить на ваши вопросы
• Связать вас с нашим магазином

Нажмите кнопку ниже, чтобы перейти в наш магазин:
"""

QUESTION_RECEIVED_MESSAGE = """
✅ Ваш вопрос получен!

Мы ответим вам в ближайшее время. 
Спасибо за обращение! 🙏
"""

# Global variables for storing data
users = []
questions = []
user_data = {}
last_update_id = 0

def send_message(chat_id, text, reply_markup=None):
    """Send message to Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return None

def edit_message(chat_id, message_id, text, reply_markup=None):
    """Edit message in Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    data = {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        logger.error(f"Error editing message: {e}")
        return None

def answer_callback_query(callback_query_id, text=None):
    """Answer callback query"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    data = {'callback_query_id': callback_query_id}
    if text:
        data['text'] = text
    
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        logger.error(f"Error answering callback: {e}")
        return None

def get_updates():
    """Get updates from Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    data = {'offset': last_update_id + 1, 'timeout': 10}
    
    try:
        response = requests.post(url, data=data)
        return response.json()
    except Exception as e:
        logger.error(f"Error getting updates: {e}")
        return None

def handle_start_command(update):
    """Handle /start command"""
    user = update['message']['from']
    chat_id = update['message']['chat']['id']
    
    # Store user data
    user_info = {
        'telegram_id': user['id'],
        'username': user.get('username', ''),
        'first_name': user.get('first_name', ''),
        'last_name': user.get('last_name', ''),
        'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Add to users if not exists
    if not any(u['telegram_id'] == user['id'] for u in users):
        users.append(user_info)
        logger.info(f"New user: {user.get('username', 'no_username')} ({user['id']})")
    
    # Create keyboard
    keyboard = {
        'inline_keyboard': [
            [{'text': '🛍️ Перейти в магазин', 'url': UZUM_SHOP_URL}],
            [{'text': '❓ Задать вопрос', 'callback_data': 'ask_question'}],
            [{'text': '📞 Связаться с нами', 'callback_data': 'contact'}]
        ]
    }
    
    send_message(chat_id, WELCOME_MESSAGE, keyboard)
    logger.info(f"User {user.get('username', 'no_username')} started the bot")

def handle_callback_query(update):
    """Handle callback queries"""
    query = update['callback_query']
    user = query['from']
    chat_id = query['message']['chat']['id']
    message_id = query['message']['message_id']
    data = query['data']
    
    answer_callback_query(query['id'])
    
    if data == "ask_question":
        user_data[user['id']] = {'state': 'waiting_for_question'}
        keyboard = {
            'inline_keyboard': [
                [{'text': '🔙 Назад', 'callback_data': 'back_to_main'}]
            ]
        }
        edit_message(chat_id, message_id, 
                    "❓ Пожалуйста, напишите ваш вопрос, и мы ответим вам в ближайшее время:",
                    keyboard)
    
    elif data == "contact":
        contact_info = f"""
📞 <b>Способы связи:</b>

🛍️ <b>Наш магазин:</b> <a href="{UZUM_SHOP_URL}">Uzum.uz - Ladium</a>

📱 <b>Telegram:</b> @your_telegram_username
📧 <b>Email:</b> your_email@example.com
☎️ <b>Телефон:</b> +998 XX XXX XX XX

🕒 <b>Время работы:</b>
Пн-Пт: 9:00 - 18:00
Сб-Вс: 10:00 - 16:00
        """
        keyboard = {
            'inline_keyboard': [
                [{'text': '🔙 Назад', 'callback_data': 'back_to_main'}]
            ]
        }
        edit_message(chat_id, message_id, contact_info, keyboard)
    
    elif data == "back_to_main":
        keyboard = {
            'inline_keyboard': [
                [{'text': '🛍️ Перейти в магазин', 'url': UZUM_SHOP_URL}],
                [{'text': '❓ Задать вопрос', 'callback_data': 'ask_question'}],
                [{'text': '📞 Связаться с нами', 'callback_data': 'contact'}]
            ]
        }
        edit_message(chat_id, message_id, WELCOME_MESSAGE, keyboard)

def handle_message(update):
    """Handle text messages"""
    user = update['message']['from']
    chat_id = update['message']['chat']['id']
    text = update['message']['text']
    user_id = user['id']
    
    # Check if waiting for question
    if user_id in user_data and user_data[user_id].get('state') == 'waiting_for_question':
        process_question(user, text)
        return
    
    # Check admin broadcast
    if user_id == ADMIN_USER_ID and text.startswith('/broadcast '):
        handle_broadcast(user, text)
        return
    
    # Check other commands
    if text == '/start':
        handle_start_command(update)
        return
    elif text == '/help':
        handle_help_command(user, chat_id)
        return
    elif text == '/stats' and user_id == ADMIN_USER_ID:
        handle_stats_command(chat_id)
        return
    
    # Default response
    send_message(chat_id, "Для навигации используйте кнопки меню или команду /start")

def process_question(user, question):
    """Process user question"""
    # Store question
    questions.append({
        'question': question,
        'user': f"{user.get('first_name', '')} {user.get('last_name', '')} (@{user.get('username', 'no_username')})",
        'user_id': user['id'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Clear state
    if user['id'] in user_data:
        del user_data[user['id']]
    
    # Send confirmation
    send_message(user['id'], QUESTION_RECEIVED_MESSAGE)
    
    # Notify admin
    if ADMIN_USER_ID:
        admin_message = f"""
🔔 <b>Новый вопрос от пользователя:</b>

👤 <b>Пользователь:</b> {user.get('first_name', '')} {user.get('last_name', '')}
📝 <b>Username:</b> @{user.get('username', 'не указан')}
🆔 <b>ID:</b> {user['id']}

❓ <b>Вопрос:</b>
{question}

⏰ <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        send_message(ADMIN_USER_ID, admin_message)
    
    logger.info(f"Question from {user.get('username', 'no_username')}: {question}")

def handle_broadcast(user, message):
    """Handle broadcast"""
    if user['id'] != ADMIN_USER_ID:
        return
    
    broadcast_text = message.replace('/broadcast ', '')
    sent_count = 0
    failed_count = 0
    
    for user_data in users:
        try:
            result = send_message(user_data['telegram_id'], broadcast_text)
            if result and result.get('ok'):
                sent_count += 1
            else:
                failed_count += 1
        except Exception as e:
            logger.error(f"Error sending to {user_data['telegram_id']}: {e}")
            failed_count += 1
    
    report = f"""
📊 <b>Отчет о рассылке:</b>

✅ Отправлено: {sent_count}
❌ Ошибок: {failed_count}
📝 Сообщение: {broadcast_text[:50]}...
    """
    send_message(user['id'], report)

def handle_help_command(user, chat_id):
    """Handle help command"""
    if user['id'] == ADMIN_USER_ID:
        help_text = """
🔧 <b>Команды администратора:</b>

/start - Запустить бота
/broadcast <сообщение> - Отправить всем пользователям
/stats - Показать статистику
/help - Показать помощь
        """
    else:
        help_text = """
🤖 <b>Помощь по боту:</b>

/start - Запустить бота
/help - Показать помощь

Используйте кнопки меню для навигации.
        """
    send_message(chat_id, help_text)

def handle_stats_command(chat_id):
    """Handle stats command"""
    stats_message = f"""
📊 <b>Статистика бота:</b>

👥 <b>Всего пользователей:</b> {len(users)}
❓ <b>Вопросов:</b> {len(questions)}
🕒 <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 <b>Последние пользователи:</b>
"""
    
    for user in users[-5:]:  # Last 5 users
        stats_message += f"• {user['first_name']} (@{user['username'] or 'no_username'})\n"
    
    send_message(chat_id, stats_message)

def main():
    """Main function"""
    global last_update_id
    
    print("🚀 Starting Uzum Shop Bot (HTTP version)...")
    print("📁 Using configuration from .env file")
    print("⚠️  Using in-memory storage (data will be lost on restart)")
    print("-" * 50)
    
    if not BOT_TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN not found in .env file")
        return
    
    if not ADMIN_USER_ID:
        print("❌ ERROR: ADMIN_USER_ID not found in .env file")
        return
    
    print(f"✅ Bot Token: {BOT_TOKEN[:10]}...")
    print(f"✅ Admin ID: {ADMIN_USER_ID}")
    print(f"✅ Shop URL: {UZUM_SHOP_URL}")
    print("-" * 50)
    print("✅ Bot is now running and ready to receive messages!")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        while True:
            updates = get_updates()
            if updates and updates.get('ok'):
                for update in updates['result']:
                    last_update_id = update['update_id']
                    
                    if 'message' in update:
                        handle_message(update)
                    elif 'callback_query' in update:
                        handle_callback_query(update)
            
            time.sleep(1)  # Wait 1 second before next check
            
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
