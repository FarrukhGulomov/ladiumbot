#!/usr/bin/env python3
"""
MVP Uzum Shop Bot - Simple redirect to shop
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

# Simple welcome message
WELCOME_MESSAGE = """
🛍️ Добро пожаловать в наш магазин Ladium на Uzum!

Нажмите кнопку ниже, чтобы перейти в наш магазин:
"""

# Global variables
users = []
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
    """Handle /start command - redirect to shop"""
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
    is_new_user = not any(u['telegram_id'] == user['id'] for u in users)
    if is_new_user:
        users.append(user_info)
        logger.info(f"🆕 NEW USER REGISTERED: {user.get('first_name', '')} {user.get('last_name', '')} (@{user.get('username', 'no_username')}) - ID: {user['id']}")
    else:
        logger.info(f"👤 RETURNING USER: {user.get('first_name', '')} {user.get('last_name', '')} (@{user.get('username', 'no_username')}) - ID: {user['id']}")
    
    # Create simple keyboard with only shop button
    keyboard = {
        'inline_keyboard': [
            [{'text': '🛍️ Перейти в магазин Ladium', 'url': UZUM_SHOP_URL}]
        ]
    }
    
    send_message(chat_id, WELCOME_MESSAGE, keyboard)
    logger.info(f"🛍️ USER REDIRECTED TO SHOP: {user.get('username', 'no_username')} - Total users: {len(users)}")

def handle_message(update):
    """Handle text messages"""
    user = update['message']['from']
    chat_id = update['message']['chat']['id']
    text = update['message']['text']
    user_id = user['id']
    
    # Handle /start command
    if text == '/start':
        handle_start_command(update)
        return
    
    # Handle /stats command for admin
    if text == '/stats' and user_id == ADMIN_USER_ID:
        handle_stats_command(chat_id)
        return
    
    # Log any other message
    logger.info(f"💬 MESSAGE FROM USER: {user.get('username', 'no_username')} - Text: '{text}'")
    
    # For any other message, show the shop button
    keyboard = {
        'inline_keyboard': [
            [{'text': '🛍️ Перейти в магазин Ladium', 'url': UZUM_SHOP_URL}]
        ]
    }
    
    send_message(chat_id, "Нажмите кнопку ниже, чтобы перейти в наш магазин:", keyboard)

def handle_stats_command(chat_id):
    """Handle stats command for admin"""
    stats_message = f"""
📊 <b>Статистика бота:</b>

👥 <b>Всего пользователей:</b> {len(users)}
🕒 <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 <b>Последние пользователи:</b>
"""
    
    for user in users[-5:]:  # Last 5 users
        stats_message += f"• {user['first_name']} (@{user['username'] or 'no_username'})\n"
    
    send_message(chat_id, stats_message)

def main():
    """Main function"""
    global last_update_id
    
    print("🚀 Starting Uzum Shop Bot (MVP version)...")
    print("📁 Using configuration from .env file")
    print("🎯 MVP: Simple redirect to Uzum shop")
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
    print("✅ Bot is now running and ready to redirect users to your shop!")
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
            
            time.sleep(1)  # Wait 1 second before next check
            
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
