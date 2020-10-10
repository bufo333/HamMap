# project/server/user/forms.py

from project.server import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email Address", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])


class PasswordForm(FlaskForm):
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )


class ForgotPwForm(FlaskForm):
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40),
        ],
    )


class ProfileForm(FlaskForm):
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40),
        ],
    )
    callsign = StringField("callsign", validators=[
        DataRequired(),
        Length(min=2, max=7),
    ],
    )

    first_name = StringField("First Name", validators=[DataRequired(),
                                                       Length(min=2, max=50),
                                                       ],
                             )

    last_name = StringField("Last Name", validators=[DataRequired(),
                                                     Length(min=2, max=50),
                                                     ],
                            )
    apikey = StringField("QRZ API Key", validators=[DataRequired(),
                                                     Length(min=0, max=19),
                                                     ],
    )
    theme = SelectField("Default Map Theme", validators=[DataRequired()],
                        choices=[(0, 'Dark'), (2, 'Light'), (1, 'Street'), (3, 'Vector'),
                                 (4, 'Frank LLoyd Wright'), (5, 'Satellite'), (6, 'Le Shine')]
                        )


class RegisterForm(FlaskForm):
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(),
            Email(message=None),
            Length(min=6, max=40),
        ],
    )
    callsign = StringField("callsign", validators=[
        DataRequired(),
        Length(min=2, max=7),
    ],
    )

    first_name = StringField("First Name", validators=[DataRequired(),
                                                       Length(min=2, max=50),
                                                       ],
                             )

    last_name = StringField("Last Name", validators=[DataRequired(),
                                                     Length(min=2, max=50),
                                                     ],
                            )

    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

class ContactsForm(FlaskForm):
                    band = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    band_rx = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    call = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    cont = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    country = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    cqz = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    distance = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    dxcc = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    email = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    gridsquare = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    ituz = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    lat = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    lon = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    lotw_qsl_rcvd = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    lotw_qsl_sent = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    lotw_qslsdate = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    mode = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    my_city = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    my_cnty = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    my_country = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    my_gridsquare = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    my_lat = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    my_lon = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    my_name = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    my_state = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    name = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    qsl_rcvd = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    qsl_sent = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    qsl_via = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    qso_date = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    qso_date_off = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    qth = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    rst_sent = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    rst_rcvd = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    station_callsign = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    time_off = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    time_on = StringField("", validators=[DataRequired(),
                                                     Length(min=1, max=50),
                                                     ],
                            )
                    id = StringField("", validators=[DataRequired(),
                                    Length(min=1, max=50),
                                    ],
                            )
          