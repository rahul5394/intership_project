from flask import Flask, render_template, request, redirect, jsonify, session
import mysql.connector
import google.generativeai as genai
import pers_info_db as pers_db
import login as log_in
import signup as sign_up
from chatbot import ( markdown_to_html)
from prompt import (get_diet_plan,get_work_sed,get_fod_rec)
from sign_prompt import (get_email)
#session key
app = Flask(__name__)
app.secret_key = ''
# MySQL Connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rahul",
    database="login_sign_in"
)
#api key
genai.configure(api_key="")
#dictonar for session
dec_info={}
dec_pro={}
dec_sed={}
dec_fod={}
# Select Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")
cursor = mydb.cursor()

# -------------------- HOME PAGE (Login) --------------------
@app.route('/')
def home():
    return render_template("index.html", error=None)


# -------------------- LOGIN CHECK --------------------

@app.route('/login', methods=['POST'])
def adduser():
    email = request.form.get("loginEmail")
    password = request.form.get("loginPassword")
    result=log_in.login_check(email,password)
    if result == 1:
        dec_info=log_in.login_check1( request.form.get("loginEmail"))
        dec_pro=get_diet_plan(email)
        dec_sed=get_work_sed(email)
        dec_fod=get_fod_rec(email)
        session['dec_pro'] = dec_pro
        session['dec_info'] = dec_info
        session['dec_sed'] = dec_sed
        session['dec_fod'] = dec_fod
        return redirect("/home")
    else :
        return redirect("/")


@app.route('/signup', methods=['POST'])
def sign__up():
    name = request.form.get("username")
    email = request.form.get("email")
    pno= request.form.get("pno")
    password = request.form.get("password")
    r=sign_up.sign_up_check(name,email,pno,password)

    if r ==1:
        return redirect("/personal")
    else:
        return redirect("/")
# -------------------- CHATBOT PAGE     --------------------
@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")

@app.route('/personal')
def personal():
    return render_template("pers_info.html")

@app.route('/per_info', methods=['POST'])
def per_info():
        uname = request.form.get("u_name")
        flevel = request.form.get("f_level")
        age = request.form.get("age")
        height = request.form.get("height")
        weight = request.form.get("weight")
        gender = request.form.get("gender")
        goal = request.form.get("goal")
        pers_db.chk(uname, flevel, age, weight, height, gender, goal)
        dec_info={'uname':uname,'flevel':flevel,'age':age,'weight':weight,'height':height,'gender':gender,'goal':goal}
        email= get_email()
        dec_pro = get_diet_plan(email)
        dec_sed = get_work_sed(email)
        dec_fod = get_fod_rec(email)
        session['dec_pro'] = dec_pro
        session['dec_sed'] = dec_sed
        session['dec_fod'] = dec_fod
        session['dec_info'] = dec_info
        return redirect("/home")

@app.route('/home')
def home_page():
    return render_template("home.html",dec_info=session['dec_info'],dec_pro=session['dec_pro'],dec_sed=session['dec_sed'],dec_fod=session['dec_fod'])



@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    # Generate response
    response = model.generate_content(user_input)
    raw_text = response.text
    cleaned_text = markdown_to_html(raw_text)
    print(cleaned_text)
    return jsonify({"reply": cleaned_text})


if __name__ == '__main__':
    app.run(debug=True)


