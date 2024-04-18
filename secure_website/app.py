from flask import Flask, request, redirect, url_for, render_template, abort, flash, session,make_response, send_file    
import sqlite3
from datetime import datetime, timedelta
from captcha.image import ImageCaptcha                              
import random                                                      
from io import BytesIO
import pandas as pd             
import hashlib
import secrets                                 
from defenses import login_attempts, check_attempt, record_attempt, generate_random_text, create_captcha, serve_captcha, encrypt_password


app = Flask(__name__)
# set one secret key
app.secret_key = 'some_random_secret_key'

DATABASE = 'database.db'
# login_attempts = {}

# Connect to the Database
def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# Initiate the User Table and search table
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE, 
        password TEXT NOT NULL,
        salt TEXT NOT NULL)''')
        db.commit()

"""
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
"""
def update_count(product_name):
    # connect to the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
 
    # Check whether the product exist or not
    # c.execute("SELECT * FROM products WHERE name = ?", (product_name,))
    
    # Vulnearble to SQL
    c.execute(f"SELECT * FROM products WHERE name = '{product_name}'")  # ' OR '1'='1
    result = c.fetchall()
    if result:
 
        conn.close()
        return True, result
    conn.close()
    return False, result



"""
# Function to generate captcha by choosing random text                                                                 
def generate_random_text(length=4):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(characters) for _ in range(length))

# Function to generate a random color in hexadecimal format
def random_color():
    return "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

# Function to create a captcha image with given text
def create_captcha(text):
    captcha = ImageCaptcha(width=200, height=80)
    color = random_color()
    image = captcha.create_captcha_image(text, color, (255, 255, 255))
    captcha.create_noise_dots(image, color=random_color(), number=100)
    captcha.create_noise_curve(image, color=random_color())
    
    # Save the image to a BytesIO stream rather than a file
    data = BytesIO()
    image.save(data, 'PNG')
    data.seek(0)
    return data

# Serve the captcha image via an HTTP response
def serve_captcha():
    random_text = generate_random_text(4)
    session['captcha'] = random_text
    image_data = create_captcha(random_text)
    return send_file(image_data, mimetype='image/png')

# Encrypt password with salt and pepper
def encrypt_password(password, salt):
 
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
 
    # Add the salt to the password and hash it
    hash_object.update(password.encode() + salt.encode())
 
    # Get the hash of the password
    hash_password = hash_object.hexdigest()
 
    # Add the pepper to the password and hash it
    hash_object.update(hash_password.encode() + PEPPER.encode())
    hash_password = hash_object.hexdigest()
    return hash_password, salt
"""



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
    # Retrieve username from cookie
    username = request.cookies.get('username')

    if request.method == 'POST':
        user_captcha_response = request.form['captcha_input']

        # Validate the captcha                                       
        if not user_captcha_response or user_captcha_response != session.get('captcha', ''):        
            return render_template('search.html', message="Incorrect captcha, please try again.")   
        
        # Retrieve product details for the submitted product name from the database
        product_name = request.form['product_name']
        product_exists, result = update_count(product_name)

        # Check if the product exists
        if product_exists:
            
            db = get_db()
            cursor = db.cursor()

            # Search user_id
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()
            user_id = user_id[0]

            date = str(datetime.now())

            
            name_list, desc_list, price_list = [], [], []
            for x in result:
                print(x)
                _, name, desc, price = x
                name_list.append(name)
                desc_list.append(desc)
                price_list.append(price)
            df = pd.DataFrame({'name':name_list,'description':desc_list,'price':price_list})
            #df = pd.DataFrame()
            # for x in result:
            #     print(x)
            #     df2 = pd.DataFrame(list(x)).T
            #     df = pd.concat([df, df2])
            # df = df.iloc[:, 1:]
            # df.columns=['name','description','price']
            message = "Search is successful"

            # Update search count
            cursor.execute('''UPDATE searches
                 SET searches = searches + 1, date = ?
                 WHERE user_id = ? AND product_name = ?''', (date, user_id, product_name))

            # If no search record, insert a new one
            if cursor.rowcount == 0:
                cursor.execute('''INSERT INTO searches (user_id, product_name, searches, date) 
                                 VALUES (?, ?, ?, ?)''', (user_id, product_name, 1, date))
            db.commit()
            db.close()

            # Return search result with product price
            return render_template('search.html', message=message, tables=[df.to_html(classes='data', header=True, index=False)], titles=df.columns.values)

        else:
            # If product does not exist, inform the user
            return render_template('search.html', message="This product doesn't exist")

    return render_template('search.html')





@app.route('/captcha')
def captcha():
    return serve_captcha()


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

        # connect to the database, check whether username and password exist
        db = get_db()
        cursor = db.cursor()

        cursor.execute(f"SELECT salt FROM users WHERE username='{username}'")
        salt = cursor.fetchone()[0]

        password, salt = encrypt_password(password, salt)

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password,))
        account = cursor.fetchone()

        if account:
            # 设置 cookie
            resp = make_response(redirect(url_for('search')))
            resp.set_cookie('username', username, max_age=60 * 60 * 24)  # 有效期1天

            # Defence against the brute force attack
            login_attempts[user_ip] = (0, datetime.now())  # Reset on successful login
            return resp


        else:
            record_attempt(user_ip)
            message = "Login failed. Please try again."
            return render_template('login.html', message=message), 401

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        salt = secrets.token_hex(8)
        password, salt = encrypt_password(password, salt)

        # make connection with the database
        db = get_db()
        cursor = db.cursor()

        # check whether the username has existed in the table
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

        # if the username has existed, warn the user
        if cursor.fetchone():
            return render_template('signup.html', message = 'The username is already taken. Please try another one.')


        # insert the new username and password
        cursor.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", (username, password, salt))
        db.commit()

        # finally, go back to the home page
        return render_template('index.html', message='You have signed up successfully!. <br> Sign in or sign up another account')

    return render_template('signup.html')


if __name__ == '__main__':
    # initialize the users table (if there is no users table)
    init_db()
    # run the website
    app.run(debug=True)
