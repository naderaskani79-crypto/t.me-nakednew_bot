import os
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_USERNAME = "@fucking_vazeyat"
ADMIN_ID = 5593404968

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

user_state = {}


async def is_member(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)

        return member.status in [
            "member",
            "administrator",
            "creator",
        ]
    except:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if await is_member(context.bot, user.id):

        user_state[user.id] = "WAIT_PHOTO"

        await update.message.reply_text(
            "✅ عضویت شما تایید شد.\n\nلطفاً عکس خود را ارسال کنید."
        )

    else:

        keyboard = [
            [
                InlineKeyboardButton(
                    "📢 عضویت در کانال",
                    url="https://t.me/fucking_vazeyat",
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ بررسی عضویت",
                    callback_data="check",
                )
            ],
        ]

        await update.message.reply_text(
            "برای استفاده از ربات ابتدا عضو کانال شوید.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user = query.from_user

    if await is_member(context.bot, user.id):

        user_state[user.id] = "WAIT_PHOTO"

        await query.message.reply_text(
            "✅ عضویت شما تایید شد.\n\nحالا عکس خود را ارسال کنید."
        )

    else:

        await query.message.reply_text(
            "❌ هنوز عضو کانال نشده‌اید."
        )


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if user_state.get(user.id) != "WAIT_PHOTO":

        await update.message.reply_text(
            "ابتدا /start را بزنید."
        )
        return

    photo = update.message.photo[-1].file_id

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=f"عکس جدید از:\n{user.full_name}\nID:{user.id}",
    )

    await update.message.reply_text(
        "✅ عکس شما با موفقیت ارسال شد."
      )
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_membership, pattern="check"))
    app.add_handler(MessageHandler(filters.PHOTO, photo))

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
