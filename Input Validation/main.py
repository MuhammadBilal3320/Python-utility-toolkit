import pyinputplus
import re

print("*****************************************")
print("*      Smart Form Validation System     *")
print("*****************************************")


# user_full_name = pyinputplus.inputStr(
#     prompt="Enter Full Name: ",
#     allowRegexes=[r"^[A-Za-z]+(?:[ -][A-Za-z]+)*$"],
#     blockRegexes=[r".*\d.*"],
#     limit=3
# )

# user_age = pyinputplus.inputInt(prompt="Enter Your Age: ", min=12, max=99 )

# user_email = pyinputplus.inputEmail(prompt="Enter Email: ",)

# user_password = pyinputplus.inputStr(
#     prompt="Enter Password: ",
#     allowRegexes=[
#         r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{8,}$"
#     ],
#     blockRegexes=[('.*', "Invalid password! Must be at least 8 characters long and include uppercase, lowercase, digit, and special character.")]
# )


def pinValidator(pin):
    """Validate 5-digit security PIN (no repeating digits)."""
    if not re.match(r"^\d{5}$", pin):
        raise Exception("PIN must be exactly 5 digits.")
    if len(set(pin)) < 5:
        raise Exception("PIN cannot contain repeating digits.")
    return pin

pin = pyinputplus.inputCustom(pinValidator, prompt="Enter your 5-digit security PIN: ")
print("✅ PIN accepted.\n")