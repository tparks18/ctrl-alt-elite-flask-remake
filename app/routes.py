from app import app
from .forms import LoginForm, RegisterForm
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired
from .models import User
# import requests


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        #we will do the logn stuff
       
    return render_template('login.html.j2', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        #create a new user
        try:
            new_user_data = {
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data
            }
            #create an empty user
            new_user_object = User()
            #build user with form data
            new_user_object.from_dict(new_user_data)
            #save user to the database
            new_user_object.save()
        except:
            flash('There was an unexpected error making your account, please try again', 'danger')
            #error return
            return render_template('register.html.j2', form=form)
        #if it worked
        flash('You have registered successfully', 'success')
        return redirect(url_for('login'))

    #get return
    return render_template('register.html.j2', form=form)


@app.route('/')
def index():
    flash('heycoolguys', 'danger')
    return render_template('index.html.j2')