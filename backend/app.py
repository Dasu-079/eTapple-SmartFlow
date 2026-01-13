from flask import Flask, request, render_template
import os
from ocr import get_text
from db import connect, create_table

app = Flask(__name__)
create_table()

UPLOAD = "uploads"
os.makedirs(UPLOAD, exist_ok=True)

@app.route("/")
def home():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    keywords = request.form.get("keywords", "")
    category = request.form.get("category")

    path = os.path.join(UPLOAD, file.filename)
    file.save(path)

    text = get_text(path).lower()
    key_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]

    found, missing = [], []
    for k in key_list:
        if k in text:
            found.append(k)
        else:
            missing.append(k)

    status = "Success" if len(missing) == 0 else "Failed"

    con = connect()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO tappal(filename,text,category,status) VALUES(?,?,?,?)",
        (file.filename, text, category, status)
    )
    con.commit()
    con.close()

    return render_template(
        "result.html",
        file=file.filename,
        category=category,
        found=found,
        missing=missing,
        status=status
    )

@app.route("/dashboard")
def dashboard():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM tappal")
    data = cur.fetchall()
    con.close()
    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
