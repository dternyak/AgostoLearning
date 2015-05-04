# Import the Flask Framework
from flask import Flask
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, make_response

from google.appengine.api import users
from google.appengine.ext import ndb


from forms import GuestBookForm
from keys import SECRET_KEY
from models import Author, Greeting, post
import time

app = Flask(__name__)
app.secret_key = SECRET_KEY
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


##################################################
###### ROUTES ####################################

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        form = GuestBookForm(request.form)
        if form.validate_on_submit():
            form = form.description.data
            post(form)
            return redirect(url_for('main'))
        else: 
            return "must have some content"
    user = users.get_current_user()
    if user:
        form = GuestBookForm()
        greetings = Greeting.query()
        return render_template("main.html",
            form=form, greetings=greetings, user=user)
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
