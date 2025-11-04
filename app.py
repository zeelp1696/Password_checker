from flask import Flask, render_template, request
import re

app = Flask(__name__)

# --- Your password checking logic ---
def check_password_strength(password):
    score = 0
    suggestions = []

    # 1️⃣ Length check
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Make your password at least 8 characters long.")

    # 2️⃣ Lowercase check
    if any(c.islower() for c in password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    # 3️⃣ Uppercase check
    if any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    # 4️⃣ Numbers check
    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    # 5️⃣ Special characters check
    if any(c in "!@#$%^&*()-_=+[{]};:'\",<.>/?\\" for c in password):
        score += 1
    else:
        suggestions.append("Add special characters (like !, @, #, or $).")

    return suggestions, score

# --- Flask route ---
@app.route('/', methods=['GET', 'POST'])
def index():
    score = None
    label = ""
    color = ""
    suggestions = []

    if request.method == 'POST':
        password = request.form['password']
        suggestions, score = check_password_strength(password)

        # Decide label and color
        if score <= 2:
            label = "Weak ❌"
            color = "red"
        elif score == 3 or score == 4:
            label = "Moderate ⚠️"
            color = "orange"
        else:
            label = "Strong 💪"
            color = "green"

    return render_template('index.html', score=score, label=label, color=color, suggestions=suggestions)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
