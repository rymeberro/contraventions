from app import app
from flask import render_template
from flask import request, redirect, url_for
from .database import Database
from flask import g
import sqlite3
from datetime import datetime 
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from flask_json_schema import JsonSchema
from flask_json_schema import JsonValidationError
import json
import hashlib
import uuid
#from .schemas import user_insert_schema
#from .schemas import user_update_schema
from flask import jsonify
from functools import wraps
from flask import session

schema = JsonSchema(app)

sched = BackgroundScheduler(daemon=True)
sched.start()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()

@app.errorhandler(404) 
def invalid_route(e): 
     return render_template('public/error404.html')



@app.route("/")
def home():  
    etablissements = get_db().get_list_etablissements()
    username = None
    if "id" in session:
        username = get_db().get_session(session["id"])
    return render_template('public/homeSearch.html', etablissements = etablissements, username=username)



@app.route("/signUp")
def signUp():   
    return render_template('public/signUp.html')

@app.route("/login")
def login():   
    return render_template('public/login.html')

@app.route("/myAccount")
def myAccount():  
    etablissements = get_db().get_list_etablissements()
    if "id" in session:
        username = get_db().get_session(session["id"])
        utilisateur = get_db().get_account_infos(username)
    return render_template('public/myAccount.html', username=username, utilisateur=utilisateur, etablissements = etablissements)

@app.route('/confirmation')
def confirmation_page():
    return render_template('public/confirmation.html')

#scheduled to run everyday at midnight
@sched.scheduled_job('cron', hour='0')
def loadXML():  
    URL = 'http://donnees.ville.montreal.qc.ca/dataset/a5c1f0b9-261f-4247-99d8-f28da5000688/resource/92719d9b-8bf2-4dfd-b8e0-1021ffcaee2f/download/inspection-aliments-contrevenants.xml'
    var_url = urlopen(URL)
    xmldoc = parse(var_url)
    dict = {}

    for item in xmldoc.iterfind('contrevenant'):        
        proprietaire = item.findtext('proprietaire')
        categorie = item.findtext('categorie')
        etablissement = item.findtext('etablissement')
        adresse = item.findtext('adresse')
        ville = item.findtext('ville')
        description = item.findtext('description')
        date_infraction = item.findtext('date_infraction')
        date_jugement = item.findtext('date_jugement')
        montant = item.findtext('montant')
        dict = { 'proprietaire': proprietaire, 'categorie': categorie, 'etablissement': etablissement, 
                'adresse': adresse, 'ville': ville, 'description': description, 'date_infraction': date_infraction, 
                'date_jugement': date_jugement, 'montant': montant 
                }
        get_db().insert_contravention(dict)
#__________________________

@app.route('/api/all')
def all_json():
    contraventions = get_db().get_contraventions()  
    return jsonify(data_json_all(contraventions))


@app.route("/showAll",  methods=["GET","POST"])
def showAll():
    contraventions = get_db().get_contraventions()
    return render_template("public/searchResults.html", contraventions=contraventions, searchText= "showAll")

#_______________________

#Search par mots clés
#__________________________

@app.route("/search",  methods=["GET","POST"])
def search():
    searchText = request.form['searchText']
    contraventions = get_db().get_contraventionsBySearch(searchText)
    return render_template("public/searchResults.html", contraventions=contraventions, searchText= searchText)

#parsing in json for all contraventions all infos 
def data_json_all(contraventions):
    data = [{"proprietaire": each[1],"categorie": each[2],
        "etablissement": each[3],"adresse": each[4],
        "ville": each[5],"description": each[6],
        "date_infraction": each[7],"date_jugement": each[8],
        "montant": each[9]} for each in contraventions]
    return data 

#__________________________

#liste des etablissement present pour la liste deroulante
#__________________________
@app.route('/listEtablissement', methods=["GET"])
def get_list_etablissements_json():
    etablissements = get_db().get_list_etablissements()
    return jsonify(data_json_list_etablissement(etablissements))

