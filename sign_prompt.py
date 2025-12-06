import mysql.connector

def get_email():
    try:
        # Connect to MySQL
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rahul",
            database="login_sign_in"
        )

        cursor = mydb.cursor()

        # 1. Get the last inserted user_id
        cursor.execute("SELECT user_id FROM signup ORDER BY user_id DESC LIMIT 1")
        result = cursor.fetchone()

        if not result:
            print("No users found.")
            return None

        last_id = result[0]

        # 2. Get the email for this user_id
        cursor.execute("SELECT email FROM signup WHERE user_id = %s", (last_id,))
        email_result = cursor.fetchone()

        if email_result:
            return email_result[0]
        else:
            print("Email not found for user_id:", last_id)
            return None

    except mysql.connector.Error as e:
        print("MySQL Error:", e)
        return None

# ---- RUN FUNCTION ----


