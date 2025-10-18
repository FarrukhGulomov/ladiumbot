import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ParseMode
from datetime import datetime
import json
import os

from config import *
from google_sheets import GoogleSheetsManager

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class UzumShopBot:
    def __init__(self):
        self.sheets_manager = GoogleSheetsManager()
        self.user_data = {}  # Store user data temporarily
        self.questions = {}  # Store questions from users
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Store user data
        user_info = {
            'telegram_id': user.id,
            'username': user.username or '',
            'first_name': user.first_name or '',
            'last_name': user.last_name or '',
            'phone': ''
        }
        
        # Add user to Google Sheets
        self.sheets_manager.add_user(user_info)
        
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
        contact_info = """
📞 <b>Способы связи:</b>

🛍️ <b>Наш магазин:</b> <a href="{shop_url}">Uzum.uz - Ladium</a>

📱 <b>Telegram:</b> @your_telegram_username
📧 <b>Email:</b> your_email@example.com
☎️ <b>Телефон:</b> +998 XX XXX XX XX

🕒 <b>Время работы:</b>
Пн-Пт: 9:00 - 18:00
Сб-Вс: 10:00 - 16:00
        """.format(shop_url=UZUM_SHOP_URL)
        
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
        if user_id == ADMIN_USER_ID and message_text.startswith('/broadcast '):
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
                logger.error(f"Error sending question to admin: {e}")
        
        logger.info(f"Question received from user {user.username}: {question}")
    
    async def handle_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        """Handle broadcast message from admin"""
        if update.effective_user.id != ADMIN_USER_ID:
            return
        
        # Extract message content
        broadcast_text = message.replace('/broadcast ', '')
        
        # Get all users
        users = self.sheets_manager.get_all_users()
        sent_count = 0
        failed_count = 0
        
        for user in users:
            try:
                telegram_id = user.get('Telegram ID')
                if telegram_id:
                    await context.bot.send_message(
                        chat_id=int(telegram_id),
                        text=broadcast_text,
                        parse_mode=ParseMode.HTML
                    )
                    sent_count += 1
                    
                    # Update user activity
                    self.sheets_manager.update_user_activity(telegram_id)
                    
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
        if update.effective_user.id != ADMIN_USER_ID:
            await update.message.reply_text("Эта команда доступна только администратору")
            return
        
        user_count = self.sheets_manager.get_user_count()
        questions_count = len(self.questions)
        
        stats_message = f"""
📊 <b>Статистика бота:</b>

👥 <b>Всего пользователей:</b> {user_count}
❓ <b>Вопросов в очереди:</b> {questions_count}
🕒 <b>Время:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        await update.message.reply_text(stats_message, parse_mode=ParseMode.HTML)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        if update.effective_user.id == ADMIN_USER_ID:
            await update.message.reply_text(ADMIN_HELP_MESSAGE, parse_mode=ParseMode.HTML)
        else:
            help_text = """
🤖 <b>Помощь по боту:</b>

/start - Запустить бота
/help - Показать это сообщение

Используйте кнопки меню для навигации:
• 🛍️ Перейти в магазин
• ❓ Задать вопрос
• 📞 Связаться с нами
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
    """Main function to run the bot"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    # Create bot instance
    bot = UzumShopBot()
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("stats", bot.stats_command))
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    
    # Add error handler
    application.add_error_handler(bot.error_handler)
    
    # Start the bot
    logger.info("Starting Uzum Shop Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
