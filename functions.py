from google.appengine.api import users
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, make_response

def hello():
	return "hello daniel"

