
from db_utils import connect_db
from textblob import TextBlob

# === INTENT KEYWORDS ===
JOIN_DATE_KEYWORDS = ["joined", "joining date", "date of join", "join date", "my join date", "when did i join"]
DEPARTMENT_KEYWORDS = ["department", "dept"]
ROLE_KEYWORDS = ["role", "my role", "position", "postion"]
SPOUSE_KEYWORDS = ["wife", "husband", "spouse", "hasbund"]
# ADDRESS_KEYWORDS = ["address", "home"]
CONTACT_KEYWORDS = ["contact", "phone", "mobile"]

def normalize_input(user_input):
    blob = TextBlob(user_input)
    corrected_text = str(blob.correct())

    if corrected_text.lower() == user_input.lower():
        return user_input.lower()
    if len(user_input.split()) <= 3:
        return corrected_text.lower()
    return user_input.lower()

def get_db_response(user_input, emp_id=None):
    if not emp_id:
        return "Please provide an employee ID."

    user_input_lower = normalize_input(user_input)

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    try:
        # === OFFICE DETAILS ===
        if any(word in user_input_lower for word in DEPARTMENT_KEYWORDS):
            cursor.execute("SELECT department FROM employee_office WHERE emp_id = %s", (emp_id,))
            row = cursor.fetchone()
            return f"You're in the {row['department']} department." if row else "I couldn't find your department information."

        elif any(word in user_input_lower for word in ROLE_KEYWORDS):
            cursor.execute("SELECT role, department FROM employee_office WHERE emp_id = %s", (emp_id,))
            row = cursor.fetchone()
            if row:
                return f"Your role is {row['role']} in the {row['department']} department."
            return "I couldn't find your role and department information."

        elif any(word in user_input_lower for word in JOIN_DATE_KEYWORDS):
            cursor.execute("SELECT join_date FROM employee_office WHERE emp_id = %s", (emp_id,))
            row = cursor.fetchone()
            return f"You joined the company on {row['join_date']}." if row else "I couldn't find your joining date."

        # === PERSONAL DETAILS ===
        elif any(word in user_input_lower for word in SPOUSE_KEYWORDS):
            cursor.execute("SELECT spouse_name FROM employee_personal WHERE emp_id = %s", (emp_id,))
            row = cursor.fetchone()
            return f"Your spouse's name is {row['spouse_name']}." if row and row['spouse_name'] else "I couldn't find spouse information for you."

        elif "name" in user_input_lower and not any(x in user_input_lower for x in SPOUSE_KEYWORDS):
            cursor.execute("SELECT full_name FROM employee_personal WHERE emp_id = %s", (emp_id,))
            row = cursor.fetchone()
            return f"Your full name is {row['full_name']}." if row else "I couldn't find your name."

        elif "age" in user_input_lower:
            cursor.execute("SELECT age FROM employee_personal WHERE emp_id = %s", (emp_id,))
            row = cursor.fetchone()
            return f"You're {row['age']} years old." if row else "I couldn't find your age information."

        # elif any(word in user_input_lower for word in ADDRESS_KEYWORDS):
        #     cursor.execute("SELECT address FROM employee_personal WHERE emp_id = %s", (emp_id,))
        #     row = cursor.fetchone()
        #     return f"Your address is {row['address']}." if row else "I couldn't find your address."

        elif any(word in user_input_lower for word in CONTACT_KEYWORDS):
            cursor.execute("SELECT contact_number FROM employee_personal WHERE emp_id = %s", (emp_id,))
            row = cursor.fetchone()
            return f"Your contact number is {row['contact_number']}." if row else "I couldn't find your contact number."

    finally:
        cursor.close()
        conn.close()

    return "I'm sorry, I don't understand the question."

