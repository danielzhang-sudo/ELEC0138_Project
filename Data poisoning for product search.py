import requests
import random
import time

# Web URL Configuration
base_url = 'http://127.0.0.1:5000/'
login_url = f'{base_url}/signin'
search_url = f'{base_url}/search'

# User and product configuration
username = 'USERNAME'   # Username which has been signed up in the website
password = 'PASSWORD'   # Password which has been signed up in the website
products = [f'P{i}' for i in range(1, 21)] 
#products = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15', 'P16', 'P17', 'P18', 'P19', 'P20']  

# Create a session
session = requests.Session()

# Login function
def login():
    # Simulate user login
    login_data = {'username': username, 'password': password}
    response = session.post(login_url, data=login_data)
    if response.status_code == 200:
        print("Login is successful")
        return True
    else:
        print("Login is failed", response.text)
        return False

# Automatic search function
def automatic_search():
    if login(): 
        # Implement continuous search
        for _ in range(10):  
            product_name = random.choice(products)
            response = session.post(search_url, data={'product_name': product_name})
            if response.status_code == 200:
                print(f"Search {product_name} successful")
                print(f"Continue to search product")
            else:
                print(f"search{product_name} failed, status code: {response.status_code}")
            time.sleep(random.randint(1, 2))

    print(f"End of search")

if __name__ == '__main__':
    automatic_search()

