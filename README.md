# 🔐 Password Strength Checker + Hash Generator (Phase 2)

A comprehensive Flask-based password security analyzer that evaluates password strength, generates multiple cryptographic hashes, checks for data breaches, and detects common passwords. Built for educational purposes and development testing.

---

## ✨ Features

### Phase 1 (Core)
- **Password Strength Analysis** - Five-point evaluation system (0-5 score)
- **Visual Feedback** - Color-coded strength indicator (Weak/Moderate/Strong)
- **Smart Suggestions** - Real-time recommendations for improvement
- **Hash Generation** - MD5, SHA-256, and bcrypt with one-click copy
- **Modern UI** - Clean, minimalist dark theme

### Phase 2 (Advanced) 🆕
- **Argon2 Hashing** - Modern, memory-hard password hashing algorithm
- **Breach Detection** - Have I Been Pwned API integration (k-anonymity)
- **Common Password Check** - Blacklist detection for top passwords
- **Security Warnings** - Critical alerts for compromised passwords
- **Enhanced Safety** - Multi-layered password evaluation

---

## 🎯 Strength Criteria

The analyzer checks for five key elements:

| Criterion | Requirement | Points |
|-----------|-------------|--------|
| **Length** | At least 8 characters | +1 |
| **Lowercase** | Contains a-z | +1 |
| **Uppercase** | Contains A-Z | +1 |
| **Numbers** | Contains 0-9 | +1 |
| **Symbols** | Contains !@#$%^&* etc. | +1 |

**Strength Levels:**
- **0-2 points** → Weak ❌ (Red)
- **3-4 points** → Moderate ⚠️ (Orange)
- **5 points** → Strong ✅ (Green)

**Phase 2 Overrides:**
- Password found in breach → **Forced to Weak** 🚨
- Password is too common → **Downgraded to Weak** ⚠️

---

## 🔐 Hash Types

### ⚠️ Educational Only (Insecure for Passwords)

**MD5**
- 128-bit hash (32 hex characters)
- Speed: ~2 billion hashes/second
- Status: Cryptographically broken since 2004
- Use case: File integrity checks, NOT passwords

**SHA-256**
- 256-bit hash (64 hex characters)
- Speed: ~1 billion hashes/second
- Status: Secure for data integrity, too fast for passwords
- Use case: File verification, blockchain, NOT passwords

### ✅ Secure for Password Storage

**bcrypt**
- Variable-length hash with embedded salt
- Speed: ~300ms per hash (intentionally slow)
- Status: Industry standard, OWASP recommended
- Key feature: Automatic random salting
- Use case: Production password storage

**Argon2** 🆕
- Variable-length hash with memory-hard algorithm
- Speed: Configurable (memory and time cost)
- Status: Winner of Password Hashing Competition 2015
- Key feature: Resistant to GPU/ASIC attacks
- Variants: Argon2d, Argon2i, Argon2id (default)
- Use case: Modern production systems

**Why Argon2 is better:**
- Memory-hard algorithm (requires large RAM)
- Resistant to specialized hardware attacks
- Three variants for different use cases
- Configurable memory cost, time cost, parallelism

---

## 🛡️ Phase 2 Security Features

### 1. Have I Been Pwned Integration

**How it works (k-Anonymity Model):**

```
Your password: "hello123"

Step 1: Hash with SHA-1
→ Full hash: 7c6a180b36896a0a8c02787eeafb0e4c

Step 2: Send only first 5 characters to API
→ API request: /range/7c6a1

Step 3: API returns ~500 hashes starting with 7c6a1
→ Your actual password never leaves your computer!

Step 4: Check locally if full hash is in results
→ Match found? Password is pwned!
```

**Privacy:** Your password is NEVER sent to any server. Only the first 5 characters of the hash are transmitted.

### 2. Common Password Detection

Checks against a blacklist of the most common passwords:
- password, 123456, qwerty, abc123
- letmein, welcome, admin, monkey
- ... and thousands more

**In production:** Load from `10-million-password-list-top-10000.txt`

### 3. Critical Warnings

**Breach Alert (Critical):**
```
🚨 CRITICAL: Password Breached!
This password appeared in 1,234,567 data breaches.
Using it puts your account at extreme risk.
```

**Common Password Alert (Moderate):**
```
⚠️ Common Password Detected
This password is in the top 10,000 most common passwords.
Attackers will try this first.
```

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask 2.0+** - Web framework
- **hashlib** - MD5, SHA-256 (built-in)
- **bcrypt** - Secure password hashing
- **argon2-cffi** 🆕 - Argon2 hashing
- **requests** 🆕 - HTTP client for API calls

### Frontend
- **HTML5** - Semantic markup with Jinja2 templates
- **CSS3** - Custom properties, minimalist dark theme
- **Vanilla JavaScript** - Clipboard API, DOM manipulation

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for breach checking)

### Setup Steps

