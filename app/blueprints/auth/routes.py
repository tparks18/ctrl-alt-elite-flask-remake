from . import bp as auth
from .forms import LoginForm, RegisterForm, EditProfileForm
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required


@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Do login Stuff
        email = form.email.data.lower()
        #email = request.form.get('email').lower()
        password = request.form.get('password')
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            # Give User feeedback of success
            flash('welcome to fakebook', 'success')
            return redirect(url_for('social.index'))
            # Give user Invalid Password Combo error
        flash('invalid password email combo', 'danger')
        return redirect(url_for('auth.login'))
    return render_template("login.html.j2", form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        #create a new user
        try:
            new_user_data = {
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data,
                "icon": int(form.icon.data)
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
        return redirect(url_for('auth.login'))

    #get return
    return render_template('register.html.j2', form=form)

@auth.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'warning')
        return redirect(url_for('auth.login'))

@auth.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data={
            "first_name": form.first_name.data.title(),
            "last_name": form.last_name.data.title(),
            "email": form.email.data.lower(),
            "password": form.password.data,
            "icon": int(form.icon.data) if int(form.icon.data) != 9000 else current_user.icon
        }
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.email != current_user.email:
            flash('Email already in use', 'danger')
            return redirect(url_for('auth.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile Updated', 'success')
        except:
            flash('There was an unexpected Error. Please try again', 'danger')
            return redirect(url_for('auth.edit_profile'))

    return render_template('register.html.j2', form=form)