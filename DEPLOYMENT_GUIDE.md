# 🚀 Deployment Guide - Uzum Shop Bot to Railway

## Step 1: Push to GitHub

### 1.1 Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: Uzum Shop Telegram Bot MVP"
```

### 1.2 Create GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Click "New repository"
3. Name it: `uzum-shop-bot`
4. Make it **Private** (recommended for security)
5. Don't initialize with README (we already have files)
6. Click "Create repository"

### 1.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/uzum-shop-bot.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Railway

### 2.1 Create Railway Account
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub account
3. Connect your GitHub account

### 2.2 Deploy from GitHub
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `uzum-shop-bot` repository
4. Click "Deploy Now"

### 2.3 Configure Environment Variables
In Railway dashboard, go to your project → Variables tab and add:

```
TELEGRAM_BOT_TOKEN=8265430634:AAGnsbhJamJYQy9D_2t0MATqNRMVkpiV8rc
ADMIN_USER_ID=6297482101
UZUM_SHOP_URL=https://uzum.uz/ru/shop/ladium
```

### 2.4 Deploy
1. Click "Deploy" button
2. Wait for deployment to complete
3. Your bot will be running 24/7!

## Step 3: Test Production Bot

1. **Find your bot** on Telegram
2. **Send** `/start`
3. **Click** shop button
4. **Check logs** in Railway dashboard

## Step 4: Monitor Your Bot

### Railway Dashboard Features:
- ✅ **Real-time logs** - See user activity
- ✅ **Metrics** - CPU, memory usage
- ✅ **Restart** - If bot crashes, auto-restarts
- ✅ **Environment variables** - Easy configuration
- ✅ **Custom domain** - Optional

### Logs You'll See:
```
🆕 NEW USER REGISTERED: John Doe (@john_doe) - ID: 123456789
🛍️ USER REDIRECTED TO SHOP: john_doe - Total users: 5
```

## Step 5: Update Bot (Optional)

To update your bot:
1. **Edit files** locally
2. **Commit changes**:
   ```bash
   git add .
   git commit -m "Update bot features"
   git push
   ```
3. **Railway auto-deploys** the changes!

## Troubleshooting

### Bot Not Responding?
1. Check Railway logs
2. Verify environment variables
3. Check bot token is correct

### Deployment Failed?
1. Check `requirements.txt` has all dependencies
2. Verify Python version in `runtime.txt`
3. Check Railway logs for errors

## Cost
- **Railway Free Tier**: $5 credit monthly
- **Your bot**: Very lightweight, should stay free
- **Upgrade**: Only if you get many users

---

**Your bot will run 24/7 on Railway! 🎉**
