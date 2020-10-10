# project/server/main/views.py
from flask import render_template, Blueprint, jsonify, current_app, request, redirect, url_for, flash, send_from_directory
from project.server.models import User, Contacts
from project.server.user.forms import ForgotPwForm, PasswordForm
from project.server import bcrypt, db
from project.server.sgrid import sendmail
import adif_io
import os
from datetime import datetime

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/favicon.ico")
def favicon():
    print("favicon is being requested")
    return redirect('/static/favicon.ico')


@main_blueprint.route("/")
def home():
    print(User.query.filter_by(id=1).all())
    print(current_app.config.get("BCRYPT_LOG_ROUNDS"))
    return render_template("main/home.html")


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")


@main_blueprint.route("/forgotpw", methods=["GET", "POST"])
def forgot_pw():
    if request.method == 'GET':
        form = ForgotPwForm()
        return render_template("main/forgotpw.html", form=form)
    if request.method == "POST":
        form = ForgotPwForm(request.form)
        if form.validate_on_submit():
            email = form.email.data
            user = User.query.filter_by(email=email).first()
            print(user)
            if user:
                token = user.get_token()
                print(token)  # Send to an email generation api
                sendmail(user.email, token)
                return redirect(url_for("main.home"))


@main_blueprint.route("/resetpw", methods=["GET", "POST"])
def reset_pw():
    if request.method == 'GET':
        form = PasswordForm()
        return render_template("user/password.html", form=form)
    if request.method == "POST":
        token = request.args.get('token')
        verified_result = User.verify_token(token)
        if token and verified_result:
            is_verified_token = True
            password_submit_form = PasswordForm(request.form)
            if password_submit_form.validate_on_submit():
                verified_result.password = bcrypt.generate_password_hash(
                    password_submit_form.password.data, current_app.config.get("BCRYPT_LOG_ROUNDS")).decode("utf-8")
                verified_result.is_active = True
                db.session.add(verified_result)
                db.session.commit()
                # return "password updated successfully"
                flash("password updated successfully")
                return redirect(url_for('user.members'))
        else:
            flash("Password too simple,doesn't match, or token expired!")
            return render_template("user/password.html", form=PasswordForm())


