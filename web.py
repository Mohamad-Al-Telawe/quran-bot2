from flask import Flask, render_template
import json, os
from threading import Thread
from bot import main as run_bot  # نفترض أن ملف bot.py فيه دالة main()

app = Flask(__name__)
DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"students": []}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

@app.route("/")
def index():
    db = load_db()
    students = sorted(db["students"], key=lambda x: x["points"], reverse=True)
    return render_template("index.html", students=students)

if __name__ == "__main__":
    Thread(target=run_bot).start()  # تشغيل البوت في Thread موازٍ
    app.run(host="0.0.0.0", port=3000)
