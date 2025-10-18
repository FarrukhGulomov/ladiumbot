# 🚀 Quick Configuration Guide

## Step 1: Get Your Bot Token

1. **Open Telegram** and search for `@BotFather`
2. **Start a chat** and send `/newbot`
3. **Choose a name** like "Ladium Shop Bot"
4. **Choose a username** like "ladium_shop_bot" (must end with 'bot')
5. **Copy the token** (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Step 2: Get Your User ID

1. **Open Telegram** and search for `@userinfobot`
2. **Start a chat** and it will show your user ID
3. **Copy the number** (like: `123456789`)

## Step 3: Configure the Simple Bot

1. **Open** `simple_test_bot.py` in your editor
2. **Find these lines** (around line 15-16):
   ```python
   BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
   ADMIN_USER_ID = 123456789  # Get from @userinfobot
   ```
3. **Replace** `YOUR_BOT_TOKEN_HERE` with your actual bot token
4. **Replace** `123456789` with your actual user ID

## Step 4: Run the Bot

```bash
py simple_test_bot.py
```

## Step 5: Test Your Bot

1. **Find your bot** on Telegram (search for the username you created)
2. **Start a chat** with your bot
3. **Send** `/start`
4. **Try the buttons** to see if they work

## Example Configuration:

```python
# Replace these with your actual values:
BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"  # Your bot token
ADMIN_USER_ID = 987654321  # Your user ID
```

## What to Test:

✅ **Send** `/start` - Should show welcome message with buttons  
✅ **Click** "🛍️ Перейти в магазин" - Should open your Uzum shop  
✅ **Click** "❓ Задать вопрос" - Should let you type a question  
✅ **Type a question** - You should get a notification  
✅ **Try** `/stats` - Should show user statistics  
✅ **Try** `/broadcast Hello!` - Should send message to all users  

## Troubleshooting:

- **Bot not responding?** Check your token is correct
- **Buttons not working?** Wait a few seconds and try again
- **Admin commands not working?** Check your user ID is correct

---

**Ready to test your Uzum shop bot! 🎉**
