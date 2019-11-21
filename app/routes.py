""" Creates routes """

from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    """ Using LoginForm class, implements the structure of a create account page"""
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('create_account.html',  title='Create Account', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Using LoginForm class, implements the structure of a log in page """
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',  title='Sign In', form=form)
    
@app.route('/calendar')
def calendar():
    return render_template('calendar.html', title='Calendar')

@app.route('/event')
def event():
    return render_template('event.html', title= 'Events')