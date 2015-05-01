from google.appengine.api import users
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, make_response

def hello():
	return "hello daniel"

def get():
    # Checks for active Google account session
    user = users.get_current_user()

    if user:
    	return "Hello " + user.nickname()
    else:
        return redirect(users.create_login_url(request.url))