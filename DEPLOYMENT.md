# Deployment Guide - Uzum Shop Telegram Bot

This guide provides detailed instructions for deploying the Uzum Shop Telegram Bot to a production server.

## Server Requirements

### Minimum Requirements
- **OS**: Ubuntu 20.04+ or CentOS 8+
- **RAM**: 512MB minimum, 1GB recommended
- **Storage**: 2GB free space
- **Python**: 3.8 or higher
- **Internet**: Stable connection for Telegram API

### Recommended VPS Providers
- DigitalOcean (Droplet)
- Linode
- Vultr
- AWS EC2
- Google Cloud Platform

## Pre-Deployment Setup

### 1. Create Telegram Bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Choose a name for your bot
4. Choose a username (must end with 'bot')
5. Copy the bot token

### 2. Get Your Telegram User ID

1. Message [@userinfobot](https://t.me/userinfobot)
2. Copy your user ID (you'll need this for admin access)

### 3. Setup Google Sheets

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Sheets API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"
4. Create Service Account:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in details and create
5. Generate Key:
   - Click on the service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose JSON format and download
6. Create Google Sheet:
   - Go to [Google Sheets](https://sheets.google.com)
   - Create a new sheet
   - Share it with the service account email (from the JSON file)
   - Copy the Sheet ID from the URL

## Deployment Methods

### Method 1: Docker Deployment (Recommended)

#### Step 1: Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again to apply docker group changes
```

#### Step 2: Deploy Application

```bash
# Clone repository
git clone <your-repo-url>
cd uzum-shop-bot

# Create environment file
cp .env.example .env
nano .env  # Edit with your configuration

# Add Google credentials
# Upload your credentials.json file to the project directory

# Start the application
docker-compose up -d

# Check logs
docker-compose logs -f
```

#### Step 3: Setup Auto-restart

```bash
# Create systemd service for Docker Compose
sudo nano /etc/systemd/system/uzum-bot.service
```

Add this content:

```ini
[Unit]
Description=Uzum Shop Bot
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/uzum-shop-bot
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable the service:

```bash
sudo systemctl enable uzum-bot.service
sudo systemctl start uzum-bot.service
```

### Method 2: Direct Python Deployment

#### Step 1: Setup Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Create application directory
sudo mkdir -p /opt/uzum-bot
sudo chown $USER:$USER /opt/uzum-bot
cd /opt/uzum-bot
```

#### Step 2: Deploy Application

```bash
# Clone repository
git clone <your-repo-url> .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup configuration
cp .env.example .env
nano .env  # Edit with your configuration

# Add Google credentials
# Upload your credentials.json file
```

#### Step 3: Create Systemd Service

```bash
sudo nano /etc/systemd/system/uzum-bot.service
```

Add this content:

```ini
[Unit]
Description=Uzum Shop Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/uzum-bot
Environment=PATH=/opt/uzum-bot/venv/bin
ExecStart=/opt/uzum-bot/venv/bin/python /opt/uzum-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable uzum-bot
sudo systemctl start uzum-bot
sudo systemctl status uzum-bot
```

## Configuration

### Environment Variables

Create `.env` file with these variables:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms

# Shop Configuration
UZUM_SHOP_URL=https://uzum.uz/ru/shop/ladium

# Admin Configuration
ADMIN_USER_ID=123456789
```

### Google Sheets Credentials

1. Upload your `credentials.json` file to the project directory
2. Ensure the service account has access to your Google Sheet
3. The sheet will be automatically created with proper headers

## Monitoring and Maintenance

### View Logs

```bash
# Docker deployment
docker-compose logs -f

# Systemd service
sudo journalctl -u uzum-bot -f

# Manual deployment
tail -f /var/log/uzum-bot.log
```

### Restart Service

```bash
# Docker deployment
docker-compose restart

# Systemd service
sudo systemctl restart uzum-bot
```

### Update Application

```bash
# Pull latest changes
git pull origin main

# Restart service
sudo systemctl restart uzum-bot
# or
docker-compose restart
```

## Security Considerations

### Firewall Setup

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### File Permissions

```bash
# Secure credentials file
chmod 600 credentials.json
chmod 600 .env

# Secure application directory
chmod 755 /opt/uzum-bot
```

### SSL/TLS (Optional)

If you plan to add a web interface:

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com
```

## Backup Strategy

### Automated Backup Script

Create `/opt/uzum-bot/backup.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups/uzum-bot"
mkdir -p $BACKUP_DIR

# Backup application files
tar -czf $BACKUP_DIR/uzum-bot_$DATE.tar.gz /opt/uzum-bot

# Keep only last 7 days of backups
find $BACKUP_DIR -name "uzum-bot_*.tar.gz" -mtime +7 -delete
```

Add to crontab:

```bash
crontab -e
# Add this line for daily backups at 2 AM
0 2 * * * /opt/uzum-bot/backup.sh
```

## Troubleshooting

### Common Issues

1. **Bot not responding**
   ```bash
   # Check if service is running
   sudo systemctl status uzum-bot
   
   # Check logs
   sudo journalctl -u uzum-bot -n 50
   ```

2. **Google Sheets errors**
   ```bash
   # Verify credentials file
   cat credentials.json | jq .
   
   # Test Google Sheets API
   python3 -c "from google_sheets import GoogleSheetsManager; gs = GoogleSheetsManager(); print('OK')"
   ```

3. **Permission errors**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER /opt/uzum-bot
   chmod 600 credentials.json .env
   ```

### Performance Monitoring

```bash
# Monitor resource usage
htop

# Monitor disk space
df -h

# Monitor network connections
netstat -tulpn | grep python
```

## Scaling Considerations

### For High Traffic

1. **Use Redis for session storage**
2. **Implement rate limiting**
3. **Add load balancing for multiple bot instances**
4. **Use database instead of Google Sheets for large user bases**

### Database Migration

For production with many users, consider migrating from Google Sheets to a proper database:

```python
# Example with PostgreSQL
import psycopg2
from psycopg2.extras import RealDictCursor

class DatabaseManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="uzum_bot",
            user="bot_user",
            password="secure_password"
        )
```

## Support and Maintenance

### Regular Maintenance Tasks

1. **Weekly**: Check logs for errors
2. **Monthly**: Update dependencies
3. **Quarterly**: Review and rotate credentials
4. **As needed**: Backup and restore procedures

### Monitoring Alerts

Set up monitoring for:
- Service status
- Memory usage
- Disk space
- Error rates
- Response times

---

**Deployment completed successfully! Your Uzum Shop Telegram Bot is now running in production.**
