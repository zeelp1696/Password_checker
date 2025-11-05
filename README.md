# Password Strength Checker + Hash Generator

A Flask-based password analyzer that scores password strength on five criteria and generates MD5, SHA‑256, and bcrypt hashes. Includes copy-to-clipboard actions and a modern, lightweight UI.

---

## Features completed

- Five-criteria strength scoring: length (≥ 8), lowercase, uppercase, digit, symbol.
- Strength label and visual bar (Weak, Moderate, Strong).
- Actionable suggestions for missing criteria.
- Hash generation:
  - MD5 (educational, not for storage)
  - SHA‑256 (educational, not for storage)
  - bcrypt (adaptive, salted; recommended)
- One-click “Copy” for each hash.
- Responsive, minimal UI.

---

## Tech stack

- Python 3.8+
- Flask
- hashlib (MD5, SHA‑256)
- bcrypt (secure hashing)
- HTML5, CSS3, vanilla JS

---

## Installation

optional: python -m venv .venv && source .venv/bin/activate # macOS/Linux
optional: .venv\Scripts\activate # Windows
pip install flask bcrypt

---

## Run

python app.py

Then open: http://127.0.0.1:5050/

---

## Usage

- Enter a password and submit.
- See strength label, score (/5), animated bar, and suggestions.
- Scroll to “Generated Hashes” to copy MD5, SHA‑256, and bcrypt outputs.

---

## What the checker evaluates

- +1 if length ≥ 8  
- +1 if contains lowercase  
- +1 if contains uppercase  
- +1 if contains digits  
- +1 if contains symbols

Score mapping:
- 0–2 = Weak
- 3–4 = Moderate
- 5 = Strong

---

## Security notes

- Do not store or log plaintext passwords.
- Do not use MD5 or SHA‑256 alone for password storage.
- Use adaptive, salted hashes (bcrypt, Argon2, PBKDF2).
- bcrypt output changes each run (random salt); verify with `bcrypt.checkpw()`.

Verify bcrypt on login:

bcrypt.checkpw(plaintext.encode(), stored_hash.encode())

---

## Project structure

password_checker/
├─ app.py # Flask route, strength logic, hash generation
├─ templates/
│ └─ index.html # Form, results, suggestions, hashes
└─ static/
└─ style.css # UI styles and animations

---

## Roadmap (next)

- Add Argon2 / PBKDF2 options.
- “Have I Been Pwned” breach check (k-anonymity).
- Common password blacklist and entropy hints.
- Built-in password generator.

---

## License

MIT