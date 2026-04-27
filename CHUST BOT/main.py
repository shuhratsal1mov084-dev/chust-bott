import random
import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, ADMIN_ID, CHANNEL_ID, players, chest_items

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CommandHandler("add_player", add_player))
    application.add_handler(CommandHandler("list_players", list_players))

    application.run_polling()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id

    # Check subscription
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            # Subscribed, show players
            await show_players(update, context)
        else:
            # Not subscribed
            keyboard = [[InlineKeyboardButton("Kanalga obuna bo'lish", url=f"https://t.me/{CHANNEL_ID[1:]}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Botdan foydalanish uchun kanalga obuna bo'ling va qayta /start bosing.",
                reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"Subscription check failed: {e}")
        await update.message.reply_text("Xatolik yuz berdi. Qayta urinib ko'ring.")

async def show_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not players:
        await update.message.reply_text("Hozircha o'yinchilar yo'q.")
        return

    keyboard = []
    for player in players:
        keyboard.append([InlineKeyboardButton(player['name'], callback_data=f"player_{players.index(player)}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("O'yinchilardan birini tanlang:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("player_"):
        index = int(data.split("_")[1])
        if 0 <= index < len(players):
            player = players[index]
            item = random.choice(chest_items)
            text = f"O'yinchi: {player['name']}\nChesti: {item}"
            if player['image']:
                await query.edit_message_text(text=text)
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=player['image'], caption=text)
            else:
                await query.edit_message_text(text=text)
            # Back to start
            await show_players(update, context)

async def add_player(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Siz admin emassiz.")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Foydalanish: /add_player <ism> <rasm_url>")
        return

    name = args[0]
    image = args[1]
    players.append({'name': name, 'image': image})
    await update.message.reply_text(f"O'yinchi {name} qo'shildi.")

async def list_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Siz admin emassiz.")
        return

    if not players:
        await update.message.reply_text("O'yinchilar yo'q.")
        return

    text = "O'yinchilar:\n" + "\n".join([f"{i+1}. {p['name']}" for i, p in enumerate(players)])
    await update.message.reply_text(text)

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(host='0.0.0.0', port=10000)