
from flask import render_template, Blueprint, url_for, redirect, flash, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_login import login_user, logout_user, login_required, current_user
from project.server.main.views import update_db
from project.server import bcrypt, db
from project.server.models import User, Contacts
from project.server.user.forms import LoginForm, RegisterForm, ProfileForm, PasswordForm
from project.server.main.views import update_db 
import json
import requests
import adif_io

user_blueprint = Blueprint("user", __name__)

def getQrzData(apikey, user):
    url = 'https://logbook.qrz.com/api'
    p = (('KEY', apikey), ('ACTION', 'FETCH'), ('OPTION', 'ALL'))
    r = requests.get(url,params=p)
    data = str(r.content, 'utf-8', errors='ignore')
    a = data.replace('&gt;', '>')
    a = a.replace('&lt;','<')
    a = a[a.find('ADIF=')+5:]
    with open(os.path.join(current_app.config['UPLOAD_FOLDER'], user.callsign + '.adi'), 'x' ) as file:
        file.write(a)
        file.close()
    update_db(user.callsign +'.adi', user)
    for idx, qso in enumerate(qsos):
        qsos[idx] = {k.lower(): v for k, v in qso.items()}

    return qsos
