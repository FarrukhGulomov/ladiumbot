# Uzum Shop Telegram Bot

A professional Telegram bot for managing customers and directing them to your Uzum marketplace shop. The bot collects user data, stores it in Google Sheets, handles customer questions, and allows admin to broadcast messages to all users.

## Features

- 🤖 **User Registration**: Automatically collects user data when they start the bot
- 📊 **Google Sheets Integration**: Stores all user data in Google Sheets for easy management
- 🛍️ **Shop Redirection**: Directs users to your Uzum marketplace shop
- ❓ **Q&A System**: Users can ask questions, admin receives notifications
- 📢 **Broadcast Messaging**: Admin can send messages to all users
- 📈 **Statistics**: Track user count and activity
- 🔧 **Admin Panel**: Special commands for bot administration

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- Google Cloud Project with Sheets API enabled
- Google Service Account credentials

## Quick Setup

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd uzum-shop-bot
python setup.py
```

### 2. Configure Environment

Edit the `.env` file with your configuration:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=your_google_sheet_id_here
UZUM_SHOP_URL=https://uzum.uz/ru/shop/ladium
ADMIN_USER_ID=your_telegram_user_id_here
```

### 3. Google Sheets Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API
4. Create a Service Account
5. Download the JSON credentials file
6. Rename it to `credentials.json` and place in project root
7. Create a Google Sheet and share it with the service account email
8. Copy the Sheet ID from the URL

### 4. Run the Bot

```bash
python bot.py
```

## Bot Commands

### User Commands
- `/start` - Start the bot and register
- `/help` - Show help information

### Admin Commands
- `/broadcast <message>` - Send message to all users
- `/stats` - Show bot statistics
- `/help` - Show admin help

## Deployment Options

### Option 1: Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

### Option 2: Systemd Service

```bash
# Generate service file
python systemd_service.py

# Install service
sudo cp uzum-shop-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable uzum-shop-bot
sudo systemctl start uzum-shop-bot

# Check status
sudo systemctl status uzum-shop-bot
```

### Option 3: Manual Server Deployment

1. Upload files to your server
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables
4. Run: `python bot.py`

## Project Structure

```
uzum-shop-bot/
├── bot.py                 # Main bot application
├── config.py             # Configuration settings
├── google_sheets.py      # Google Sheets integration
├── requirements.txt      # Python dependencies
├── setup.py             # Setup script
├── systemd_service.py   # Systemd service generator
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile          # Docker configuration
├── .env               # Environment variables (create from .env.example)
├── credentials.json   # Google Sheets credentials (add your own)
└── README.md         # This file
```

## Google Sheets Structure

The bot automatically creates the following columns in your Google Sheet:

| Column | Description |
|--------|-------------|
| ID | Auto-incrementing user ID |
| Username | Telegram username |
| First Name | User's first name |
| Last Name | User's last name |
| Telegram ID | User's Telegram ID |
| Phone | Phone number (if provided) |
| Registration Date | When user first used the bot |
| Last Activity | Last time user interacted with bot |

## Bot Flow

1. **User starts bot** → Data collected and stored in Google Sheets
2. **User clicks shop button** → Redirected to Uzum marketplace
3. **User asks question** → Question sent to admin, confirmation to user
4. **Admin broadcasts message** → Message sent to all registered users

## Security Features

- Environment variables for sensitive data
- Admin-only commands with user ID verification
- Error handling and logging
- Input validation and sanitization

## Monitoring and Logs

The bot includes comprehensive logging:
- User interactions
- Google Sheets operations
- Error tracking
- Admin actions

Logs are written to console and can be configured for file output.

## Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check if TELEGRAM_BOT_TOKEN is correct
   - Verify bot is not blocked by Telegram

2. **Google Sheets errors**
   - Ensure credentials.json is valid
   - Check if service account has access to the sheet
   - Verify GOOGLE_SHEET_ID is correct

3. **Permission errors**
   - Check file permissions for credentials.json
   - Ensure .env file is readable

### Getting Help

1. Check the logs for error messages
2. Verify all environment variables are set
3. Test Google Sheets API access separately
4. Ensure all dependencies are installed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the troubleshooting section

---

**Made with ❤️ for Uzum marketplace sellers**
