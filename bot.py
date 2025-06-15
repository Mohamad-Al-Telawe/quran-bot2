from pymongo import MongoClient

# بيانات الاتصال من MongoDB Atlas
MONGO_URI = "mongodb+srv://abwb7293:1ybQhn38Gcx8KpDS@cluster0.7yjkzmr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# الاتصال بقاعدة البيانات
client = MongoClient(MONGO_URI)

# تحديد القاعدة والمجموعة
db = client["quran_bot"]
students_collection = db["students"]

# إضافة طالب وهمي
test_student = {
    "id": "9999",
    "points": 100
}

# إدخال الطالب
result = students_collection.insert_one(test_student)
print("✅ تم إدخال الطالب بنجاح، ID:", result.inserted_id)
