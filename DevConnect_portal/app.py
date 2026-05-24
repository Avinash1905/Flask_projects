from flask import Flask,render_template,request,redirect,flash,session,jsonify
import mysql.connector
import requests

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "mawa"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="avinash@1419",
    database="new"
)

cursor = db.cursor()

# HOME
@app.route("/")
def home():

    return render_template("index.html")


# REGISTER PAGE
@app.route("/register",methods=["GET"])
def registration():

    return render_template("register.html")


# REGISTER SUBMIT
@app.route("/register",methods=["POST"])
def registration_submit():

    image = request.files["profile_image"]

    name = request.form["name"]

    email = request.form["email"]

    skill = request.form["skill"]

    experience = request.form["experience"]

    password = request.form["password"]

    # VALIDATION
    if (
        name == "" or
        email == "" or
        skill == "" or
        experience == "" or
        password == "" or
        image.filename == ""
    ):

        flash("All fields are required")

        return redirect("/register")

    # CHECK EXISTING USER
    check_sql = """
    select * from developers
    where email=%s
    """

    cursor.execute(check_sql,(email,))

    a = cursor.fetchone()

    if a:

        flash("User already exists")

        return redirect("/register")

    # HASH PASSWORD
    hashed_password = generate_password_hash(password)

    # SECURE IMAGE NAME
    filename = secure_filename(image.filename)

    # SAVE IMAGE
    image.save("static/uploads/" + filename)

    # INSERT USER
    sql = """
    insert into developers
    (
        name,
        email,
        skill,
        experience,
        password,
        profile_image
    )

    values(%s,%s,%s,%s,%s,%s)
    """

    values = (
        name,
        email,
        skill,
        experience,
        hashed_password,
        filename
    )

    cursor.execute(sql,values)

    db.commit()

    flash("User Added Successfully")

    return redirect("/login")


# LOGIN PAGE
@app.route("/login")
def login():

    return render_template("login.html")


# LOGIN SUBMIT
@app.route("/login",methods=["POST"])
def login1():

    email = request.form["email"]

    password = request.form["password"]

    check_user = """
    select * from developers
    where email=%s
    """

    cursor.execute(check_user,(email,))

    user = cursor.fetchone()

    if user:

        db_password = user[5]

        if check_password_hash(
            db_password,
            password
        ):

            session["user"] = email

            flash("Login Successful")

            return redirect("/dashboard")

        else:

            flash("Wrong Password")

            return redirect("/login")

    else:

        flash("User Not Found")

        return redirect("/login")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user" in session:

        return render_template(
            "dashboard.html",
            user=session["user"]
        )

    else:

        return redirect("/login")


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("user",None)

    flash("Logged Out")

    return redirect("/")


# ALL DEVELOPERS
@app.route("/developers")
def list():

    if "user" in session:

        sql = "select * from developers"

        cursor.execute(sql)

        developers = cursor.fetchall()

        return render_template(
            "developers.html",
            developers=developers
        )

    else:

        return redirect("/login")

@app.route("/ai-chat")
def ai_chat():

    if "user" not in session:

        return redirect("/login")

    return render_template("ai_chat.html")
# INDIVIDUAL PROFILE
@app.route("/developer/<int:id>")
def developer_profile(id):

    sql = """
    select * from developers
    where id=%s
    """

    cursor.execute(sql,(id,))

    dev = cursor.fetchone()

    return render_template(
        "developer_profile.html",
        dev=dev
    )


# UPDATE PAGE
@app.route("/update")
def update_page():

    if "user" not in session:

        return redirect("/login")

    return render_template("update.html")


# UPDATE SUBMIT
@app.route("/update",methods=["POST"])
def update():

    id = request.form["id"]

    skill = request.form["skill"]

    sql = """
    update developers
    set skill=%s
    where id=%s
    """

    values = (skill,id)

    cursor.execute(sql,values)

    db.commit()

    if cursor.rowcount > 0:

        flash("Updated Successfully")

    else:

        flash("Developer Not Found")

    return redirect("/developers")


# DELETE PAGE
@app.route("/delete")
def delete_page():

    if "user" not in session:

        return redirect("/login")

    return render_template("delete.html")


# DELETE SUBMIT
@app.route("/delete",methods=["POST"])
def delete():

    email = request.form["email"]

    sql = """
    delete from developers
    where email=%s
    """

    cursor.execute(sql,(email,))

    db.commit()

    if cursor.rowcount > 0:

        flash("Deleted Successfully")

    else:

        flash("User Not Found")

    return redirect("/developers")


# SEARCH PAGE
@app.route("/search")
def search1():

    if "user" not in session:

        return redirect("/login")

    return render_template("search.html")


# SEARCH SUBMIT
@app.route("/search",methods=["POST"])
def search():

    skill = request.form["skill"]

    sql = """
    select * from developers
    where skill LIKE %s
    """

    values = ("%" + skill + "%",)

    cursor.execute(sql,values)

    dev = cursor.fetchall()

    return render_template(
        "search_user.html",
        dev=dev
    )


# REST API
@app.route("/ai-chat", methods=["POST"])
def ai_chatbot():

    question = request.form["question"]

    # FETCH DEVELOPERS
    sql = "select * from developers"

    cursor.execute(sql)

    developers = cursor.fetchall()

    # CREATE CONTEXT
    context = ""

    for dev in developers:

        context += f"""

        Name: {dev[1]}
        Email: {dev[2]}
        Skill: {dev[3]}
        Experience: {dev[4]}

        """

    # AI PROMPT
    prompt = f"""

    You are DevConnect AI Assistant.

    Answer ONLY using the developers data below.

    Developers Data:

    {context}

    User Question:

    {question}

    """

    try:

        # OPENROUTER API REQUEST
        response = requests.post(

            url="https://openrouter.ai/api/v1/chat/completions",

            headers={

                "Authorization":
                "Bearer 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",

                "Content-Type":
                "application/json"
            },

            json={

                "model":
                "openai/gpt-3.5-turbo",

                "messages":[

                    {
                        "role":"user",

                        "content":prompt
                    }
                ]
            }
        )

        data = response.json()

        print(data)

        # SUCCESS RESPONSE
        if "choices" in data:

            answer = data["choices"][0]["message"]["content"]

        else:

            answer = "API Error: " + str(data)

    except Exception as e:

        answer = str(e)

    return render_template(
        "ai_chat.html",
        answer=answer
    )

if __name__ == "__main__":

    app.run(debug=True)
