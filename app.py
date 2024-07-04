import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from forms import RegistrationForm, SetupForm


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_TOKEN')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

proxied = FlaskBehindProxy(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    goal_weight = db.Column(db.Integer, nullable=True)
    reason = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'User({self.username}, {self.email})'

with app.app_context():
    db.drop_all()
    db.create_all()


@app.route('/')
@app.route('/home')
def home():
    login = request.args.get('is_logged_in')
    if login:
        return render_template('home.html', subtitle='Home Page', text='')
    else:
        return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    user_id = request.args.get('user_id')
    form = SetupForm()
    if form.validate_on_submit():
        user = User.query.get(user_id)
        user.age = form.age.data
        user.weight = form.weight.data
        user.goal_weight = form.goal_weight.data
        user.reason = form.reason.data
        db.session.commit()
        flash(f'Account created for {user.username}!', 'success')
        return redirect(url_for('home', is_logged_in=True))
    return render_template('setup.html', title='Setup', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('setup', user_id=user.id))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)