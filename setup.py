#!/usr/bin/env python3
"""
Setup script for Uzum Shop Telegram Bot
"""

import os
import sys
import subprocess
import json

def create_env_file():
    """Create .env file from template"""
    env_content = """# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=your_google_sheet_id_here

# Shop Configuration
UZUM_SHOP_URL=https://uzum.uz/ru/shop/ladium

# Admin Configuration
ADMIN_USER_ID=your_telegram_user_id_here
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Created .env file. Please fill in your configuration.")
    else:
        print("⚠️  .env file already exists.")

def install_dependencies():
    """Install required dependencies"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def create_google_sheets_template():
    """Create template for Google Sheets setup"""
    template = {
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n",
        "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
    }
    
    if not os.path.exists('credentials_template.json'):
        with open('credentials_template.json', 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2)
        print("✅ Created credentials_template.json. Please replace with your actual Google Sheets credentials.")
    else:
        print("⚠️  credentials_template.json already exists.")

def main():
    """Main setup function"""
    print("🚀 Setting up Uzum Shop Telegram Bot...")
    print("=" * 50)
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed. Please check the error messages above.")
        return
    
    # Create Google Sheets template
    create_google_sheets_template()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed!")
    print("\n📋 Next steps:")
    print("1. Get your Telegram bot token from @BotFather")
    print("2. Set up Google Sheets API credentials")
    print("3. Fill in the .env file with your configuration")
    print("4. Rename credentials_template.json to credentials.json and add your credentials")
    print("5. Run: python bot.py")
    print("\n📖 For detailed instructions, see README.md")

if __name__ == '__main__':
    main()
