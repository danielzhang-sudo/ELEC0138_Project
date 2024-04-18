import sqlite3
import secrets
from defenses import encrypt_password

def init_db():
    # Make a connection to a sqlite database (if there is no connection, create one)
    conn = sqlite3.connect("database.db")

    # Build cursor
    cur = conn.cursor()

    with open('../dataset/products.csv') as f:
        products = f.read().splitlines()

    with open('../dataset/searches.csv') as f:
        searches = f.read().splitlines()

    with open('../dataset/user.csv') as f:
        users = f.read().splitlines()

    # Build one table to store the products name
    cur.execute("DROP TABLE IF EXISTS current_id")

    # build one table to store the usernames and passwords
    with conn:
    ##    cur.execute("""CREATE TABLE IF NOT EXISTS users (
    ##    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ##    username TEXT NOT NULL UNIQUE,
    ##    password TEXT NOT NULL
    ##    )""")

        
        # Add encryption to the password
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        salt TEXT NOT NULL
        )""")

        for i in range(len(users)-1):
            username, password = users[i+1].split(',')
            
            salt = secrets.token_hex(8)
            password, salt = encrypt_password(password, salt)
            
            cur.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", (username, password, salt))
            
            
            # cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            
        #cur.execute("DROP TABLE IF EXISTS current_id")

        

    with conn:
        cur.execute("""CREATE TABLE IF NOT EXISTS products (
        key INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        price TEXT
        )""")
        

        for i in range(len(products)-1):
            name, description, price = products[i+1].split(',')
            cur.execute(f"""INSERT INTO products (name, description, price) VALUES(?, ?, ? )""", (name, description, price,))


    # build one table to store the search history
    with conn:
        cur.execute("""CREATE TABLE IF NOT EXISTS searches (
        user_id INTEGER,
        product_name TEXT,
        searches INTEGER,
        date TEXT
        )""")

        #cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        #user_id = cur.fetchone()[0]


        for i in range(len(searches)-1):
            username, name, search, date = searches[i+1].split(',')
            cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            user_id = cur.fetchone()[0]
            
            cur.execute(f"""INSERT INTO searches (user_id, product_name, searches, date) VALUES(?,?,?,? )""", (user_id, name, search, date))

        #cur.execute(f"""INSERT INTO searches (user_id, price) VALUES(? )""", (name,))
        #cur.execute("DROP TABLE IF EXISTS current_id")


    with conn:


        cur.execute("""CREATE TABLE IF NOT EXISTS current_id (
        table_id INTEGER PRIMARY KEY,
        user_id INTEGER
        )""")

        #cur.execute(f"""INSERT INTO current_id (user_id) VALUES(? )""", (0,))




    # Close database connection
    conn.close()


if __name__=='__main__':
    init_db()