```bash
# Clone repository
git clone https://github.com/zeelp1696/Password_checker.git
cd Password_checker

# Install Phase 2 dependencies
pip install flask bcrypt argon2-cffi requests

# Run application
python app.py
```

### Access
Open your browser and navigate to: **http://127.0.0.1:5050/**

---

## 📂 Project Structure

```
password_checker/
├── app.py                 # Flask backend with Phase 2 features
├── templates/
│   └── index.html         # Enhanced UI with warnings
├── static/
│   └── style.css          # Refined minimalist dark theme
└── README.md              # This file
```

---

## 💻 How It Works

### Backend Flow (Phase 2)

```
User Input → POST /
    ↓
check_password_strength() [5 criteria check]
    ↓
generate_hashes() [MD5, SHA-256, bcrypt, Argon2] 🆕
    ↓
is_common_password() [Blacklist check] 🆕
    ↓
check_pwned_password() [Breach API] 🆕
    ↓
Override strength if compromised 🆕
    ↓
Render results with warnings
```

### Key Functions

**Phase 1 Functions:**
- `check_password_strength(password)` - 5-point evaluation
- `get_strength_info(score)` - Label/color mapping

**Phase 2 Functions (NEW):**

**`generate_hashes(password)`** - Enhanced
```python
Returns: {
    'insecure': {
        'md5': '...',
        'sha256': '...'
    },
    'secure': {
        'bcrypt': '...',
        'argon2': '...'  # NEW!
    }
}
```

**`is_common_password(password)`** 🆕
```python
# Checks against blacklist
# Returns: True if common, False if unique
```

**`check_pwned_password(password)`** 🆕
```python
# Uses k-anonymity model with Have I Been Pwned API
# Returns: (is_pwned: bool, breach_count: int)
```

---

## 🧪 Testing Examples

### Test Case 1: Weak Password
```
Input: hello
Score: 2/5 (Weak)
Missing: Uppercase, numbers, symbols

Warnings: None (not common or breached)

Hashes:
- MD5:    5d41402abc4b2a76b9719d911017c592
- SHA256: 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
- bcrypt: $2b$12$[random_hash]
- Argon2: $argon2id$v=19$m=65536,t=3,p=4$[random_hash]
```

### Test Case 2: Common Password (Critical)
```
Input: password
Score: FORCED to Weak ⚠️
Original: 5/5, Downgraded due to commonness

Warning: ⚠️ This password is extremely common!
All hashes generated
```

### Test Case 3: Breached Password (Critical)
```
Input: 123456
Score: FORCED to Weak 🚨
Breach count: ~23,000,000+

Warning: 🚨 Password appeared in 23,174,662 data breaches!
All hashes generated
```

### Test Case 4: Strong & Unique
```
Input: MyS3cur3P@ssw0rd!2025
Score: 5/5 (Strong ✅)

No warnings
All hashes generated including Argon2
```

---

## 🔒 Security Best Practices

### For Developers

1. **Never log plaintext passwords**
   ```python
   # ❌ DON'T
   print(f"Password: {password}")
   
   # ✅ DO
   print("Password received and processed")
   ```

2. **Use Argon2 or bcrypt for storage**
   ```python
   # Argon2 (recommended for new projects)
   from argon2 import PasswordHasher
   ph = PasswordHasher()
   hash = ph.hash(password)
   
   # bcrypt (still excellent)
   hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
   ```

3. **Verify passwords correctly**
   ```python
   # Argon2
   try:
       ph.verify(stored_hash, input_password)
       print("✅ Login successful")
   except VerifyMismatchError:
       print("❌ Wrong password")
   
   # bcrypt
   if bcrypt.checkpw(input_password.encode(), stored_hash):
       print("✅ Login successful")
   ```

4. **Check for breaches periodically**
   ```python
   # On password change or periodic security audits
   is_pwned, count = check_pwned_password(new_password)
   if is_pwned:
       return "Choose a different password"
   ```

5. **Block common passwords**
   ```python
   if is_common_password(new_password):
       return "This password is too common"
   ```

---

## 🎓 Educational Notes

### Argon2 vs bcrypt

| Feature | bcrypt | Argon2 |
|---------|--------|--------|
| **Year** | 1999 | 2015 |
| **Algorithm** | Blowfish-based | Memory-hard |
| **Resistance** | Time-based | Time + Memory |
| **GPU Attack** | Moderate | Strong |
| **ASIC Attack** | Weak | Strong |
| **Configurable** | Rounds only | Memory, Time, Parallelism |
| **Status** | Industry standard | Modern standard |

**When to use:**
- **bcrypt:** Legacy systems, widely supported
- **Argon2:** New projects, maximum security

### Have I Been Pwned k-Anonymity

**Why it's safe:**

```
❌ Naive approach:
   Send full password → API checks → Return result
   Problem: API sees your password!

✅ k-Anonymity approach:
   Send 5-char hash prefix → API returns ~500 matches → Check locally
   Result: API never sees your password or full hash!
```

