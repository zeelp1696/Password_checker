# =============================================================================
# PHASE 1: PASSWORD CHECKER WITH HASH GENERATION
# =============================================================================
# This Flask app checks password strength AND generates different types of hashes
# Author: Enhanced by AI Assistant for learning purposes
# =============================================================================

from flask import Flask, render_template, request
import re
import hashlib  # ← For basic hashing (MD5, SHA256)
import bcrypt   # ← For secure password hashing

app = Flask(__name__)

# =============================================================================
# FUNCTION 1: PASSWORD STRENGTH CHECKER
# =============================================================================
def check_password_strength(password):
    """
    Checks how strong a password is by testing 5 criteria.
    Returns: (suggestions_list, score_number)
    
    Score breakdown:
    - 0-2 = Weak
    - 3-4 = Moderate  
    - 5   = Strong
    """
    score = 0
    suggestions = []

    # 1️⃣ Length check (at least 8 characters)
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Make your password at least 8 characters long.")

    # 2️⃣ Lowercase check (has a-z)
    if any(c.islower() for c in password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    # 3️⃣ Uppercase check (has A-Z)
    if any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    # 4️⃣ Numbers check (has 0-9)
    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    # 5️⃣ Special characters check (has symbols like !@#$)
    if any(c in "!@#$%^&*()-_=+[{]};:'\",<.>/?\\|`~" for c in password):
        score += 1
    else:
        suggestions.append("Add special characters (like !, @, #, or $).")

    return suggestions, score


# =============================================================================
# FUNCTION 2: HASH GENERATOR
# =============================================================================
def generate_hashes(password):
    """
    Generates multiple hash types from the password.
    
    Returns a dictionary with:
    - 'insecure': MD5 and SHA256 hashes (NEVER use for real passwords!)
    - 'secure': bcrypt hash (USE THIS for real password storage!)
    
    EXPLANATION:
    - password.encode() converts text string to bytes (required for hashing)
    - .hexdigest() converts raw bytes to readable hexadecimal text
    - bcrypt.gensalt() creates a random "salt" (unique random data)
    - .decode() converts bytes back to string for display
    """
    
    # ⚠️ INSECURE HASHES (for educational comparison only!)
    # These are TOO FAST - hackers can crack billions per second
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # ✅ SECURE HASH (this is what real websites should use!)
    # bcrypt is SLOW by design - takes ~0.3 seconds to hash
    # This makes it nearly impossible for hackers to crack
    # gensalt() adds random data so same password = different hash each time!
    bcrypt_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    # Return organized dictionary
    return {
        'insecure': {
            'md5': md5_hash,
            'sha256': sha256_hash
        },
        'secure': {
            'bcrypt': bcrypt_hash
        }
    }


# =============================================================================
# FUNCTION 3: DETERMINE STRENGTH LABEL & COLOR
# =============================================================================
def get_strength_info(score):
    """
    Converts numeric score to user-friendly label and color.
    
    Args:
        score (int): Password strength score (0-5)
        
    Returns:
        tuple: (label_text, color_name, width_percentage)
    """
    if score <= 2:
        return "Weak ❌", "red", "33%"
    elif score in [3, 4]:
        return "Moderate ⚠️", "orange", "66%"
    else:
        return "Strong ✅", "green", "100%"


# =============================================================================
# ROUTE: MAIN PAGE (Handles both GET and POST requests)
# =============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route that handles:
    - GET: Display empty form
    - POST: Process password and show results
    """
    
    # Initialize default values (shown on first page load)
    score = None
    label = ""
    color = ""
    width = "0%"
    suggestions = []
    hashes = None  # ← NEW: Will hold generated hashes
    password = ""  # ← NEW: Store password to display with hashes

    # Check if user submitted the form (POST request)
    if request.method == 'POST':
        # Get password from form input (name="password" in HTML)
        password = request.form['password']
        
        # Run strength check (your original function)
        suggestions, score = check_password_strength(password)
        
        # Get label, color, and bar width based on score
        label, color, width = get_strength_info(score)
        
        # 🆕 GENERATE HASHES (Phase 1 new feature!)
        hashes = generate_hashes(password)
        
        # DEBUGGING INFO (you can see this in terminal when testing)
        print(f"\n{'='*50}")
        print(f"Password analyzed: {password}")
        print(f"Strength score: {score}/5")
        print(f"Label: {label}")
        print(f"MD5: {hashes['insecure']['md5']}")
        print(f"bcrypt: {hashes['secure']['bcrypt']}")
        print(f"{'='*50}\n")

    # Render HTML template and pass all variables to it
    return render_template(
        'index.html',
        score=score,
        label=label,
        color=color,
        width=width,
        suggestions=suggestions,
        hashes=hashes,      # ← NEW: Pass hashes to HTML
        password=password   # ← NEW: Pass password for display
    )


# =============================================================================
# RUN THE APP
# =============================================================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔐 PASSWORD STRENGTH CHECKER WITH HASH GENERATION")
    print("="*60)
    print("📍 Running on: http://127.0.0.1:5050/")
    print("🛑 Press CTRL+C to stop")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5050)
