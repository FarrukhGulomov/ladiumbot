#!/usr/bin/env python3
"""
Quick Start Script for Uzum Shop Telegram Bot
This script helps you get the bot running quickly with minimal setup.
"""

import os
import sys
import json
import subprocess

def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print("🛍️  UZUM SHOP TELEGRAM BOT - QUICK START")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies!")
        return False

def create_env_file():
    """Create .env file with user input"""
    print("\n🔧 Setting up configuration...")
    
    # Check if .env already exists
    if os.path.exists('.env'):
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/N): ").lower()
        if overwrite != 'y':
            print("✅ Using existing .env file")
            return True
    
    # Get configuration from user
    print("\nPlease provide the following information:")
    
    bot_token = input("🤖 Telegram Bot Token (from @BotFather): ").strip()
    if not bot_token:
        print("❌ Bot token is required!")
        return False
    
    sheet_id = input("📊 Google Sheet ID (from sheet URL): ").strip()
    if not sheet_id:
        print("❌ Google Sheet ID is required!")
        return False
    
    admin_id = input("👤 Your Telegram User ID (from @userinfobot): ").strip()
    if not admin_id:
        print("❌ Admin User ID is required!")
        return False
    
    shop_url = input("🛍️  Uzum Shop URL (default: https://uzum.uz/ru/shop/ladium): ").strip()
    if not shop_url:
        shop_url = "https://uzum.uz/ru/shop/ladium"
    
    # Create .env file
    env_content = f"""# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN={bot_token}

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID={sheet_id}

# Shop Configuration
UZUM_SHOP_URL={shop_url}

# Admin Configuration
ADMIN_USER_ID={admin_id}
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Configuration saved to .env file")
    return True

def setup_google_credentials():
    """Guide user through Google credentials setup"""
    print("\n🔑 Google Sheets Setup:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Enable Google Sheets API")
    print("4. Create a Service Account")
    print("5. Download the JSON credentials file")
    print("6. Rename it to 'credentials.json' and place in this directory")
    print("7. Share your Google Sheet with the service account email")
    
    input("\nPress Enter when you have completed the Google Sheets setup...")
    
    if os.path.exists('credentials.json'):
        print("✅ credentials.json found!")
        return True
    else:
        print("⚠️  credentials.json not found. Please add it before running the bot.")
        return False

def test_configuration():
    """Test if configuration is working"""
    print("\n🧪 Testing configuration...")
    
    try:
        from config import TELEGRAM_BOT_TOKEN, GOOGLE_SHEET_ID, ADMIN_USER_ID
        from google_sheets import GoogleSheetsManager
        
        if not TELEGRAM_BOT_TOKEN:
            print("❌ Telegram Bot Token not found in .env")
            return False
        
        if not GOOGLE_SHEET_ID:
            print("❌ Google Sheet ID not found in .env")
            return False
        
        if not ADMIN_USER_ID:
            print("❌ Admin User ID not found in .env")
            return False
        
        print("✅ Configuration loaded successfully!")
        
        # Test Google Sheets connection
        try:
            gs = GoogleSheetsManager()
            print("✅ Google Sheets connection successful!")
        except Exception as e:
            print(f"❌ Google Sheets connection failed: {e}")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_bot():
    """Run the bot"""
    print("\n🚀 Starting the bot...")
    print("Press Ctrl+C to stop the bot")
    print("-" * 40)
    
    try:
        import bot
        bot.main()
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error running bot: {e}")

def main():
    """Main function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create .env file
    if not create_env_file():
        return
    
    # Setup Google credentials
    if not setup_google_credentials():
        print("⚠️  Please complete Google Sheets setup and run the script again")
        return
    
    # Test configuration
    if not test_configuration():
        print("❌ Configuration test failed. Please check your setup.")
        return
    
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nYour bot is ready to run!")
    print("\nNext steps:")
    print("1. Test the bot by messaging it on Telegram")
    print("2. Check your Google Sheet for user data")
    print("3. Use /broadcast command to send messages to users")
    print("\nTo run the bot manually: python bot.py")
    
    run_now = input("\n🚀 Run the bot now? (Y/n): ").lower()
    if run_now != 'n':
        run_bot()

if __name__ == '__main__':
    main()
