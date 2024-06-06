import json
import os
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
from token_1 import token

DATA_FILE = 'bot_data.json'

def load_bot_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        user_ids = set(data['user_ids'])
    else:
        start_date = datetime.now()
        user_ids = set()
        save_bot_data(start_date, user_ids)
    return start_date, user_ids

def save_bot_data(start_date, user_ids):
    data = {
        "start_date": start_date.strftime('%Y-%m-%d'),
        "user_ids": list(user_ids)
    }
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

def escape_markdown_v2(text):
    """Helper function to escape special characters for MarkdownV2."""
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user_ids.add(user_id)
    save_bot_data(start_date, user_ids)
    await update.message.reply_text(
        "Welcome! Use /flip to flip a coin, /dice to roll a dice, and /exp to expire your bets."
    )

async def flip(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_ids:
        await inline_start(update, context) 
        return
    user = update.effective_user
    result = random.choice(["heads", "tails"])
    user_link = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    message = f"『 {user_link} 』flipped a coin!\n\nIt's {result}!"
    if update.message.reply_to_message:
        original_msg_id = update.message.reply_to_message.message_id
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='HTML')
    else:
        await update.message.reply_text(message, parse_mode='HTML')


async def dice(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_ids:
        await inline_start(update, context)
        return
    if update.message.reply_to_message:
        user_dice_msg_id = update.message.reply_to_message.message_id
        await context.bot.send_dice(chat_id=update.effective_chat.id, reply_to_message_id=user_dice_msg_id)
    else:
        await context.bot.send_dice(chat_id=update.effective_chat.id)

async def expire(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_ids:
        await inline_start(update, context)
        return
    await update.message.reply_text("Your all bets are expired")

async def broadcast(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in user_ids:
        await inline_start(update, context)
        return
    message = ' '.join(context.args)
    if not message:
        await update.message.reply_text("Please provide a message to broadcast.")
        return
    for user_id in user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

async def inline_start(update: Update, context: CallbackContext) -> None:
    button = InlineKeyboardButton("Start Bot", url=f"https://t.me/{context.bot.username}?start=start")
    reply_markup = InlineKeyboardMarkup([[button]])
    await update.message.reply_text("Please start the bot by clicking the button below:", reply_markup=reply_markup)

def main():
    global start_date, user_ids
    start_date, user_ids = load_bot_data()

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("flip", flip))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("exp", expire))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CallbackQueryHandler(inline_start, pattern="start"))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
