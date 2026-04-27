# PUBG Chest Bot

Bu Telegram bot PUBG mashhur o'yinchilarining chestlarini ochish uchun.

## O'rnatish

1. Python 3.7+ o'rnating.
2. Kutubxonalarni o'rnating: `pip install -r requirements.txt`
3. `config.py` da BOT_TOKEN, ADMIN_ID, CHANNEL_ID ni o'zgartiring.
4. Botni ishga tushiring: `python main.py`

## Ishlash tartibi

- /start bosilganda, kanalga obuna tekshiriladi.
- Agar obuna bo'lmagan bo'lsa, obuna bo'lish uchun havola beriladi.
- Obuna bo'lgach, o'yinchilar ro'yxati ko'rsatiladi.
- O'yinchi tanlanganda, rasm, ism va tasodifiy chest ko'rsatiladi.
- Keyin boshiga qaytiladi.

## Admin panel

- /add_player <ism> <rasm_url> - O'yinchi qo'shish.
- /list_players - O'yinchilarni ko'rish.

Bot tokenini @BotFather dan oling.

## Render'da joylash

1. GitHub'da yangi repository yarating.
2. Bu fayllarni repository'ga yuklang.
3. Render.com ga kiring va "New +" > "Web Service" ni tanlang.
4. GitHub repository'ni ulang.
5. Build & Deploy:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
6. Environment Variables qo'shing:
   - BOT_TOKEN: Sizning bot tokeningiz
   - ADMIN_ID: Admin ID
   - CHANNEL_ID: Kanal username (masalan, @abe_ako)
7. Deploy qiling.

Bot Render'da 24/7 ishlaydi.