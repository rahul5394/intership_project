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
    result = cursor.fetchone()
    if result:
        return 1
    return None
def login_check1(email):
    cursor1 = mydb.cursor()
    query2 = """SELECT u_name, f_level, age, weight, height, gender, goal
        FROM pers_info
        WHERE user_id IN (
            SELECT user_id FROM signup WHERE email =%s
        ) """

    user_info={}
    cursor.execute(query2, (email,))
    res = cursor.fetchall()
    for row in res:
        user_info = {
            "uname": row[0],
            "flevel": row[1],
            "age": row[2],
            "weight": row[3],
            "height": row[4],
            "gender": row[5],
            "goal": row[6]
        }

    print(email)
    print(res)
    print(user_info)
    mydb.commit()
    cursor1.close()
    return  user_info