import os


from functools import wraps
from flask import g, request, redirect, url_for, render_template, session

""" 
Login function taken from
https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
"""

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    return render_template("apology.html", message=message, code=code), code