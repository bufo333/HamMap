# project/server/models.py


import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from project.server import db, bcrypt


class Contacts (db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    band = db.Column(db.String(10))
    band_rx = db.Column(db.String(10))
    call = db.Column(db.String(10))
    cont = db.Column(db.String(4))
    country = db.Column(db.String(50))
    cqz = db.Column(db.Integer)
    distance = db.Column(db.Integer)
    dxcc = db.Column(db.String(10))
    email = db.Column(db.String(50))
    gridsquare = db.Column(db.String(10))
    ituz = db.Column(db.Integer)
    lat = db.Column(db.String(20))
    lon = db.Column(db.String(20))
    lotw_qsl_rcvd = db.Column(db.String(10))
    lotw_qsl_sent = db.Column(db.String(10))
    lotw_qslsdate = db.Column(db.Date)
    mode = db.Column(db.String(5))
    my_city = db.Column(db.String(50))
    my_cnty = db.Column(db.String(50))
    my_country = db.Column(db.String(50))
    my_gridsquare = db.Column(db.String(50))
    my_lat = db.Column(db.String(50))
    my_lon = db.Column(db.String(50))
    my_name = db.Column(db.String(50))
    my_state = db.Column(db.String(50))
    name = db.Column(db.String(50))
    qsl_rcvd = db.Column(db.String(50))
    qsl_sent = db.Column(db.String(50))
    qsl_via = db.Column(db.String(50))
    qso_date = db.Column(db.Date)
    qso_date_off = db.Column(db.Date)
    qth = db.Column(db.String(50))
    rst_sent = db.Column(db.String(50))
    rst_rcvd = db.Column(db.String(50))
    station_callsign = db.Column(db.String(50))
    time_off = db.Column(db.Time)
    time_on = db.Column(db.Time)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    callsign = db.Column(db.String(10))
    contacts = db.relationship('Contacts', backref='users', lazy=True, passive_deletes=True, cascade="all, delete" )
    theme = db.Column(db.Integer, default=6)
    apikey = db.Column(db.String(19), nullable=True)

    def __init__(self, email, password, callsign, first_name, last_name, admin=False):
        self.email = email
        self.callsign = callsign
        self.first_name = first_name
        self.last_name = last_name
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode("utf-8")
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.theme = 6

    def get_token(self):
        s = Serializer(
            current_app.config['SECRET_KEY'], current_app.config['EXPIRATION'])
        return s.dumps({'user': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('user')
        if id:
            return User.query.get(id)
        return None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "<User {0}>".format(self.first_name)
