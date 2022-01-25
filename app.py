# Flask Imports
from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional
from flask_sqlalchemy import SQLAlchemy

# Util Imports
from utils import *
import requests, pyperclip, os, pretty_errors

# Creating Image folder
IMAGE_FOLDER = os.path.join('static', 'images')

# Initializing app and configs
app = Flask(__name__)
app.config['SECRET_KEY'] = 'c1e9b5e816d90800898e594b57a76dbb'
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER


# Creating class for HTML Form to obtain info need for main function
class OptionsForm(FlaskForm):
    lang = SelectField('Language:', choices=["All", "Arabic", "Bulgarian", "Catalan", "Chinese", "Czech", "Danish", "Dutch", "English", "Finnish",
        "French", "German", "Greek", "Hindi", "Hungarian", "Indonesian", "Italian", "Japanese", "Korean", "Malay", "Norwegian", "Polish",
        "Portuguese", "Romanian", "Russian", "Slovak", "Spanish", "Swedish", "Tagalog", "Thai", "Turkish", "Ukrainian", "Vietnamese", "Other"])
    top_games = IntegerField('Top ___ Games:', validators=[NumberRange(min=1, max=200), Optional()])
    yes_games = StringField('Only include game(s) in search:', validators=[Optional()])
    no_games = StringField('Exclude game(s) in search:', validators=[Optional()])
    FF = BooleanField('Family Friendly:')
    charity = BooleanField('Charity Streams:')
    v_tuber = BooleanField('V-Tuber:')
    CC = BooleanField('Closed Captions:')
    no_ad = BooleanField('No Sponsored Streams:')
    tag = StringField('Tag:')
    min_viewers = IntegerField('Min Viewers:', validators=[NumberRange(min=0, max=9999999), Optional()])
    max_viewers = IntegerField('Max Viewers:', validators=[NumberRange(min=0, max=9999999), Optional()])
    submit = SubmitField('Find Random Stream')
    
# Home Page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = OptionsForm()
    tag = os.path.join(app.config['UPLOAD_FOLDER'], 'tag.png')
    resp = os.path.join(app.config['UPLOAD_FOLDER'], 'responses.png')
    return render_template('index.html', form=form, tag=tag, resp=resp)

# Results Page
@app.route('/result', methods=['GET', 'POST'])
def result():
    form = OptionsForm()
    img = os.path.join(app.config['UPLOAD_FOLDER'], 'tag.png')
    resp = os.path.join(app.config['UPLOAD_FOLDER'], 'responses.png')
    
    # Variables from Form responses 
    language = request.form['lang']
    try:
        topGames = int(request.form['top_games'])
    except:
        topGames = 200
    included = request.form['yes_games']
    excluded = request.form['no_games']
    try:
        family = bool(request.form['FF'])
    except:
        family = False
    try:
        char = bool(request.form['charity'])
    except:
        char = False
    try:
        captions = bool(request.form['CC'])
    except:
        captions = False
    try:
        virtualTuber = bool(request.form['v_tuber'])
    except:
        virtualTuber = False
    try:
        noSponsor = bool(request.form['no_ad'])
    except:
        noSponsor = False
    custom = request.form['tag']
    try:
        minimum = int(request.form['min_viewers'])
    except:
        minimum = 0
    try:
        maximum = int(request.form['max_viewers'])
    except:
        maximum = 9999999
    
    # Main Function
    string = str(randomStream(gamesIncluded=included, gamesExcluded=excluded, lang=language, minViewers=minimum, maxViewers=maximum, 
                              FF=family,charity=char, notSponsored=noSponsor, vtuber=virtualTuber, CC=captions, tag=custom, top=topGames))
    textLength = len(string)
    
    return render_template('result.html', form=form, string=string, tag=img, resp=resp, length=textLength)

# Activating Debug for Flask
if __name__ == "__main__":
    app.run(debug=False)
    
