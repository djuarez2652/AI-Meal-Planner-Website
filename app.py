import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, flash, redirect
from flask_behind_proxy import FlaskBehindProxy
from forms import RegistrationForm


app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_TOKEN')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://users.db'

proxied = FlaskBehindProxy(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f'User({self.username}, {self.email})'

with app.context():
    db.create_all()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', subtitle='Home Page', text='')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)