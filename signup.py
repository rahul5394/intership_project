from flask import Flask, render_template, request, redirect
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rahul",
    database="login_sign_in"
)

cursor = mydb.cursor()
def sign_up_check(name,email,pno,password):
    query = "insert into signup  (uname, email,p_number,password1) values (%s, %s, %s, %s)"
    values = (name, email, pno, password)

    cursor.execute(query, values)
    mydb.commit()

    #add value  login table
    cursor1 = mydb.cursor()
    query = "insert into login  (email,password1) values (%s, %s)"
    values = (email, password)
    cursor1.execute(query, values)
    mydb.commit()
    if cursor.rowcount > 0:
        return 1

    else:
        print("Login Failed!")
        return render_template("index.html", error="Invalid Email or Password")
