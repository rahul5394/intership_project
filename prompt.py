import mysql.connector
import google.generativeai as genai
import re
model = genai.GenerativeModel("gemini-2.0-flash")
genai.configure(api_key="AIzaSyA3H0q2K-0XXjnsrra4BgmCdiUKMVKytzE")

# 2) Load model
# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rahul",
    database="login_sign_in"
)

# ---------------------------------------------------------
# FUNCTION: Fetch user info, get AI diet plan, return dict
# ---------------------------------------------------------
def get_diet_plan(email):
    cursor = mydb.cursor()

    # --- Fetch user data ---
    query = """
        SELECT u_name, f_level, age, weight, height, gender, goal
        FROM pers_info
        WHERE user_id IN (
            SELECT user_id FROM signup WHERE email = %s
        )
    """
    cursor.execute(query, (email,))
    rows = cursor.fetchall()

    if not rows:
        print("❌ No user found for this email!")
        return {}

    row = rows[0]
    flevel, age, weight, height, gender, goal = row[1], row[2], row[3], row[4], row[5], row[6]

    # --- Build AI prompt ---
    prompt = f"""
    User data:
    age={age}, weight={weight}, height={height}, gender={gender}, goal={goal}, fitness level={flevel}

    Suggest an Indian diet plan in this exact format:
    Breakfast:
    Lunch:
    Dinner:
    Snacks:
    Only list items. No extra text.
    """

    # --- Call AI model (Gemini / ChatGPT) ---
    response = model.generate_content(prompt)
    bot_output = response.text.strip()

    # --- Extract meals ---
    pattern = r"(Breakfast|Lunch|Dinner|Snacks|Snack):"
    parts = re.split(pattern, bot_output, flags=re.IGNORECASE)

    meals = {"breakfast": "", "lunch": "", "dinner": "", "snacks": ""}

    for i in range(1, len(parts), 2):
        heading = parts[i].lower()
        content = parts[i + 1].strip()
        if "breakfast" in heading:
            meals["breakfast"] = content
        elif "lunch" in heading:
            meals["lunch"] = content
        elif "dinner" in heading:
            meals["dinner"] = content
        elif "snack" in heading:
            meals["snacks"] = content

    # --- Return dictionary ---
    return meals
def get_work_sed(email):
    cursor = mydb.cursor()

    # --- Fetch user data ---
    query = """
        SELECT u_name, f_level, age, weight, height, gender, goal
        FROM pers_info
        WHERE user_id IN (
            SELECT user_id FROM signup WHERE email = %s
        )
    """
    cursor.execute(query, (email,))
    rows = cursor.fetchall()

    if not rows:
        print("❌ No user found for this email!")
        return {}

    row = rows[0]
    flevel, age, weight, height, gender, goal = row[1], row[2], row[3], row[4], row[5], row[6]

    # --- Build AI prompt ---
    prompt = f"""
    User data:
    age={age}, weight={weight}, height={height}, gender={gender}, goal={goal}, fitness level={flevel}

    Please provide the following sections ONLY:

    Morning Workout:
    Strength Training:
    Steps Goal:
    Water Intake:
    Sleep Schedule:

    Only list items. No extra text.
    """

    # --- Call AI model ---
    response = model.generate_content(prompt)
    bot_output = response.text.strip('*')

    # --- Extract categories ---
    pattern = r"(Morning Workout|Strength Training|Steps Goal|Water Intake|Sleep Schedule):"
    parts = re.split(pattern, bot_output, flags=re.IGNORECASE)

    daily_data = {
        "morning_workout": "",
        "strength_training": "",
        "steps_goal": "",
        "water_intake": "",
        "sleep_schedule": ""
    }

    # --- Arrange extracted data ---
    for i in range(1, len(parts), 2):
        heading = parts[i].strip().lower()
        content = parts[i + 1].strip()

        if "morning workout" in heading:
            daily_data["morning_workout"] = content.strip('*')
        elif "strength training" in heading:
            daily_data["strength_training"] = content.strip('*')
        elif "steps goal" in heading:
            daily_data["steps_goal"] = content.strip('*')
        elif "water intake" in heading:
            daily_data["water_intake"] = content.strip('*')
        elif "sleep schedule" in heading:
            daily_data["sleep_schedule"] = content.strip('*')

    # --- Final dictionary returned ---
    return daily_data
def get_fod_rec(email):
    cursor = mydb.cursor()

    # --- Fetch user data ---
    query = """
        SELECT u_name, f_level, age, weight, height, gender, goal
        FROM pers_info
        WHERE user_id IN (
            SELECT user_id FROM signup WHERE email = %s
        )
    """
    cursor.execute(query, (email,))
    rows = cursor.fetchall()

    if not rows:
        print("❌ No user found for this email!")
        return ""

    row = rows[0]
    flevel, age, weight, height, gender, goal = row[1], row[2], row[3], row[4], row[5], row[6]

    # --- AI Prompt (Food Recommendation ONLY) ---
    prompt = f"""
    User data:
    age={age}, weight={weight}, height={height}, gender={gender}, goal={goal}, fitness level={flevel}

    Provide ONLY the following section:

     Food Recommendation:
    not any dieat or sedule
    No extra text. name of food and caleris.
    """

    # --- Call AI Model ---
    response = model.generate_content(prompt)
    bot_output = response.text.strip()

    # --- Extract ONLY Food Recommendation ---
    pattern = r"Food Recommendation:"
    parts = re.split(pattern, bot_output, flags=re.IGNORECASE)

    if len(parts) < 2:
        return "No food recommendation generated."

    food_reco = parts[1].strip('*')

    return food_reco.strip('*')



