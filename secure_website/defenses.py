from flask import Flask, request, redirect, url_for, render_template, abort, flash, session,make_response, send_file    
import sqlite3
from datetime import datetime, timedelta
from captcha.image import ImageCaptcha                              
import random                                                      
from io import BytesIO
import pandas as pd             
import hashlib
import secrets


login_attempts = {}
PEPPER = '703cf07d693052dca36c16924f1710d1'

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



