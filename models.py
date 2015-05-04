
import time
from google.appengine.api import users
from google.appengine.ext import ndb




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

def post_ajax(first_value, second_value):
    # We set the same parent key on the 'Greeting' to ensure each
    # Greeting is in the same entity group. Queries across the
    # single entity group will be consistent. However, the write
    # rate to a single entity group should be limited to
    # ~1/second
    user = users.get_current_user()
    all_content = Greeting.query()
    for contents in all_content:
        if contents.content == first_value and user.user_id() == contents.author.identity:
            contents.content = second_value
            contents.put()
            print contents
            time.sleep(1)
        else:
            return "failure"



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
    if not "!" in form:
        greeting.content = form
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}

        time.sleep(1)
    else:
        return "! is not allowed to be posted"
    