#parsing in json for list etablissements pour liste deroulante
def data_json_list_etablissement(etablissements):
    data = [{"etablissement": each[0]} for each in etablissements]
    return data 

#infos par nom etablissement
@app.route('/etablissementSearch', methods=["GET","POST"])
def get_contraventions_etablissement():
    etablissement = request.form['etablissement']
    contraventions = get_db().get_contraventionsByEtablissement(etablissement)
    return render_template("public/etablissementSearchResults.html", contraventions=contraventions, etablissement = etablissement)


#contraventions par nom d'etablissement
#__________________________
@app.route('/etablissement', methods=["GET"])
def get_etablissements_json():
    etablissement = request.args.get('nom')
    contraventions = get_db().get_nbrContraventionsByEtablissement(etablissement)
    return jsonify(data_json_etab_nbrContravention(contraventions))

def data_json_etab_nbrContravention(contraventions):
    data = [{"etablissement": each[0],"nbrContraventions": each[1]} for each in contraventions]
    return data 


#__________________________

#recherche entre 2 dates 
#__________________________
@app.route('/dateSearch', methods=["GET","POST"])
def get_contraventions_date():
    date_debut = request.form['date-debut']
    date_fin = request.form['date-fin']
    contraventions = get_db().get_contraventionsByDateSearch(date_debut, date_fin)
    return render_template("public/periodSearchResults.html", contraventions=contraventions, date_debut = date_debut, date_fin = date_fin)

#contraventions entre 2 dates
@app.route('/contravenants', methods=["GET"])
def get_contraventions_date_json():
    date_debut = request.args.get('du')
    date_fin = request.args.get('au')
    contraventions = get_db().get_contraventionsByDateSearch(date_debut, date_fin)
    return jsonify(data_json_etab_contravention(contraventions))

#parsing in json for etablissement et nbrContraventions
def data_json_etab_contravention(contraventions):
    data = [{"etablissement": each[3],"nbrContraventions": each[10]} for each in contraventions]
    return data 
#__________________________


@app.route('/signUp', methods=["GET", "POST"])
def user_creation():
    utilisateur = request.form["full-name"]
    password = request.form["password"]
    email = request.form["email"]
    # Vérifier que les champs ne sont pas vides
    if utilisateur == "" or password == "" or email == "":
        return render_template("public/signUp.html", error="Tous les champs sont obligatoires.")
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
    get_db().create_user(utilisateur, email, salt, hashed_password)
    return redirect("/confirmation")

@app.route("/showUsers",  methods=["GET","POST"])
def showUsers():
    users = get_db().get_users()
    return jsonify(data_json_users(users))

def data_json_users(contraventions):
    data = [{"id": each[0],"utilisateur": each[1],
        "email": each[2],"salt": each[3],
        "hash": each[3]} for each in contraventions]
    return data 
#_____________


@app.route('/login', methods=["POST"])
def log_user():
    email = request.form["email"]
    password = request.form["password"]
    # Vérifier que les champs ne sont pas vides
    if email == "" or password == "":
        return render_template("public/login.html", error="Tous les champs sont obligatoires.")

    user = get_db().get_user_login_info(email)
    if user is None:
        return redirect("/")

    salt = user[0]
    hashed_password = hashlib.sha512(str(password + salt).encode("utf-8")).hexdigest()
    if hashed_password == user[1]:
        # Accès autorisé
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, email)
        session["id"] = id_session
        return redirect("/")
    else:
        return redirect("/")


def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)
    return decorated


@app.route('/logout')
@authentication_required
def logout():
    id_session = session["id"]
    session.pop('id', None)
    get_db().delete_session(id_session)
    return redirect("/")


def is_authenticated(session):
    return "id" in session


def send_unauthorized():
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


app.secret_key = "(*&*&322387he738220)(*(*22347657"



