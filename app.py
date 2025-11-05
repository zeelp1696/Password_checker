# =============================================================================
# PHASE 2: PASSWORD CHECKER WITH ADVANCED SECURITY FEATURES
# =============================================================================
# New in Phase 2:
# - Argon2 hashing (modern alternative to bcrypt)
# - Have I Been Pwned breach check (k-anonymity model)
# - Common password blacklist detection
# =============================================================================

from flask import Flask, render_template, request
import re
import hashlib
import bcrypt
from argon2 import PasswordHasher  # ← NEW: Argon2 support
from argon2.exceptions import HashingError
import requests  # ← NEW: For API calls
import os

app = Flask(__name__)

# =============================================================================
# COMMON PASSWORDS LIST (Top 100 for demo - expand to 10,000 in production)
# =============================================================================
# In production, load from a file containing 10,000+ common passwords
# Download from: https://github.com/danielmiessler/SecLists/tree/master/Passwords
COMMON_PASSWORDS = {
    'password', '123456', '123456789', 'qwerty', 'abc123', 'monkey', 
    '1234567', 'letmein', 'trustno1', 'dragon', 'baseball', 'iloveyou',
    'master', 'sunshine', 'ashley', 'bailey', 'shadow', 'superman',
    'password1', '123123', 'admin', 'welcome', 'login', 'hello',
    'passw0rd', 'password123', 'qwerty123', '12345678', '111111',
    # Add more as needed...
}

