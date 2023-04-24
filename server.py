import json
from flask import Flask, render_template, request, redirect, flash, url_for, abort
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

maxPlaces = 12


def check_for_availability(competition):
    now = datetime.now()
    comp_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    if comp_date < now:
        competition['available'] = False
    elif comp_date >= now:
        competition['available'] = True
    return competition


@app.route('/')
def index():
    return render_template('index.html', clubs=clubs)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email']
                == request.form['email']][0]
    except IndexError:
        flash('There is no account using this email')
        return render_template('index.html')
    for competition in competitions:
        competition = check_for_availability(competition)
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [
            c for c in competitions if c['name'] == competition][0]
    except IndexError:
        flash('Please follow the links and do not attempt to directly enter an url')
        return render_template('index.html')
    try:
        key_exist = foundCompetition["available"]
    except KeyError:
        flash('Please follow the links and do not attempt to directly enter an url')
        return render_template('index.html')
    if foundCompetition['available'] == False:
        flash("You were redirected here because you tried to book place for a competition that already happened")
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        if foundClub and foundCompetition:
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name']
                   == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired > maxPlaces:
        flash('Error: You cannot redeem more than 12 places')
    elif placesRequired < 0:
        flash('Error: You cannot redeem a negative number of places')
    else:
        if int(club['points']) >= placesRequired:
            competition['numberOfPlaces'] = int(
                competition['numberOfPlaces'])-placesRequired
            club['points'] = int(club['points']) - placesRequired
            flash('Great-booking complete!')
        else:
            flash('Error: Inssufficient points')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