**Technical Details:**
```
SHA-1("password123") = 482c811da5d5b4bc6d497ffa98491e38
                       ^^^^^
                       Only these 5 chars sent to API
```

### Common Password Statistics

Based on real data breach analyses:
- Top 10 passwords = 5% of all passwords
- Top 100 passwords = 10% of all passwords
- Top 10,000 passwords = 20% of all passwords

**That's why checking matters!**

---

## 🚀 What I Learned

### Technical Skills (Phase 1)
- Flask routing and request handling
- Password security fundamentals
- Cryptographic hash functions (MD5, SHA-256, bcrypt)
- Frontend-backend integration with Jinja2
- JavaScript Clipboard API

### New Skills (Phase 2) 🆕
- **API Integration** - Consuming REST APIs with requests library
- **Privacy-preserving queries** - k-anonymity model implementation
- **Advanced hashing** - Argon2 configuration and usage
- **Conditional rendering** - Dynamic UI warnings in Jinja2
- **Error handling** - Network timeouts and API failures
- **Data breach awareness** - Real-world password compromise statistics

### Security Concepts
- Why fast hashing is dangerous for passwords
- Importance of salting in password storage
- Memory-hard vs compute-hard algorithms
- k-anonymity for privacy-preserving lookups
- Password entropy and predictability
- Adaptive cost factors in hash functions

---

## 🔮 Future Enhancements (Phase 3 Preview)

- [ ] **PBKDF2 hashing** - Additional secure algorithm option
- [ ] **Password generator** - Create strong passwords automatically
- [ ] **Entropy calculator** - Show bits of randomness with visualization
- [ ] **Keyboard pattern detection** - Identify "qwerty", "asdfgh" patterns
- [ ] **Dictionary word detection** - Reject common words
- [ ] **Password strength meter** - Real-time visual feedback while typing
- [ ] **Export results** - Save analysis as PDF or image
- [ ] **Multi-language support** - Internationalization
- [ ] **Dark/Light mode toggle** - User preference

---

## 📜 License

This project is open source under the MIT License.

---

## 👤 Author

**Zeel Patel**
- GitHub: [@zeelp1696](https://github.com/zeelp1696)
- Project: [Password_checker](https://github.com/zeelp1696/Password_checker)
- Focus: Cybersecurity & Full-Stack Development

---

## 🙏 Acknowledgments

- **OWASP** - Password storage cheat sheet
- **Troy Hunt** - Have I Been Pwned API
- **Flask Community** - Excellent documentation
- **bcrypt Contributors** - Secure hashing library
- **Argon2 Team** - Modern password hashing standard
- **Cybersecurity Educators** - Best practices and resources

---

## 📊 Project Stats

- **Language Breakdown:** Python 52%, HTML 24%, CSS 24%
- **Version:** 2.0 (Phase 2)
- **Lines of Code:** ~850 (backend + frontend)
- **Dependencies:** 4 (Flask, bcrypt, argon2-cffi, requests)
- **Status:** Active Development
- **API Calls:** Have I Been Pwned (external)

---

## 🐛 Troubleshooting

### Issue: argon2-cffi not installing
```bash
# Windows
pip install argon2-cffi

# If fails, try:
pip install --upgrade pip setuptools
pip install argon2-cffi

# Mac/Linux
pip3 install argon2-cffi
```

### Issue: requests module not found
```bash
pip install requests
```

### Issue: Have I Been Pwned API timeout
```python
# In app.py, increase timeout:
response = requests.get(url, timeout=5)  # Default is 3
```

### Issue: Common password list too small
```python
# Download larger list from:
# https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt

# Load into COMMON_PASSWORDS set in app.py
```

### Issue: Port already in use
```python
# In app.py, change port:
app.run(debug=True, port=5051)  # Try different port
```

---

## 🔧 Configuration

### Adjusting Argon2 Parameters

```python
from argon2 import PasswordHasher

# Default (balanced)
ph = PasswordHasher()

# Higher security (slower)
ph = PasswordHasher(
    time_cost=4,        # Default: 3
    memory_cost=131072, # Default: 65536 (128 MB)
    parallelism=8       # Default: 4
)

# Lower security (faster, for testing)
ph = PasswordHasher(
    time_cost=2,
    memory_cost=32768,
    parallelism=2
)
```

### Expanding Common Password List

```python
# In app.py, load from file:
COMMON_PASSWORDS = set()
with open('common-passwords.txt', 'r') as f:
    for line in f:
        COMMON_PASSWORDS.add(line.strip().lower())
```

---

## 📚 Resources

### Documentation
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Have I Been Pwned API Docs](https://haveibeenpwned.com/API/v3)
- [Argon2 RFC](https://datatracker.ietf.org/doc/html/rfc9106)
- [bcrypt Specification](https://www.usenix.org/legacy/events/usenix99/provos/provos.pdf)

### Tools & Lists
- [SecLists Password Lists](https://github.com/danielmiessler/SecLists/tree/master/Passwords)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)

---

**Made with ❤️ for learning advanced password security and cybersecurity fundamentals**