import mysql.connector
def chk(uname, flevel, age, weight, height, gender, goal):

    # MySQL Connection
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rahul",
    database="login_sign_in"
    )

    cursor = mydb.cursor()
    query= """
INSERT INTO pers_info (u_name, f_level, age, weight, height, gender, goal)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
    values = (uname, flevel, age, weight, height, gender, goal)

    cursor.execute(query,values)
    mydb.commit()

# Close the connection
    cursor.close()
    mydb.close()
