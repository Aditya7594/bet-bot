import random
from telegram import Update
from telegram.ext import  CallbackContext

# Assuming user_ids is imported from main.py
from main import user_ids, save_user_ids

async def flip(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    result = random.choice(["heads", "tails"])
    message = f"『 {user.first_name} 』flipped a coin!\n\nIt's {result}!"
    await update.message.reply_text(message)

async def dice(update: Update, context: CallbackContext) -> None:
    await context.bot.send_dice(chat_id=update.effective_chat.id)

async def expire(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Your all bets are expired")

async def broadcast(update: Update, context: CallbackContext) -> None:
    # Extract the broadcast message from the command
    message = ' '.join(context.args)
    if not message:
        await update.message.reply_text("Please provide a message to broadcast.")
        return
    
    # Send the message to all stored user IDs
    for user_id in user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")
