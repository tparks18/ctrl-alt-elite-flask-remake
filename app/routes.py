from app import app
from .forms import LoginForm, RegisterForm
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from .models import User
from flask_login import login_user, current_user, logout_user, login_required
import requests


@app.route('/login', methods=['GET','POST'])
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
            return redirect(url_for('index'))
            # Give user Invalid Password Combo error
        flash('invalid password email combo', 'danger')
        return redirect(url_for('login'))
    return render_template("login.html.j2", form=form)

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

@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'warning')
        return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    # flash('heycoolguys', 'danger')
    return render_template('index.html.j2')

@app.route('/ergast', methods = ['GET', 'POST'])
@login_required
#normally these would all be different functions if we had a larger application
#keep this in mind for code reviews?
def ergast():
    if request.method == 'POST':
        year = request.form.get('year')
        round = request.form.get('round')
        url = f"https://ergast.com/api/f1/{year}/{round}/driverStandings.json"
        response = requests.get(url)
        if response.ok:
            data = response.json()["MRData"]["StandingsTable"]["StandingsLists"]
            if len(data)<=0:
                error_string = f"There is no info for {year} round {round}"
                return render_template('ergast.html.j2', error=error_string)
            all_racers=[]
            for racer in data[0].get("DriverStandings"):
            # for racer in data:
                racer_dict={}
                racer_dict={
                    "first_name": racer['Driver']['givenName'],
                    "last_name": racer['Driver']['familyName'],
                    "position": racer['position'],
                    "wins": racer['wins'],
                    "DOB": racer['Driver']['dateOfBirth'],
                    "nationality": racer['Driver']['nationality'],
                    "constructor": racer['Constructors'][0]['name']
                }
                all_racers.append(racer_dict)
            return render_template('ergast.html.j2', racers = all_racers)
        else:
            error_string = "Houston we have a problem"
            return render_template('ergast.html.j2', error=error_string)
    return render_template('ergast.html.j2')

#make something like this for pokemon api and google books
# @app.route('/pokemon', methods = ['GET', 'POST'])
# def pokemon():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         url = f"https://pokeapi.co/api/v2/pokemon/{name}"
#         response = requests.get(url)
#         if response.ok:
#             data = response.json()
#             if len(data)<=0:
#                 error_string = f"There is no info for {name}"
#                 return render_template('pokemon.html.j2', error=error_string)
#             all_poke=[]
#             for poke in data:
#                 poke_dict={}
#                 poke_dict={
#                     "name": poke['name'],
#                     "height": poke['height'],
#                     "weight": poke['weight'],
#                     "ability": poke['abilities'][0]['ability']['name'],
#                     "image": poke['sprites']['front_shiny']
#                 }
#                 all_racers.append(poke_dict)
#             return render_template('pokemon.html.j2', pokes = all_poke)
#         else:
#             error_string = "Houston we have a problem"
#             return render_template('pokemon.html.j2', error=error_string)
#     return render_template('pokemon.html.j2')