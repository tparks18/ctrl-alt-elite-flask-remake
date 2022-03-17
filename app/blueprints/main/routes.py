from . import bp as main
from flask import render_template, request
from flask_wtf import FlaskForm
from flask_login import login_required
import requests

@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/ergast', methods = ['GET', 'POST'])
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
# @main.route('/pokemon', methods = ['GET', 'POST'])
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