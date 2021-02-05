from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField


class LoginForm(FlaskForm):
    username = StringField("Username: ",
                           validators=[validators.Length(min=7, max=50),
                                       validators.DataRequired(message="Enter Persona Username: ")])
    password = PasswordField("password", validators=[validators.DataRequired("Enter Password: ")])
