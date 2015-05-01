"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, make_response

import functions
from google.appengine.api import users
from google.appengine.ext import ndb


from forms import GuestBookForm
from keys import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    guestbook_name = str(guestbook_name)
    return ndb.Key('Guestbook', DEFAULT_GUESTBOOK_NAME)

class Author(ndb.Model):
    #Sub model for representing an author.
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)

class Greeting(ndb.Model):
    #A main model for representing an individual Guestbook entry.
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

def get():
    guestbook_name = ('guestbook_name', DEFAULT_GUESTBOOK_NAME)
    greetings_query = Greeting.query(
        ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
    greetings = greetings_query.fetch(10)
    user = users.get_current_user()
                

def post(form):
    # We set the same parent key on the 'Greeting' to ensure each
    # Greeting is in the same entity group. Queries across the
    # single entity group will be consistent. However, the write
    # rate to a single entity group should be limited to
    # ~1/second
    guestbook_name = ('guestbook_name', DEFAULT_GUESTBOOK_NAME)
    greeting = Greeting(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
        greeting.author = Author(
                identity=users.get_current_user().user_id(),
                email=users.get_current_user().email())
    
    form = str(form)
    greeting.content = form
    greeting.put()

    query_params = {'guestbook_name': guestbook_name}

    return "posted"


##################################################
###### ROUTES ####################################

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        form = GuestBookForm(request.form)
        if form.validate_on_submit():
            form = form.description.data
            return post(form)
        else: 
            return "must have some content"
    user = users.get_current_user()
    if user:
        form = GuestBookForm()
        return render_template("main.html",
            form=form)
    else:
        return redirect(users.create_login_url(request.url))

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    user = users.get_current_user()
    greetings = Greeting.query()   

    if user:
        return render_template("posts.html",
            greetings=greetings, 
            user=user)
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
