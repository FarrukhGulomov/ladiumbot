# 🚀 Quick Setup Instructions for Uzum Shop Bot

## Step 1: Get Your Bot Token

1. **Open Telegram** and search for `@BotFather`
2. **Start a chat** with BotFather
3. **Send** `/newbot`
4. **Choose a name** for your bot (e.g., "Ladium Shop Bot")
5. **Choose a username** (must end with 'bot', e.g., "ladium_shop_bot")
6. **Copy the token** that BotFather gives you (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Step 2: Get Your User ID

1. **Open Telegram** and search for `@userinfobot`
2. **Start a chat** with userinfobot
3. **Copy your user ID** (a number like: `123456789`)

## Step 3: Configure the Bot

1. **Open** `simple_test_bot.py` in your editor
2. **Find these lines** (around line 15-16):
   ```python
   BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
   ADMIN_USER_ID = 123456789  # Get from @userinfobot
   ```
3. **Replace** `YOUR_BOT_TOKEN_HERE` with your actual bot token
4. **Replace** `123456789` with your actual user ID

## Step 4: Run the Bot

Open PowerShell in your project folder and run:
```powershell
py simple_test_bot.py
```

## Step 5: Test the Bot

1. **Find your bot** on Telegram (search for the username you created)
2. **Start a chat** with your bot
3. **Send** `/start` to test
4. **Try the buttons** to see if they work

## Bot Features to Test:

### ✅ User Features:
- `/start` - Shows welcome message with buttons
- **🛍️ Shop button** - Opens your Uzum shop
- **❓ Question button** - Lets users ask questions
- **📞 Contact button** - Shows contact information

### ✅ Admin Features (only for you):
- `/stats` - Shows user statistics
- `/broadcast <message>` - Sends message to all users
- **Question notifications** - You get notified when users ask questions

## Example Test:

1. **Start the bot** with `/start`
2. **Click "❓ Задать вопрос"**
3. **Type a test question** like "Hello, this is a test"
4. **Check your Telegram** - you should receive a notification about the question
5. **Try** `/stats` to see the user count

## Troubleshooting:

### ❌ "Bot token not found"
- Make sure you copied the token correctly from @BotFather
- Check that there are no extra spaces in the token

### ❌ "User ID not found"
- Make sure you got your ID from @userinfobot
- The ID should be just numbers, no @ symbol

### ❌ Bot doesn't respond
- Check that the bot is running (you should see "Bot started" message)
- Make sure you're messaging the correct bot username
- Try sending `/start` first

### ❌ Buttons don't work
- This is normal for the first few seconds after starting
- Wait a moment and try again
- Make sure you're using the latest version of Telegram

## Next Steps:

Once the simple bot is working:

1. **Set up Google Sheets** for full functionality
2. **Deploy to a server** for 24/7 operation
3. **Customize messages** and add more features

## Need Help?

If you have any issues:
1. Check the console output for error messages
2. Make sure all dependencies are installed
3. Verify your bot token and user ID are correct
4. Try restarting the bot

---

**Your bot is ready to help customers find your Uzum shop! 🎉**
