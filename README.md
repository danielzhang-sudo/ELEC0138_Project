## How to run this project

First, create a new environment and install the required packages with:
```
conda create --name 'ELEC0138_Group_O'
conda install --yes --file requirements.txt
```
> [!TIP]
> To ensure all files run smoothly, run on Windows Powershell or Linux terminal.

Run one the two versions of the website with:
```
python app.py
```
This will run the website which will be hosted locally in the machine. You can access it in any browser with the URL: http://127.0.0.1:5000.

## Clean the data and create database

> [!CAUTION]
> The following command may take a long time to execute or hang depending on your computer!

If you wish to run the code to clean the data of the original dataset, please run the combined or the privacy attack including the `--from_dataset` argument:
```
python privacy_attack.py --from_dataset
```
or
```
python main.py --from_dataset
```
This code will take the original dataset and generate a cleaned `.csv` file, and the data for the users, products and searches table for the SQL database.

If you wish to populate the database with the new `.csv` files, first delete `database.db` of both websites if included. Then, create the database of the website by running:
```
python SQLite.py
```
in the `website/` folder. If the `database.db` and the cleaned `.csv` are not included, please go to the first step to ensure that the data from the website database coincides with the cleaned data.


> [!IMPORTANT]
> If the `database.db` is not deleted, it will raise an error. Please ensure it is deleted.

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

A video presentation of the project is available [here]()
