# project/server/user/views.py


from flask import render_template, Blueprint, url_for, redirect, flash, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_login import login_user, logout_user, login_required, current_user
from project.server.main.views import update_db
from project.server import bcrypt, db
from project.server.models import User, Contacts
from project.server.user.forms import LoginForm, RegisterForm, ProfileForm, PasswordForm, ContactsForm
import json
from datetime import datetime
from project.server.user.qrzapi import getQrzData

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/profile/<callsign>", methods=["GET", "POST"])
@login_required
def profile(callsign):
    if request.method == 'GET':
        user = User.query.filter_by(callsign=callsign).first()
        form = ProfileForm(obj=user, ca=current_app.app_context)
        return render_template("user/profile.html", form=form, user=current_user)

    if request.method == "POST":
        user = User.query.filter_by(callsign=callsign).first()
        form = ProfileForm(request.form)
        if form.validate_on_submit():
            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.callsign = form.callsign.data
            user.theme = form.theme.data
            user.apikey = form.apikey.data
            db.session.merge(user)
            db.session.flush()
            db.session.commit()
            flash("Updated Profile.", "success")
            return redirect(url_for("user.members"))
        else:
            flash("Form Invalid.", "Failure")
            return redirect(url_for("user.profile", callsign=current_user.callsign))


@user_blueprint.route("/pwupdate/<callsign>", methods=["GET", "POST"])
@login_required
def password_update(callsign):
    if request.method == 'GET':
        user = User.query.filter_by(callsign=callsign).first()
        form = PasswordForm(obj=user, ca=current_app.app_context)
        return render_template("user/password.html", form=form, user=current_user)

    if request.method == "POST":
        user = User.query.filter_by(callsign=callsign).first()
        form = PasswordForm(request.form)
        if form.validate_on_submit() and user.callsign == current_user.callsign:
            if form.password.data == form.confirm.data:
                user.password = bcrypt.generate_password_hash(
                    form.password.data, current_app.config.get(
                        "BCRYPT_LOG_ROUNDS")
                ).decode("utf-8")
            db.session.merge(user)
            db.session.commit()
            flash("Updated Profile.", "success")
            return redirect(url_for("user.members"))
        else:
            flash("Form Invalid.", "Failure")
            return redirect(url_for("user.password_update", callsign=current_user.callsign))


