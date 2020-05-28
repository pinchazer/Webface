from flask import Blueprint
from flask import render_template
from .form import TextForm
from flask import request
from flask import Markup
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import joblib
from config import Configuration
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
twitter_TfidfVectorizer_path = os.path.join(THIS_FOLDER, 'static/model/twitter_TfidfVectorizer.z')
twitter_TfidfVectorizer_nocomp_simple_path = os.path.join(THIS_FOLDER, 'static/model/twitter_TfidfVectorizer_nocomp_simple')
twitter_model_path = os.path.join(THIS_FOLDER, 'static/model/twitter_model_logreg.z')
twitter_model_simple_path = os.path.join(THIS_FOLDER, 'static/model/twitter_model_logreg_nocomp_simple')


if Configuration.FAST_TEXT_MODEL: #true
    with open(twitter_model_simple_path, 'rb') as f:
        twitter_model_logreg = joblib.load(f)
    with open(twitter_TfidfVectorizer_nocomp_simple_path, 'rb') as f:
        twitter_TfidfVectorizer = joblib.load(f)
        #twitter_TfidfVectorizer = joblib.load(f)
else: #false
    with open(twitter_model_path, 'rb') as f:
        twitter_model_logreg = joblib.load(f)
    with open(twitter_TfidfVectorizer_path, 'rb') as f:
        twitter_TfidfVectorizer = joblib.load(f)
        #twitter_TfidfVectorizer = joblib.load(f)

text = Blueprint('text', __name__, template_folder='templates', static_folder='static')

def preprocess(text):
    tmp = re.sub(r'[^a-z]+', ' ', text.lower())
    tmp = re.sub(r'[\s]+', ' ', tmp)
    return tmp

def prediction(text):
    prc_txt_arr = twitter_TfidfVectorizer.transform([preprocess(text)])
    a = twitter_model_logreg.predict(prc_txt_arr)[0]
    p = twitter_model_logreg.predict_proba(prc_txt_arr)
    if a == 1: #good
        proba = round(p[0, 1]*100, 2)
        if proba > 90:
            answ = Markup("I'm sure that it's <b>good</b>")
        elif 75 < proba <= 90:
            answ = Markup("I think that it's probably <b>good</b>")
        elif 50 <= proba <= 75:
            answ = Markup("Eemmm... well... should be <b>good</b>")
    else: #bad
        proba = round(p[0, 0]*100, 2)
        if proba > 90:
            answ = Markup("That is totally <b>bad</b> thing")
        elif 75 < proba <= 90:
            answ = Markup("Sounds like something <b>bad</b>")
        elif 50 <= proba <= 75:
            answ = Markup("Well... let it be <b>bad</b>")
    if Configuration.FAST_TEXT_MODEL:
        answ = answ + Markup("<b> NOT WORKING PROPERLY, CHECK README IN GIT</b>")
    r = {'answ': answ, 'proba': proba}
    return r

@text.route('/', methods=['POST','GET'])
def index():
    form = TextForm(request.form)
    answer = ''
    if request.method == 'POST' and form.validate():
        answer = prediction(form.txtfld.data) # this is dict {'answ': str, 'proba': float}
    return render_template('text.html', field=form.txtfld, answer=answer)
