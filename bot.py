import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "7908716419:AAGpFWjBLRDMDQtzOH-oa2vmB2DBQhFziBo"
DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({"students": []}, f)
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_points(student_id, points):
    db = load_db()
    student = next((s for s in db["students"] if s["id"] == student_id), None)
    if student:
        student["points"] += points
    else:
        db["students"].append({"id": student_id, "points": points})
    save_db(db)

def get_points(student_id):
    db = load_db()
    student = next((s for s in db["students"] if s["id"] == student_id), None)
    return student["points"] if student else None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحباً بك! أرسل رقم الطالب ومسافة وعدد النقاط مثل: 1234 10\nأو استخدم /check 1234 لعرض النقاط.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    parts = text.split()
    if len(parts) == 2 and parts[1].isdigit():
        student_id = parts[0]
        points = int(parts[1])
        add_points(student_id, points)
        await update.message.reply_text(f"✅ تمت إضافة {points} نقطة للطالب رقم {student_id}.")
    else:
        await update.message.reply_text("❌ الرجاء إرسال البيانات بالصيغة: رقم_الطالب عدد_النقاط\nمثال: 1234 10")

async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❌ استخدم الأمر هكذا: /check 1234")
        return

    student_id = context.args[0]
    points = get_points(student_id)
    if points is not None:
        await update.message.reply_text(f"📌 الطالب رقم {student_id} لديه {points} نقطة.")
    else:
        await update.message.reply_text("❌ الطالب غير موجود.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ البوت يعمل الآن ...")
    app.run_polling()

if __name__ == "__main__":
    main()
