import pyinputplus as pyip
import re

# ---------------------------------------------
# FULL NAME VALIDATION
# ---------------------------------------------
name = pyip.inputStr(
    prompt="Enter your full name: ",
    blockRegexes=[r'\d', r'[^a-zA-Z\s]'],  # block digits and special characters
    allowRegexes=[r'^[A-Za-z\s]+$'],       # allow only letters and spaces
)
print(f"✅ Name accepted: {name}\n")


# ---------------------------------------------
# AGE VALIDATION
# ---------------------------------------------
age = pyip.inputNum(
    prompt="Enter your age (12–99): ",
    min=12, max=99, limit=3, default='N/A'
)
print(f"✅ Age accepted: {age}\n")


# ---------------------------------------------
# EMAIL VALIDATION
# ---------------------------------------------
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
email = pyip.inputStr(
    prompt="Enter your email: ",
    allowRegexes=[email_pattern],
    blockRegexes=[r'.*'],  # block everything else except allowed pattern
    limit=3, default='N/A'
)
print(f"✅ Email accepted: {email}\n")


# ---------------------------------------------
# PASSWORD VALIDATION (Custom Function)
# ---------------------------------------------
def passwordValidator(password):
    """Checks password strength: 8+ chars, upper, lower, digit, special char."""
    if len(password) < 8:
        raise Exception("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise Exception("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise Exception("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise Exception("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise Exception("Password must contain at least one special character.")
    return password

password = pyip.inputCustom(passwordValidator, prompt="Enter your password: ")
print("✅ Password accepted.\n")


# ---------------------------------------------
# SECURITY PIN VALIDATION (Custom Function)
# ---------------------------------------------
def pinValidator(pin):
    """Validate 5-digit security PIN (no repeating digits)."""
    if not re.match(r"^\d{5}$", pin):
        raise Exception("PIN must be exactly 5 digits.")
    if len(set(pin)) < 5:
        raise Exception("PIN cannot contain repeating digits.")
    return pin

pin = pyip.inputCustom(pinValidator, prompt="Enter your 5-digit security PIN: ")
print("✅ PIN accepted.\n")


# ---------------------------------------------
#  SUMMARY OUTPUT
# ---------------------------------------------
print("\n" + "=" * 40)
print("✅ REGISTRATION COMPLETE!")
print(f"Full Name: {name}")
print(f"Age: {age}")
print(f"Email: {email}")
print(f"Password: {'*' * len(password)}")
print(f"Security PIN: {pin}")
print("=" * 40)

if age == 'N/A' or email == 'N/A':
    print("\nNote: Some fields were skipped or invalid.")
    

with open("registration_data.txt", "a") as file_object:
    file_object.write("\n" + "=" * 40 + "\n")
    file_object.write(f"Full Name: {name}\n")
    file_object.write(f"Age: {age}\n")
    file_object.write(f"Email: {email}\n")
    file_object.write(f"Password: {password}\n")
    file_object.write(f"Security PIN: {pin}\n")
    file_object.write("=" * 40 + "\n")
