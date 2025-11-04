🧠 Project Name: Password Strength Checker (Cyber Security Project)
📌 Description
This project checks how strong a password is using Python and Flask. It shows if a password is Weak, Moderate, or Strong with a colored bar (red, yellow, green) and gives suggestions to make the password stronger. It is my learning project about cyber security basics and backend with Flask.

🚀 Features
✅ Checks for:

Password length (8+ characters)
Uppercase letters
Lowercase letters
Numbers
Special symbols
✅ Shows a colored bar to show strength ✅ Gives tips to improve weak passwords ✅ Built using Flask, HTML, and CSS

⚙️ Technologies Used
Python 3
Flask (for the web app)
HTML + CSS (for the frontend)
🧩 How It Works
User enters a password in the website.

Flask sends the password to Python backend.

The backend runs the strength check using logic like:

if any(c.islower() for c in password):
    score += 1
The result is shown with a colored bar and text like “Weak ❌”, “Moderate ⚠️”, or “Strong ✅”.

🖥️ How to Run
Install Flask:

pip install flask
Run the app:

python app.py
Open your browser and go to:

http://127.0.0.1:5000/
🧰 Folder Structure
password_checker/
│
├── app.py                # Main Flask backend
├── static/
│   ├── style.css         # Bar colors and design
│
├── templates/
│   ├── index.html        # Frontend form
│
└── README.md             # Project info
🧠 What I Learned
How to use Python logic for password checking
How to make a simple Flask web app
How to use HTML and CSS for styling
How backend and frontend work together
