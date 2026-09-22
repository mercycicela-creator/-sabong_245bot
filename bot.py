import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# --- Bot Functions ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message with a persistent menu."""
    user = update.effective_user
    
    # Persistent Menu Button (Reply Keyboard)
    keyboard = [
        [InlineKeyboardButton("📢 Updates", callback_data='updates')],
        [InlineKeyboardButton("🛠 Tools", callback_data='tools')],
        [InlineKeyboardButton("ℹ️ About", callback_data='about')],
        [InlineKeyboardButton("🆘 Help", callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Hi {user.mention_html()}! 👋\n\n"
        "I'm **@sabong_245bot**, your quick access bot for info, updates, and features.\n\n"
        "Use the buttons below to navigate.",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles button clicks."""
    query = update.callback_query
    await query.answer()

    if query.data == 'updates':
        await query.edit_message_text(text="📢 **Latest Updates**\n\n- Bot is live on Railway!\n- New tools coming soon.\n- Stay tuned.")
    elif query.data == 'tools':
        await query.edit_message_text(text="🛠 **Available Tools**\n\n- /ping - Check bot status\n- /info - Get your Telegram ID\n- More features coming soon.")
    elif query.data == 'about':
        await query.edit_message_text(text="ℹ️ **About**\n\n@sabong_245bot provides quick access to useful information and Telegram features in one place.")
    elif query.data == 'help':
        await query.edit_message_text(text="🆘 **Help**\n\nCommands:\n/start - Show main menu\n/ping - Check bot status\n/info - Get your user ID\n\nUse the menu buttons to navigate.")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Simple ping command to check if bot is alive."""
    await update.message.reply_text("🏓 Pong! I'm active and responding.")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provides user info."""
    user = update.effective_user
    await update.message.reply_text(
        f"👤 **Your Info**\n\n"
        f"Name: {user.full_name}\n"
        f"ID: `{user.id}`\n"
        f"Username: @{user.username}" if user.username else f"👤 **Your Info**\n\nName: {user.full_name}\nID: `{user.id}`",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a help message."""
    await update.message.reply_text(
        "🆘 **Help**\n\n"
        "I provide quick access to information and features.\n\n"
        "**Commands:**\n"
        "/start - Show main menu\n"
        "/ping - Check status\n"
        "/info - Get your user ID\n"
        "/help - Show this message"
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors."""
    logger.error("Exception while handling an update:", exc_info=context.error)

# --- Main Application ---

def main() -> None:
    """Start the bot."""
    # Get token from environment variable
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN is not set!")
        return

    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # Register Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("help", help_command))
    
    # Register Callback Query Handler for buttons
    application.add_handler(CallbackQueryHandler(button_click))
    
    # Register Error Handler
    application.add_error_handler(error_handler)

    # Run the bot with long polling
    logger.info("Starting @sabong_245bot with long polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
