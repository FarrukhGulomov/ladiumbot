#!/usr/bin/env python3
"""
Modern Uzum Shop Bot - Compatible with latest telegram library
"""

import logging
import asyncio
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode
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

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    user = update.effective_user
    
    # Store user data
    user_info = {
        'telegram_id': user.id,
        'username': user.username or '',
        'first_name': user.first_name or '',
        'last_name': user.last_name or '',
        'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Add to users if not exists
    if not any(u['telegram_id'] == user.id for u in users):
        users.append(user_info)
        logger.info(f"New user: {user.username} ({user.id})")
    
    # Create keyboard
    keyboard = [
        [InlineKeyboardButton("🛍️ Перейти в магазин", url=UZUM_SHOP_URL)],
        [InlineKeyboardButton("❓ Задать вопрос", callback_data="ask_question")],
        [InlineKeyboardButton("📞 Связаться с нами", callback_data="contact")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    
    logger.info(f"User {user.username} started the bot")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "ask_question":
        await handle_question_request(query, context)
    elif query.data == "contact":
        await handle_contact_request(query, context)
    elif query.data == "back_to_main":
        await show_main_menu(query, context)

async def handle_question_request(query, context):
    """Handle question request"""
    user_data[query.from_user.id] = {'state': 'waiting_for_question'}
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "❓ Пожалуйста, напишите ваш вопрос, и мы ответим вам в ближайшее время:",
        reply_markup=reply_markup
    )

async def handle_contact_request(query, context):
    """Handle contact request"""
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
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        contact_info,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

async def show_main_menu(query, context):
    """Show main menu"""
    keyboard = [
        [InlineKeyboardButton("🛍️ Перейти в магазин", url=UZUM_SHOP_URL)],
        [InlineKeyboardButton("❓ Задать вопрос", callback_data="ask_question")],
        [InlineKeyboardButton("📞 Связаться с нами", callback_data="contact")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        WELCOME_MESSAGE,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # Check if waiting for question
    if user_id in user_data and user_data[user_id].get('state') == 'waiting_for_question':
        await process_question(update, context, message_text)
        return
    
    # Check admin broadcast
    if user_id == ADMIN_USER_ID and message_text.startswith('/broadcast '):
        await handle_broadcast(update, context, message_text)
        return
    
    # Default response
    await update.message.reply_text(
        "Для навигации используйте кнопки меню или команду /start"
    )

async def process_question(update: Update, context: ContextTypes.DEFAULT_TYPE, question: str):
    """Process user question"""
    user = update.effective_user
    
    # Store question
    questions.append({
        'question': question,
        'user': f"{user.first_name} {user.last_name or ''} (@{user.username or 'no_username'})",
        'user_id': user.id,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Clear state
    if user.id in user_data:
        del user_data[user.id]
    
    # Send confirmation
    await update.message.reply_text(QUESTION_RECEIVED_MESSAGE)
    
    # Notify admin
    if ADMIN_USER_ID:
        admin_message = f"""
🔔 <b>Новый вопрос от пользователя:</b>

👤 <b>Пользователь:</b> {user.first_name} {user.last_name or ''}
📝 <b>Username:</b> @{user.username or 'не указан'}
🆔 <b>ID:</b> {user.id}

❓ <b>Вопрос:</b>
{question}

⏰ <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_USER_ID,
                text=admin_message,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Error sending to admin: {e}")
    
    logger.info(f"Question from {user.username}: {question}")

async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
    """Handle broadcast"""
    if update.effective_user.id != ADMIN_USER_ID:
        return
    
    broadcast_text = message.replace('/broadcast ', '')
    sent_count = 0
    failed_count = 0
    
    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user['telegram_id'],
                text=broadcast_text,
                parse_mode=ParseMode.HTML
            )
            sent_count += 1
        except Exception as e:
            logger.error(f"Error sending to {user['telegram_id']}: {e}")
            failed_count += 1
    
    report = f"""
📊 <b>Отчет о рассылке:</b>

✅ Отправлено: {sent_count}
❌ Ошибок: {failed_count}
📝 Сообщение: {broadcast_text[:50]}...
    """
    
    await update.message.reply_text(report, parse_mode=ParseMode.HTML)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show stats"""
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("Эта команда доступна только администратору")
        return
    
    stats_message = f"""
📊 <b>Статистика бота:</b>

👥 <b>Всего пользователей:</b> {len(users)}
❓ <b>Вопросов:</b> {len(questions)}
🕒 <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 <b>Последние пользователи:</b>
"""
    
    for user in users[-5:]:  # Last 5 users
        stats_message += f"• {user['first_name']} (@{user['username'] or 'no_username'})\n"
    
    await update.message.reply_text(stats_message, parse_mode=ParseMode.HTML)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    if update.effective_user.id == ADMIN_USER_ID:
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
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Main function"""
    print("🚀 Starting Uzum Shop Bot...")
    print("📁 Using configuration from .env file")
    print("⚠️  Using in-memory storage (data will be lost on restart)")
    print("-" * 50)
    
    if not BOT_TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN not found in .env file")
        print("Please add your bot token to the .env file")
        return
    
    if not ADMIN_USER_ID:
        print("❌ ERROR: ADMIN_USER_ID not found in .env file")
        print("Please add your user ID to the .env file")
        return
    
    print(f"✅ Bot Token: {BOT_TOKEN[:10]}...")
    print(f"✅ Admin ID: {ADMIN_USER_ID}")
    print(f"✅ Shop URL: {UZUM_SHOP_URL}")
    print("-" * 50)
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    print("✅ Bot handlers configured")
    print("✅ Starting bot...")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        print("🎉 Bot is now running and ready to receive messages!")
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
