""" Creates routes """

from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
import os
import goggle_events

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

@app.route('/task')
def task():
    return render_template('task.html', title= 'Tasks')

@app.route('/survey')
def survey():
    return render_template('survey.html', title='Survey')

@app.route('/newevent', methods=['POST'])
def newevent():
    #projectpath = request.form['C:\Users\mahmad1\Desktop\softdes\FairyGodmothers\FairyGodmothers\app\templates\event.html']
    summary = request.form['eventname']
    day_of_week = request.form['dayofweek']
    start_hour = request.form['shour']
    start_min = request.form['smin']
    am1 = request.form['day1']
    end_hour = request.form['ehour']
    end_min = request.form['emin']
    am2 = request.form['day2']   
    #print("The event name is '" + summary + "'")
    s = start_hour + start_min 
    print(s)
    #start_time_str = day_of_week + start_hour + start_min
    #create_event()
    return redirect('/calendar')