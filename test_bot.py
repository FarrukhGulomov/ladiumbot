#!/usr/bin/env python3
"""
Test version of Uzum Shop Telegram Bot
This version can run for testing without full configuration
"""

import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Test configuration (replace with your actual values)
TEST_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your actual bot token
TEST_ADMIN_ID = 123456789  # Replace with your actual Telegram user ID
UZUM_SHOP_URL = "https://uzum.uz/ru/shop/ladium"

# Test messages
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

class TestUzumShopBot:
    def __init__(self):
        self.user_data = {}
        self.questions = {}
        self.users = []  # Simple in-memory storage for testing
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Store user data (simplified for testing)
        user_info = {
            'telegram_id': user.id,
            'username': user.username or '',
            'first_name': user.first_name or '',
            'last_name': user.last_name or '',
            'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add to users list if not already there
        if not any(u['telegram_id'] == user.id for u in self.users):
            self.users.append(user_info)
            logger.info(f"New user registered: {user.username} ({user.id})")
        
        # Create keyboard with shop button
        keyboard = [
            [InlineKeyboardButton("🛍️ Перейти в магазин", url=UZUM_SHOP_URL)],
            [InlineKeyboardButton("❓ Задать вопрос", callback_data="ask_question")],
            [InlineKeyboardButton("📞 Связаться с нами", callback_data="contact")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send welcome message
        await update.message.reply_text(
            WELCOME_MESSAGE,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        logger.info(f"User {user.username} started the bot")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "ask_question":
            await self.handle_question_request(query, context)
        elif query.data == "contact":
            await self.handle_contact_request(query, context)
        elif query.data == "back_to_main":
            await self.show_main_menu(query, context)
    
    async def handle_question_request(self, query, context):
        """Handle when user wants to ask a question"""
        self.user_data[query.from_user.id] = {'state': 'waiting_for_question'}
        
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "❓ Пожалуйста, напишите ваш вопрос, и мы ответим вам в ближайшее время:",
            reply_markup=reply_markup
        )
    
    async def handle_contact_request(self, query, context):
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
    
    async def show_main_menu(self, query, context):
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
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Check if user is waiting to ask a question
        if user_id in self.user_data and self.user_data[user_id].get('state') == 'waiting_for_question':
            await self.process_question(update, context, message_text)
            return
        
        # Check if message is from admin
        if user_id == TEST_ADMIN_ID and message_text.startswith('/broadcast '):
            await self.handle_broadcast(update, context, message_text)
            return
        
        # Default response
        await update.message.reply_text(
            "Для навигации используйте кнопки меню или команду /start"
        )
    
    async def process_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE, question: str):
        """Process user question"""
        user = update.effective_user
        
        # Store the question
        self.questions[user.id] = {
            'question': question,
            'user_info': {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'telegram_id': user.id
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Clear user state
        if user.id in self.user_data:
            del self.user_data[user.id]
        
        # Send confirmation to user
        await update.message.reply_text(QUESTION_RECEIVED_MESSAGE)
        
        # Notify admin about new question
        if TEST_ADMIN_ID:
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
                    chat_id=TEST_ADMIN_ID,
                    text=admin_message,
                    parse_mode=ParseMode.HTML
                )
            except Exception as e:
                logger.error(f"Error sending question to admin: {e}")
        
        logger.info(f"Question received from user {user.username}: {question}")
    
    async def handle_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        """Handle broadcast message from admin"""
        if update.effective_user.id != TEST_ADMIN_ID:
            return
        
        # Extract message content
        broadcast_text = message.replace('/broadcast ', '')
        
        # Send to all users (simplified for testing)
        sent_count = 0
        failed_count = 0
        
        for user in self.users:
            try:
                telegram_id = user.get('telegram_id')
                if telegram_id:
                    await context.bot.send_message(
                        chat_id=int(telegram_id),
                        text=broadcast_text,
                        parse_mode=ParseMode.HTML
                    )
                    sent_count += 1
                    
            except Exception as e:
                logger.error(f"Error sending broadcast to user {telegram_id}: {e}")
                failed_count += 1
        
        # Send report to admin
        report = f"""
📊 <b>Отчет о рассылке:</b>

✅ Отправлено: {sent_count}
❌ Ошибок: {failed_count}
📝 Сообщение: {broadcast_text[:50]}...
        """
        
        await update.message.reply_text(report, parse_mode=ParseMode.HTML)
        logger.info(f"Broadcast sent to {sent_count} users, {failed_count} failed")
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command for admin"""
        if update.effective_user.id != TEST_ADMIN_ID:
            await update.message.reply_text("Эта команда доступна только администратору")
            return
        
        user_count = len(self.users)
        questions_count = len(self.questions)
        
        stats_message = f"""
📊 <b>Статистика бота (ТЕСТОВЫЙ РЕЖИМ):</b>

👥 <b>Всего пользователей:</b> {user_count}
❓ <b>Вопросов в очереди:</b> {questions_count}
🕒 <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 <b>Пользователи:</b>
"""
        
        for user in self.users[:5]:  # Show first 5 users
            stats_message += f"• {user['first_name']} (@{user['username'] or 'no_username'})\n"
        
        if len(self.users) > 5:
            stats_message += f"... и еще {len(self.users) - 5} пользователей"
        
        await update.message.reply_text(stats_message, parse_mode=ParseMode.HTML)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        if update.effective_user.id == TEST_ADMIN_ID:
            help_text = """
🔧 <b>Команды администратора (ТЕСТОВЫЙ РЕЖИМ):</b>

/start - Запустить бота
/broadcast <сообщение> - Отправить сообщение всем пользователям
/stats - Показать статистику пользователей
/help - Показать это сообщение

⚠️ <b>Внимание:</b> Это тестовая версия бота!
Данные хранятся в памяти и будут потеряны при перезапуске.
            """
        else:
            help_text = """
🤖 <b>Помощь по боту:</b>

/start - Запустить бота
/help - Показать это сообщение

Используйте кнопки меню для навигации:
• 🛍️ Перейти в магазин
• ❓ Задать вопрос
• 📞 Связаться с нами

⚠️ <b>Внимание:</b> Это тестовая версия бота!
            """
        await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            try:
                await update.effective_message.reply_text(
                    "Произошла ошибка. Пожалуйста, попробуйте еще раз или используйте /start"
                )
            except Exception as e:
                logger.error(f"Error sending error message: {e}")

def main():
    """Main function to run the test bot"""
    if TEST_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Please set your actual bot token in TEST_BOT_TOKEN variable")
        print("Get your bot token from @BotFather on Telegram")
        return
    
    if TEST_ADMIN_ID == 123456789:
        print("❌ ERROR: Please set your actual Telegram user ID in TEST_ADMIN_ID variable")
        print("Get your user ID from @userinfobot on Telegram")
        return
    
    # Create bot instance
    bot = TestUzumShopBot()
    
    # Create application
    application = Application.builder().token(TEST_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("stats", bot.stats_command))
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Add error handler
    application.add_error_handler(bot.error_handler)
    
    # Start the bot
    print("🚀 Starting Uzum Shop Bot (TEST MODE)...")
    print("⚠️  This is a test version - data will be lost on restart")
    print("Press Ctrl+C to stop the bot")
    print("-" * 50)
    
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