# =============================================================================
# FUNCTION 1: PASSWORD STRENGTH CHECKER (Phase 1 - unchanged)
# =============================================================================
def check_password_strength(password):
    """
    Checks password strength based on 5 criteria.
    Returns: (suggestions_list, score_number)
    """
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Make your password at least 8 characters long.")

    if any(c.islower() for c in password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    if any(c in "!@#$%^&*()-_=+[{]};:'\",<.>/?\\|`~" for c in password):
        score += 1
    else:
        suggestions.append("Add special characters (like !, @, #, or $).")

    return suggestions, score


# =============================================================================
# FUNCTION 2: HASH GENERATOR (Enhanced for Phase 2)
# =============================================================================
def generate_hashes(password):
    """
    Generates multiple hash types including Argon2.
    
    NEW in Phase 2: Added Argon2 hash generation
    
    Returns dictionary with:
    - 'insecure': MD5, SHA256 (educational only)
    - 'secure': bcrypt, Argon2 (production-ready)
    """
    
    # ⚠️ INSECURE HASHES (unchanged from Phase 1)
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # ✅ SECURE HASHES
    # bcrypt (Phase 1)
    bcrypt_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    # 🆕 Argon2 (Phase 2 - NEW!)
    # Argon2 won the Password Hashing Competition in 2015
    # More resistant to GPU/ASIC attacks than bcrypt
    ph = PasswordHasher()  # Uses secure defaults
    try:
        argon2_hash = ph.hash(password)
    except HashingError:
        argon2_hash = "Error generating hash"
    
    return {
        'insecure': {
            'md5': md5_hash,
            'sha256': sha256_hash
        },
        'secure': {
            'bcrypt': bcrypt_hash,
            'argon2': argon2_hash  # ← NEW!
        }
    }


# =============================================================================
# FUNCTION 3: CHECK COMMON PASSWORD (NEW - Phase 2)
# =============================================================================
def is_common_password(password):
    """
    Checks if password is in the common passwords list.
    
    EXPLANATION:
    - Converts to lowercase for case-insensitive check
    - Returns True if password is too common
    - In production, this list should contain 10,000+ passwords
    
    Returns: Boolean (True if common, False if unique)
    """
    return password.lower() in COMMON_PASSWORDS


# =============================================================================
# FUNCTION 4: HAVE I BEEN PWNED CHECK (NEW - Phase 2)
# =============================================================================
def check_pwned_password(password):
    """
    Checks if password appears in data breaches using Have I Been Pwned API.
    
    HOW IT WORKS (k-Anonymity Model):
    1. Hash the password using SHA-1
    2. Send only the first 5 characters of hash to API
    3. API returns all hashes starting with those 5 chars
    4. Check locally if full hash appears in results
    
    This way, your actual password NEVER leaves your machine!
    
    Returns: (is_pwned: Boolean, breach_count: int)
    """
    
    # Step 1: Hash password with SHA-1
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    
    # Step 2: Split hash into prefix (first 5 chars) and suffix (rest)
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    # Step 3: Query Have I Been Pwned API with only the prefix
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    try:
        response = requests.get(url, timeout=3)
        
        if response.status_code != 200:
            # API error - return safe default
            return False, 0
        
        # Step 4: Check if our suffix appears in the results
        # Response format: "SUFFIX:COUNT\r\n" (one per line)
        for line in response.text.splitlines():
            hash_suffix, count = line.split(':')
            if hash_suffix == suffix:
                # Found! Password is in breach database
                return True, int(count)
        
        # Not found - password is safe (so far)
        return False, 0
        
    except requests.RequestException:
        # Network error - return safe default
        return False, 0


# =============================================================================
# FUNCTION 5: DETERMINE STRENGTH LABEL & COLOR (Phase 1 - unchanged)
# =============================================================================
def get_strength_info(score):
    """
    Converts numeric score to user-friendly label and color.
    """
    if score <= 2:
        return "Weak ❌", "red", "33%"
    elif score in [3, 4]:
        return "Moderate ⚠️", "orange", "66%"
    else:
        return "Strong ✅", "green", "100%"


# =============================================================================
# ROUTE: MAIN PAGE (Enhanced for Phase 2)
# =============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route with Phase 2 enhancements:
    - Common password detection
    - Breach checking via Have I Been Pwned
    - Argon2 hash generation
    """
    
    # Initialize default values
    score = None
    label = ""
    color = ""
    width = "0%"
    suggestions = []
    hashes = None
    password = ""
    
    # 🆕 Phase 2 variables
    is_common = False
    is_pwned = False
    breach_count = 0

    if request.method == 'POST':
        password = request.form['password']
        
        # Phase 1: Run strength check
        suggestions, score = check_password_strength(password)
        label, color, width = get_strength_info(score)
        
        # Phase 1: Generate hashes
        hashes = generate_hashes(password)
        
        # 🆕 Phase 2: Check if password is too common
        is_common = is_common_password(password)
        if is_common:
            suggestions.insert(0, "⚠️ This password is extremely common! Choose a unique one.")
            # Downgrade strength if common
            if score > 2:
                label = "Weak ❌"
                color = "red"
                width = "33%"
        
        # 🆕 Phase 2: Check if password was breached
        is_pwned, breach_count = check_pwned_password(password)
        if is_pwned:
            suggestions.insert(0, f"🚨 This password appeared in {breach_count:,} data breaches! Never use it!")
            # Force to weak if pwned
            label = "Weak ❌"
            color = "red"
            width = "33%"
        
        # Debugging output
        print(f"\n{'='*60}")
        print(f"Password: {password}")
        print(f"Strength: {score}/5 - {label}")
        print(f"Common: {is_common}")
        print(f"Pwned: {is_pwned} ({breach_count:,} times)" if is_pwned else f"Pwned: {is_pwned}")
        print(f"Argon2: {hashes['secure']['argon2'][:50]}...")
        print(f"{'='*60}\n")

    return render_template(
        'index.html',
        score=score,
        label=label,
        color=color,
        width=width,
        suggestions=suggestions,
        hashes=hashes,
        password=password,
        is_common=is_common,      # ← NEW
        is_pwned=is_pwned,        # ← NEW
        breach_count=breach_count # ← NEW
    )


# =============================================================================
# RUN THE APP
# =============================================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔐 PASSWORD STRENGTH CHECKER - PHASE 2 EDITION")
    print("="*70)
    print("✅ Basic strength checking")
    print("✅ Hash generation (MD5, SHA-256, bcrypt, Argon2)")
    print("✅ Common password detection")
    print("✅ Have I Been Pwned breach checking")
    print("="*70)
    print("📍 Running on: http://127.0.0.1:5050/")
    print("🛑 Press CTRL+C to stop")
    print("="*70 + "\n")
    
    app.run(debug=True, port=5050)
