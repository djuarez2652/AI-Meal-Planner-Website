from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class SetupForm(FlaskForm):
    age = IntegerField('Age',
                       validators=[DataRequired(), NumberRange(min=18, max=99)])
    weight = IntegerField('Weight',
                          validators=[DataRequired(), NumberRange(min=0)])
    goal_weight = IntegerField('Goal Weight',
                               validators=[DataRequired(), NumberRange(min=0)])
    reason = StringField('Reason',
                         validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Finish Setup')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Login')