from flask import Flask, request, redirect, url_for, render_template, abort, flash, session
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'some_random_secret_key'


DATABASE = 'database.db'
login_attempts = {}

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

# used to avoid brute force attack
def check_attempt(ip):
    if ip in login_attempts:
        attempts, last_attempt = login_attempts[ip]
        if datetime.now() - last_attempt < timedelta(minutes=5) and attempts >= 5:
            return False
        elif datetime.now() - last_attempt >= timedelta(minutes=5):
            login_attempts[ip] = (0, datetime.now())
    return True


def record_attempt(ip):
    if ip in login_attempts:
        attempts, _ = login_attempts[ip]
        login_attempts[ip] = (attempts + 1, datetime.now())
    else:
        login_attempts[ip] = (1, datetime.now())

# 更新搜索次数，这里的核心是确定被搜索的产品是否位于产品列表内，存在返回True, 不存在返回 False
def update_count(product_name):
    # connect to the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Check whether the product exist or not
    c.execute("SELECT name FROM products WHERE name = ?", (product_name,))
    result = c.fetchone()
    if result:

        conn.close()
        return True
    conn.close()
    return False


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/search', methods=['GET', 'POST'])
def search():


    success = request.args.get('success', default='', type=str)  # 返回默认值空字符串，如果没有提供 'text'

    if request.method == 'POST':
        product_name = request.form['product_name']
        # use the update_count function to update the count number
        # the update_count will also return a boole value, represent whether the product exists or not
        product_exists = update_count(product_name)

        # back end transmits message back to the front end
        if product_exists:
            # 从 current_id table 中调用 user_id
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("SELECT user_id FROM current_id WHERE table_id = ?", (1,))
            # 获取查询结果
            result = c.fetchone()
            user_id = result[0]

            message = "Search is successful"
            # 现在我有product_name，有user_id, 要么加1， 要么插入一个
            conn = sqlite3.connect('database.db')
            c = conn.cursor()

            # 尝试更新记录
            c.execute('''UPDATE searches
                             SET searches = searches + 1
                             WHERE user_id = ? AND product_name = ?''', (user_id, product_name))

            # 如果没有更新任何记录（意味着记录不存在），则插入新记录
            if c.rowcount == 0:
                c.execute('''INSERT INTO searches (user_id, product_name, searches)
                                 VALUES (?, ?, ?)''', (user_id, product_name, 1))

            conn.commit()
            conn.close()



            # 这里的关键是，
            return render_template('search.html', message=message)


        else:
            message = "This product doesn't exist"
            return render_template('search.html', message=message)

    # 这里的 return 相当于是
    return render_template('search.html', success=success)


@app.route('/signin', methods=['GET', 'POST'])
def login():

    # Get the user IP address
    user_ip = request.remote_addr

    # Defence against the brute force attack
    if not check_attempt(user_ip):
        abort(429, description="Too many login attempts. Please try again later.")

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # connect to the database
        db = get_db()
        cursor = db.cursor()

        # check whether username and password exist
        # statement safe from SQL injection
        # cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password,))

        # statement vulnerable to the SQL injection
        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")

        # as long as account is not none, then we could successfully log in
        account = cursor.fetchone()

        if account:
            # In this part, we check the user id according to the username
            cursor.execute(f"SELECT user_id FROM users WHERE username='{username}'")

            user_id = cursor.fetchone()
            user_id = user_id[0]
            print("The user id is", user_id)


            # 每次登录成功，就需要在 current_id 库里面改一下 user_id
            cursor.execute("UPDATE current_id SET user_id = ? WHERE table_id = ?", (user_id,1,))

            db.commit()
            db.close()

            login_attempts[user_ip] = (0, datetime.now())  # Reset on successful login
            return redirect(url_for('search', success='Logged in successfully!'))

        else:
            record_attempt(user_ip)
            message =  "Login failed. Please try again."
            return render_template('login.html', message = message)

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
    init_db()
    app.run(debug=True)