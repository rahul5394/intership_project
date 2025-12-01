from flask import  render_template
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rahul",
    database="login_sign_in"
)

cursor = mydb.cursor()

def login_check(email,password):
    query = """
SELECT email, password1 
FROM login 
WHERE email = %s AND password1 = %s
"""

    values = (email, password)

    cursor.execute(query, values)
    query2 = """select u_name, f_level, age, weight, height, gender, goal from  pers_info  where user_id  in (select user_id from signup where email = %s)"""
    values = (email)
    result = cursor.fetchone()
    dec_login = {}
    if result:
        cursor.execute(query2,values)
        res=cursor.fetchall()
        user_info = {}
        for row in res:
            user_info[row[0]] = {
                "f_level": row[1],
                "age": row[2],
                "weight": row[3],
                "height": row[4],
                "gender": row[5],
                "goal": row[6]
            }

        # 7️⃣ Print the results
        print("Raw fetched rows:")
        print(res)
        print("\nUser info dictionary:")
        print(user_info)

        # 8️⃣ Close cursor and connection

        return 1
    return None
cursor.close()




