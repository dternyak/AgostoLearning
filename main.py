# Import the Flask Framework
from flask import Flask
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, make_response

from google.appengine.api import users
from google.appengine.ext import ndb

import json
from forms import GuestBookForm
from keys import SECRET_KEY
from models import Author, Greeting, post, post_ajax
import time

app = Flask(__name__)
app.secret_key = SECRET_KEY
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


##################################################
###### ROUTES ####################################

@app.route('/', methods=['GET', 'POST'])
def main():
    user = users.get_current_user()
    if user:
        form = GuestBookForm()
        greetings = Greeting.query()
        return render_template("main.html",
            form=form, greetings=greetings, user=user)
    else:
        return redirect(users.create_login_url(request.url))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        form = GuestBookForm(request.form)
        if form.validate_on_submit():
            form = form.description.data
            form = form.replace(" ", "_")
            form = form.replace("!", "")
            post(form)
            return redirect(url_for('main'))
        else: 
            return "must have some content"
    else:
        return "post only"

@app.route('/addajax', methods=['GET', 'POST'])
def addajax():
    if request.method == 'POST':
        angular_dict = request.form
        for list_item in angular_dict.items():
            first_value = list_item[0]
            second_value = list_item[1]
        second_value = second_value.replace("!", "")
        user = users.get_current_user()
        all_content = Greeting.query()
        for contents in all_content:
            if contents.content == first_value and user.user_id() == contents.author.identity:
                second_value = second_value.replace(" ", "_")
                contents.content = second_value
                contents.put()
                print contents
                print "test"
                time.sleep(1)
                return "success"
            else:
                print first_value
                print second_value
                return "nodomain"

    else:
        return "post only"

@app.route('/update', methods=['GET', 'POST'])
def update():
    user = users.get_current_user()
    if user:
        greetings = Greeting.query()
        return render_template("update.html",
            greetings=greetings, user=user)
    else:
        return redirect(users.create_login_url(request.url))


###################################################
##### ERROR HANLDING ##############################




@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