@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    callsign=form.callsign.data,
                    password=form.password.data)
        userlist = User.query.filter_by(email=user.email).first()
        if userlist:
            flash("This email address is already in use!")
            return redirect(url_for("user.register"))
        else:
            db.session.add(user)
            db.session.commit()
            login_user(user)

            flash("Thank you for registering.", "success")
            return redirect(url_for("user.members"))

    return render_template("user/register.html", form=form)


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.password, request.form["password"]
        ):
            login_user(user)
            flash("You are logged in. Welcome!", "success")
            return redirect(url_for("user.members"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("user/login.html", form=form)
    return render_template("user/login.html", title="Please Login", form=form)


@user_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out. Bye!", "success")
    return redirect(url_for("main.home"))


@user_blueprint.route("/members")
@login_required
def members():
    #flash(str(current_user.is_authenticated()) + ': ' + str(current_user.id))
    user = {}
    user['email'] = current_user.email
    user['callsign'] = current_user.callsign
    user['theme'] = current_user.theme
    print(current_user.theme)
    return render_template("user/members.html", url='members', user=user)


@login_required
@user_blueprint.route('/api/', methods=['POST'])
def get_data():
    if request.method == "POST":
        data = User.query.filter_by(
            email=request.json['Email']).first().contacts
        info = []
        if data:
            for contact in data:
                newcontact = contact.__dict__
                del(newcontact['_sa_instance_state'])
                info.append(newcontact)
        else:
            user = User.query.filter_by(email=request.json['Email']).first()
            apikey = user.apikey
            if apikey:
                print(apikey, user.callsign)
                data = getQrzData(apikey, user )
                info = data
        return json.dumps(info, indent=4, sort_keys=True, default=str)


@user_blueprint.route("/log", methods=['POST','GET'])
@login_required
def view_log():
    if request.method == "POST":
        with db.session.no_autoflush:
            form = ContactsForm(request.form)
            if form.validate_on_submit():
                contacts = Contacts.query.filter_by(id=int(form.id.data)).first()
                contacts.band = form.band.data
                contacts.band_rx = form.band_rx.data
                contacts.call = form.call.data
                contacts.cont = form.cont.data
                contacts.country = form.country.data
                contacts.cqz = form.cqz.data
                contacts.distance = form.distance.data
                contacts.dxcc = form.dxcc.data
                contacts.email = form.email.data
                contacts.gridsquare = form.gridsquare.data
                contacts.ituz = form.ituz.data
                contacts.lat = form.lat.data
                contacts.lon = form.lon.data
                contacts.lotw_qsl_rcvd = form.lotw_qsl_rcvd.data
                contacts.lotw_qsl_sent = form.lotw_qsl_sent.data
                contacts.lotw_qslsdate = datetime.strptime(form.lotw_qslsdate.data, '%Y-%m-%d').date()
                contacts.mode = form.mode.data
                contacts.my_city = form.my_city.data
                contacts.my_cnty = form.my_cnty.data
                contacts.my_country = form.my_country.data
                contacts.my_gridsquare = form.my_gridsquare.data
                contacts.my_lat = form.my_lat.data
                contacts.my_lon = form.my_lon.data
                contacts.my_name = form.my_name.data
                contacts.my_state = form.my_state.data
                contacts.name = form.name.data
                contacts.qsl_rcvd = form.qsl_rcvd.data
                contacts.qsl_sent = form.qsl_sent.data
                contacts.qsl_via = form.qsl_via.data
                contacts.qso_date = datetime.strptime(form.qso_date.data, '%Y-%m-%d').date()
                contacts.qso_date_off = datetime.strptime(form.qso_date_off.data, '%Y-%m-%d').date() 
                contacts.qth = form.qth.data
                contacts.rst_sent = form.rst_sent.data
                contacts.rst_rcvd = form.rst_rcvd.data
                contacts.station_callsign = form.station_callsign.data
                contacts.time_off = datetime.strptime(form.time_off.data, '%H:%M:%S').time() 
                contacts.time_on = datetime.strptime(form.time_on.data, '%H:%M:%S').time() 
                db.session.merge(contacts)
                db.session.commit()
                flash("Updated Profile.", "success")
                return redirect(url_for("user.view_log"))
            else:
                flash("Form Invalid.", "Failure")
                return redirect(url_for("user.view_log"))
    #flash(str(current_user.is_authenticated()) + ': ' + str(current_user.id))
    form = ContactsForm()
    page = request.args.get('page', 1, type=int)
    contacts = Contacts.query.filter_by(userid=current_user.id)
    contacts = contacts.paginate(page, 15, False)
    next_url = url_for('user.view_log', page=contacts.next_num) \
        if contacts.has_next else None
    prev_url = url_for('user.view_log', page=contacts.prev_num) \
        if contacts.has_prev else None
    return render_template("user/logs.html", title='Logs', contacts=[json.loads(x)for x in [json.dumps(x.__dict__, default=str) for x in contacts.items]],
                           next_url=next_url, prev_url=prev_url, form=form)
    #[json.dumps(x.__dict__,default=str) for x in contacts.items]


@user_blueprint.route("/delete/log/<id>")
@login_required
def del_log(id):
    #flash(str(current_user.is_authenticated()) + ': ' + str(current_user.id))
    if id == 'all':
        contacts = User.query.filter_by(id=current_user.id).first().contacts
        for contact in contacts:
            db.session.delete(contact)
        db.session.commit()
    else:
        contact = Contacts.query.filter_by(id=id).first()
        db.session.delete(contact)
        db.session.commit()
    return redirect('/log')
    #[json.dumps(x.__dict__,default=str) for x in contacts.items]


@user_blueprint.route("/delete/user")
@login_required
def del_user():
    #flash(str(current_user.is_authenticated()) + ': ' + str(current_user.id))
    id = current_user.id
    logout_user()
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect('/')
    #[json.dumps(x.__dict__,default=str) for x in contacts.items]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in current_app.config['ALLOWED_EXTENSIONS']


@login_required
@user_blueprint.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'],
                               filename)


@login_required
@user_blueprint.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename))
            flash('File Uploaded Sucessfully')
            update_db(filename, current_user)
            return redirect(url_for('user.view_log'))
    return '''
        <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
