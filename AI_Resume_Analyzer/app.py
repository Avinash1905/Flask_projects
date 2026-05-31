from flask import Flask,render_template,request,redirect,session
from PyPDF2 import PdfReader
import mysql.connector
import requests
from werkzeug.security import (
generate_password_hash,
check_password_hash,
)
from werkzeug.utils import secure_filename
import uuid
db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="avinash@1419",
    database="new"
)
cursor=db.cursor()
app=Flask(__name__)
OPENROUTER_API_KEY = "api"
app.secret_key="mawa"
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/register")
def register_page():
    return render_template("register.html")
@app.route('/register',methods=["POST"])
def register_form():
    name=request.form.get("name")
    email=request.form.get("email")
    password=request.form.get("password")
    sql="select * from users where email=%s"
    values=(email,)
    cursor.execute(sql,values)
    a=cursor.fetchone()
    if a:
        return redirect("/register")
    else:
        h_password=generate_password_hash(password)
        sql="insert into users(name,email,password) values(%s,%s,%s)"
        values=(name,email,h_password)
        cursor.execute(sql,values)
        db.commit()
        return redirect("/login")
def analyze_resume(resume_text):

    prompt = f"""
    Analyze this resume.

    Return ONLY in this format:

    ATS_SCORE: <score>

    SUMMARY:
    <summary>

    SKILLS:
    <skills>

    WEAKNESSES:
    <weaknesses>

    SUGGESTIONS:
    <suggestions>

    Resume:


    {resume_text}

    Give:

    1. Professional Summary
    2. Technical Skills
    3. Strengths
    4. Weaknesses
    5. Suggestions
    """

    response = requests.post(

        "https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },

        json={
            "model": "openai/gpt-4o-mini",

            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    data = response.json()

    print(data)

    if "choices" not in data:

        return {
            "score": "N/A",
            "summary": str(data),
            "skills": "",
            "weaknesses": "",
            "suggestions": ""
        }

    analysis = data["choices"][0]["message"]["content"]

    print(analysis)

    score = ""
    summary = ""
    skills = ""
    weaknesses = ""
    suggestions = ""

    lines = analysis.split("\n")

    current = None

    for line in lines:

        line = line.strip()

        if line.startswith("ATS_SCORE"):
            current = "score"
            score = line.replace("ATS_SCORE:", "").strip()

        elif line.startswith("SUMMARY"):
            current = "summary"
            summary = line.replace("SUMMARY:", "").strip()

        elif line.startswith("SKILLS"):
            current = "skills"
            skills = line.replace("SKILLS:", "").strip()

        elif line.startswith("WEAKNESSES"):
            current = "weaknesses"
            weaknesses = line.replace("WEAKNESSES:", "").strip()

        elif line.startswith("SUGGESTIONS"):
            current = "suggestions"
            suggestions = line.replace("SUGGESTIONS:", "").strip()

        else:

            if current == "summary":
                summary += " " + line

            elif current == "skills":
                skills += " " + line

            elif current == "weaknesses":
                weaknesses += " " + line

            elif current == "suggestions":
                suggestions += " " + line

    return {
        "score": score,
        "summary": summary,
        "skills": skills,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }
@app.route("/login")
def login_page():
    return render_template("login.html")
@app.route("/login",methods=["POST"])
def login():
    email=request.form.get("email")
    password=request.form.get("password")
    sql="select * from users where email=%s"
    values=(email,)
    cursor.execute(sql,values)
    a=cursor.fetchone()
    if a:
        db_password=a[3]
        if check_password_hash(db_password,password):
            session["user"]=email
            return redirect("/dashboard")
        else:
            return redirect("/login")
    else:
        return redirect("/register")
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    else:
        return render_template("dashboard.html")
@app.route("/upload-resume")
def upload():
    return render_template("upload_resume.html")
@app.route("/analyze", methods=["POST"])
def read():

    if "user" not in session:

        return redirect("/login")

    resume = request.files["resume"]

    filename = (
        str(uuid.uuid4())
        + "_"
        + secure_filename(resume.filename)
    )

    path = "uploads/" + filename

    resume.save(path)

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text

    resume_text = text

    # AI ANALYSIS
    analysis = analyze_resume(resume_text)

    # SAVE TO DB
    email = session["user"]

    sql = "select * from users where email=%s"

    cursor.execute(sql, (email,))

    user = cursor.fetchone()

    user_id = user[0]

    sql = """
    insert into resumes(user_id, filename)
    values(%s,%s)
    """

    values = (
        user_id,
        filename
    )

    cursor.execute(sql, values)

    db.commit()

    result = analyze_resume(resume_text)
    sql = """
    insert into analysis_history
    (
        user_email,
        score,
        analysis
    )

    values(%s,%s,%s)
    """
    full_analysis = f"""

    SUMMARY:
    {result['summary']}

    SKILLS:
    {result['skills']}

    WEAKNESSES:
    {result['weaknesses']}

    SUGGESTIONS:
    {result['suggestions']}
    """

    values = (
        session["user"],
        result["score"],
        full_analysis
    )
    return render_template(
        "result.html",
        score=result["score"],
        summary=result["summary"],
        skills=result["skills"],
        weaknesses=result["weaknesses"],
        suggestions=result["suggestions"]
    )
@app.route("/history")
def history():

    if "user" not in session:

        return redirect("/login")

    email = session["user"]

    sql = """
    select * from users
    where email=%s
    """

    cursor.execute(sql,(email,))

    user = cursor.fetchone()

    user_id = user[0]

    sql = """
    select * from resumes
    where user_id=%s
    order by upload_date desc
    """

    cursor.execute(sql,(user_id,))

    resumes = cursor.fetchall()

    return render_template(
        "history.html",
        resumes=resumes
    )

@app.route("/logout")
def logout():
    session.pop("user")
    return redirect("/login")
if __name__=="__main__":
    app.run(debug=True)