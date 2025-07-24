import re

def is_valid_email(email):
    # Basic regex for email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def is_valid_password(password):
    # Simple rule: minimum 6 characters
    return password is not None and len(password) >= 6

def validate_user_data(data, require_password=True):
    errors = []
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not name.strip():
        errors.append("Name is required")

    if not email or not is_valid_email(email):
        errors.append("Valid email is required")

    if require_password and not is_valid_password(password):
        errors.append("Password must be at least 6 characters")

    return errors
