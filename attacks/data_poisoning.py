import requests
import random
import time

# Web URL Configuration
base_url = 'http://127.0.0.1:5000/'
login_url = f'{base_url}/signin'
search_url = f'{base_url}/search'

### User and product configuration
##username = 'hello'   # Username which has been signed up in the website
##password = 'hello'   # Password which has been signed up in the website
### products = [f'P{i}' for i in range(1, 21)]  
##session = requests.Session()    # Create a session


# Automatic search function
def automatic_search(session, products_list, k_prod, n_times):

    # products_list = sql_injection()
    # Implement continuous search as attack want
    for i, product_name in enumerate(random.choices(products_list, k=k_prod), 1):    # Set how many products to search for the product
        for j in range(n_times):
            response = session.post(search_url, data={'product_name': product_name})
            if response.status_code == 200:
                print(f"Search({i}) {product_name} successful")
            else:
                print(f"Search({i}) {product_name} failed, status code: {response.status_code}")
            time.sleep(random.randint(1, 3))
                
    print("End of search")

if __name__ == '__main__':
    automatic_search()


