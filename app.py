import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, SetupForm, LoginForm


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_TOKEN')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
proxied = FlaskBehindProxy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    setup = db.Column(db.Boolean, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    goal_weight = db.Column(db.Integer, nullable=True)
    reason = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'User({self.username}, {self.email})'

with app.app_context():
    # db.drop_all()
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
@app.route('/home')
@login_required
def home():

    is_setup = current_user.setup

    if not is_setup:
        return redirect(url_for('setup', user_id=current_user.id))
    return render_template('home.html', subtitle='Home Page', text='')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username_or_email = form.username.data
        password = form.password.data

        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            logout_user()
            return render_template('login.html', form=form, incorrect=True)
    return render_template('login.html', form=form, incorrect=False)


@app.route('/setup', methods=['GET', 'POST'])
@login_required
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
        login_user(user)
        return redirect(url_for('home'))
    return render_template('setup.html', title='Setup', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=generate_password_hash(form.password.data),
                    setup=False)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('setup', user_id=user.id))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)