def update_db(filename, current_user):
    filename = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    potential_entries = []
    current_entries = User.query.filter_by(
        callsign=current_user.callsign).first().contacts
    import threading

    def dbwork(filename, email, potential_entries, db, apc):
        with apc():
            import adif_io
            with open(filename, 'r', errors='ignore') as file:
                data = file.read()

            qsos, header = adif_io.read_from_string(data)

            for qso in qsos:
                if 'OPERATOR' in qso and not 'MY_STATION' in qso:
                    qso['MY_STATION'] = qso['OPERATOR']
                entry = Contacts(
                    band=qso['BAND'] if 'BAND' in qso else None,
                    band_rx=qso['BAND_RX'] if 'BAND_RX' in qso else None,
                    call=qso['CALL'] if 'CALL' in qso else None,
                    cont=qso['CONT'] if 'CONT' in qso else None,
                    country=qso['COUNTRY'] if 'COUNTRY' in qso else None,
                    cqz=qso['CQZ'] if 'CQZ' in qso else None,
                    distance=qso['DISTANCE'] if 'DISTANCE' in qso else None,
                    dxcc=qso['DXCC'] if 'DXCC' in qso else None,
                    email=qso['EMAIL'] if 'EMAIL' in qso else None,
                    gridsquare=qso['GRIDSQUARE'] if 'GRIDSQUARE' in qso else None,
                    ituz=qso['ITUZ'] if 'ITUZ' in qso else None,
                    lat=qso['LAT'] if 'LAT' in qso else 'S000 00.000',
                    lon=qso['LON'] if 'LON' in qso else 'W000 00.000',
                    lotw_qsl_rcvd=qso['LOTW_QSL_RCVD'] if 'LOTW_QSL_RCVD' in qso else None,
                    lotw_qsl_sent=qso['LOTW_QSL_SENT'] if 'LOTW_QSL_SENT' in qso else None,
                    lotw_qslsdate=datetime.strptime(
                        qso['LOTW_QSLSDATE'], '%Y%m%d').date() if 'LOTW_QSLSDATE' in qso else None,
                    mode=qso['MODE'] if 'MODE' in qso else None,
                    my_city=qso['MY_CITY'] if 'MY_CITY' in qso else None,
                    my_cnty=qso['MY_CNTY'] if 'MY_CNTY' in qso else None,
                    my_country=qso['MY_COUNTRY'] if 'MY_COUNTRY' in qso else None,
                    my_gridsquare=qso['MY_GRIDSQUARE'] if 'MY_GRIDSQUARE' in qso else None,
                    my_lat=qso['MY_LAT'] if 'MY_LAT' in qso else None,
                    my_lon=qso['MY_LON'] if 'MY_LON' in qso else None,
                    my_name=qso['MY_NAME'] if 'MY_NAME' in qso else None,
                    my_state=qso['MY_STATE'] if 'MY_STATE' in qso else None,
                    name=qso['NAME'] if 'NAME' in qso else None,
                    qsl_rcvd=qso['QSL_RCVD'] if 'QSL_RCVD' in qso else None,
                    qsl_sent=qso['QSL_SENT'] if 'QSL_SENT' in qso else None,
                    qsl_via=qso['QSL_VIA'] if 'QSL_VIA' in qso else None,
                    qso_date=datetime.strptime(
                        qso['QSO_DATE'], '%Y%m%d').date() if 'QSO_DATE' in qso else None,
                    qso_date_off=datetime.strptime(
                        qso['QSO_DATE_OFF'], '%Y%m%d').date() if 'QSO_DATE_OFF' in qso else None,
                    qth=qso['QTH'] if 'QTH' in qso else None,
                    rst_sent=qso['RST_SENT'] if 'RST_SENT' in qso else None,
                    rst_rcvd=qso['RST_RCVD'] if 'RST_RCVD' in qso else None,
                    station_callsign=qso['STATION_CALLSIGN'] if 'STATION_CALLSIGN' in qso else None,
                    userid=User.query.filter_by(email=email).first().id,
                    time_off = None,
                    time_on= None
                )
                if 'TIME_OFF' in qso and len(qso['TIME_OFF']) == 4:
                    entry.time_off = datetime.strptime(qso['TIME_OFF'], '%H%M').time()
                elif 'TIME_OFF' in qso and len(qso['TIME_OFF']) > 4:
                    entry.time_off = datetime.strptime(qso['TIME_OFF'], '%H%M%S').time()
                if 'TIME_ON' in qso and len(qso['TIME_ON']) == 4:
                    entry.time_on = datetime.strptime(qso['TIME_ON'], '%H%M').time()
                elif 'TIME_ON' in qso and len(qso['TIME_ON']) > 4:
                    entry.time_on = datetime.strptime(qso['TIME_ON'], '%H%M%S').time()

                potential_entries.append(entry)
            os.remove(filename)
            cols = [x for x in potential_entries[0].__dict__]
            if len(current_entries) > 0:
                for current in current_entries:
                    for idx, entry in enumerate(potential_entries):
                        same = []
                        for item in cols:
                            if not item.startswith('_'):
                                if entry.__getattribute__(item).__str__() == current.__getattribute__(item).__str__():
                                    same.append(True)
                                else:
                                    same.append(False)
                        if all(same):
                            potential_entries.pop(idx)
            for entry in potential_entries:
                print(entry)
                db.session.add(entry)
            db.session.commit()
            print('Thread Complete')

    t1 = threading.Thread(target=dbwork, args=(
        filename, current_user.email, potential_entries, db, current_app.app_context))
    t1.start()
