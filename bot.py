from pymongo import MongoClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# رابط الاتصال بـ MongoDB
client = MongoClient(
    "mongodb://abwb7293:1ybQhn38Gcx8KpDS@ac-k5pzowt-shard-00-00.7yjkzmr.mongodb.net:27017,"
    "ac-k5pzowt-shard-00-01.7yjkzmr.mongodb.net:27017,"
    "ac-k5pzowt-shard-00-02.7yjkzmr.mongodb.net:27017/"
    "?ssl=true&replicaSet=atlas-k5pzowt-shard-0&authSource=admin&retryWrites=true&w=majority"
)


db = client["quran_bot"]  # اسم قاعدة البيانات
students_collection = db["students"]  # اسم الكوليكشن

# التوكن الخاص بالبوت من BotFather
TOKEN = "YOUR_BOT_TOKEN_HERE"  # ← استبدله بالتوكن الحقيقي

# إضافة نقاط لطالب
def add_points(student_id, points):
    student = students_collection.find_one({"id": student_id})
    if student:
        students_collection.update_one({"id": student_id}, {"$inc": {"points": points}})
    else:
        students_collection.insert_one({"id": student_id, "points": points})

# جلب نقاط طالب
def get_points(student_id):
    student = students_collection.find_one({"id": student_id})
    return student["points"] if student else None

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحباً بك! أرسل رقم الطالب وعدد النقاط مثل: 1234 10\nأو استخدم /check 1234 لعرض النقاط.")

# التعامل مع الرسائل العادية
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

# أمر /check
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

# تشغيل البوت
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ البوت يعسمل الآن ...")
    app.run_polling()
