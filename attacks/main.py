from data import clean_dataset, get_database
from privacy_attack import preprocess, train, predict
from brute_force_attack import username_brute, length_brute
from data_poisoning import automatic_search
from sql_injection import sql_injection, sql_login
from combined import run_combined
import argparse

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--sql_login', action='store_true', default=False)
    parser.add_argument('--path', type=str, default='data.csv')
    parser.add_argument('--dates_update', action='store_true', default=True)
    parser.add_argument('--from_dataset', action='store_true', default=False)
    parser.add_argument('--database', type=str, default='../unsecure_website/database.db')
    parser.add_argument('--k_prod', type=int, default=1)
    parser.add_argument('--n_times', type=int, default=1)
    parser.add_argument("-f", "--file", required=False)
    args = parser.parse_args()

    
    if args.from_dataset:
        print('Cleaning dataset')
        df = clean_dataset(args)
    else:
        print('Getting data from database')
        df = get_database(args)

    scaled_df = preprocess(df)

    # Train model for pivacy attack
    print('Running privacy attack')
    model = train(scaled_df)

    """
    
    # Run brute force, SQL injection and data poisoning
    run_combined(args)

    """

    sql_log = args.sql_login
    
    # Login into somoeone's account with SQL injection
    logged_in = False
    if sql_log:
        print('Trying SQL injection login...')
        logged_in, session = sql_login()
        logged_in = True
        
    if not logged_in:
        print('Trying brute force login...')
        # Login someone's account with brute force
        logged_in, username, password, session = username_brute()

    if logged_in:
        print('Logged in!')
        """
        # Run privacy attack
        target_df = df[df['username'] == username]
        prediction = predict(model, target_df)
        print(f"User '{username}' belongs to class: '{prediction}'")
        """
    
        # Obtain a list of products
        products_list = sql_injection(session)

        # Do data poisoning
        k_prod = args.k_prod
        n_times = args.n_times
        automatic_search(session, products_list, k_prod, n_times)

        print('All attacks completed')

        """
        # Run privacy attack after data poisoning
        df = get_database(args)
        target_df = df[df['username'] == username]
        prediction = predict(model, target_df)
        print(f"User '{username}' belongs to class: '{prediction}'")
        """        
    else:
        print('Failed to log in')


    # Run privacy attack after data poisoning
    
