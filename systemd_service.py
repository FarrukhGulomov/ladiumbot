#!/usr/bin/env python3
"""
Systemd service configuration generator for Uzum Shop Telegram Bot
"""

import os
import getpass

def generate_systemd_service():
    """Generate systemd service file"""
    current_user = getpass.getuser()
    current_dir = os.getcwd()
    python_path = os.path.join(current_dir, 'venv', 'bin', 'python')
    
    service_content = f"""[Unit]
Description=Uzum Shop Telegram Bot
After=network.target

[Service]
Type=simple
User={current_user}
WorkingDirectory={current_dir}
Environment=PATH={current_dir}/venv/bin
ExecStart={python_path} {current_dir}/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    with open('uzum-shop-bot.service', 'w', encoding='utf-8') as f:
        f.write(service_content)
    
    print("✅ Generated uzum-shop-bot.service file")
    print(f"📁 Service file location: {os.path.join(current_dir, 'uzum-shop-bot.service')}")
    print("\n📋 To install the service:")
    print("1. sudo cp uzum-shop-bot.service /etc/systemd/system/")
    print("2. sudo systemctl daemon-reload")
    print("3. sudo systemctl enable uzum-shop-bot")
    print("4. sudo systemctl start uzum-shop-bot")
    print("5. sudo systemctl status uzum-shop-bot")

if __name__ == '__main__':
    generate_systemd_service()
