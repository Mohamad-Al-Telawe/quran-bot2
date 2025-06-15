from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ضع التوكن مباشرة كسلسلة نصية
TOKEN = "7908716419:AAGpFWjBLRDMDQtzOH-oa2vmB2DBQhFziBo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك في بوت البايثون!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("✅ البوت يعمل الآن ...")
    app.run_polling()
