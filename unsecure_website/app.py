from flask import Flask, request, redirect, url_for, render_template, abort, flash, session,make_response
import sqlite3
from datetime import datetime, timedelta
import hashlib
import secrets
import pandas as pd

app = Flask(__name__)
# set one secret key
app.secret_key = 'some_random_secret_key'


DATABASE = 'database.db'

# Connect to the Database
def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# Initiate the User Table
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE, 
        password TEXT NOT NULL)''')
        db.commit()


def update_count(product_name):
    # connect to the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check whether the product exist or not
    c.execute(f"SELECT * FROM products WHERE name = '{product_name}'")
    result = c.fetchall()
    if result:

        conn.close()
        return True, result
    conn.close()
    return False, result


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.delete_cookie('username')
    return resp


@app.route('/search', methods=['GET', 'POST'])
def search():
    username = request.cookies.get('username')
    print(username)
    if request.method == 'POST':
        product_name = request.form['product_name']
        # use the update_count function to update the count number
        # the update_count will also return a boole value, represent whether the product exists or not
        product_exists, result = update_count(product_name)

        # back end transmits message back to the front end
        if product_exists:

            db = get_db()
            cursor = db.cursor()
            # 寻找到 user_id
            cursor.execute(f"SELECT user_id FROM users WHERE username='{username}'")
            user_id = cursor.fetchone()
            user_id = user_id[0]

            date = str(datetime.now())

            df = pd.DataFrame()
            for x in result:
                df2 = pd.DataFrame(list(x)).T
                df = pd.concat([df, df2])
            df = df.iloc[:, 1:]
            df.columns=['name','description','price']
            message = "Search is successful"

            # 尝试更新记录
            cursor.execute('''UPDATE searches
                 SET searches = searches + 1, date = ?
                 WHERE user_id = ? AND product_name = ?''', (date, user_id, product_name))

            # 如果没有更新任何记录（意味着记录不存在），则插入新记录
            if cursor.rowcount == 0:
                cursor.execute('''INSERT INTO searches (user_id, product_name, searches, date)
                                 VALUES (?, ?, ?, ?)''', (user_id, product_name, 1, date))

            db.commit()
            db.close()
            return render_template('search.html', message=message, tables=[df.to_html(classes='data', header=True, index=False)], titles=df.columns.values)

        else:
            message = "This product doesn't exist"
            return render_template('search.html', message=message)

    return render_template('search.html')


@app.route('/signin', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # connect to the database, check whether username and password exist
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        account = cursor.fetchone()

        if account:
            # 设置 cookie
            resp = make_response(redirect(url_for('search', success='Logged in successfully!')))
            resp.set_cookie('username', username, max_age=60 * 60 * 24)  # 有效期1天

            return resp


        else:
            message = "Login failed. Please try again."
            return render_template('login.html', message=message), 401

    return render_template('login.html')










@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        # make connection with the database
        db = get_db()
        cursor = db.cursor()

        # check whether the username has existed in the table
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

        # if the username has existed, warn the user
        if cursor.fetchone():
            return render_template('signup.html', message = 'The username is already taken. Please try another one.')


        # insert the new username and password
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()

        # finally, go back to the home page
        return render_template('index.html', message='You have signed up successfully!. <br> Sign in or sign up another account')

    return render_template('signup.html')


if __name__ == '__main__':
    # initialize the users table (if there is no users table)
    init_db()
    # run the website
    app.run(debug=True)
