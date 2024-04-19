## Run the attacks

To run the attacks, go the `attacks/` folder and run:
```
python main.py
```

This will run the all the attacks in a pipeline:
- A privacy attack against users.
- A SQL injection / brute force attack to login into someone's account.
- A SQL injection to obtain a list of products
- A data poisoning attack that will contaminate the website database.

The `main.py` file accepts several arguments:
- '--sql_login': Attempts to login with SQL injection, otherwise it will do brute force. Default is brute force
- '--from_dataset': Whether to clean the original dataset.
- '--path': Path to the original dataset where the products, customers and history where obtained.
- '--dates_update': Moves the dates specified in the original dataset to be one day before the day the code was executed. Default is True.
- '--database': Path to the website database. Default is the unsecure website database.
- '--k_prod': How many products to search.
- '--n_times': How many times to search each product.

The attacks can also be executed individually. To run an attack:
```
python {attack}.py
```

Each attack may have different arguments:
- SQL: `--login` and `--search`: Login or obtain product list with SQL injection.
- Brute force: None
- Data poisoning: `--username`, `--password` are REQUIRED to indicate and existing username and password. `--k_prod` and `--n_times`: same as inidcated above.
- Privacy attack: `--path`, `--dates_update`, `--from_dataset` and `--database`: Same as above.
