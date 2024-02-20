from flask import Flask, request, render_template, jsonify, redirect
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import jinja2
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, current_user
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField, validators
from flask_wtf import FlaskForm
import os
import random
import time
import multiprocessing
import asyncio

app = Flask(__name__)
socketio = SocketIO(app)
login = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/project/www/books_table.db'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
login_manager = LoginManager(app)

DIAPAZON = 15
STEP = 10



class Users(db.Model, UserMixin):
    tablename = 'users'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    username = db.Column(db.String(), nullable=False, unique=True)
    # email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String())

    def init(self, id, username, email, password):
        self.id = id
        self.username = username
        #self.email = email
        self.password = password

    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self.password

    def check_password(self, password):
        return check_password_hash(self.password, password)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired()])
    # email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Password", validators=[validators.DataRequired()])  #PasswordField("Password", validators=[validators.DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField()


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(user_id)


@app.route('/login', methods=['post', 'get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(Users).filter(Users.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/')

        #flash("Invalid password", 'error')
        return "Sorry, you don't log on"

    return render_template('login.html', form=form)

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect("/login")
    return render_template('password.html')

# @socketio.on('my_event')
# def test_message(message):
#     while True:
#         numb = str(random.randint(1, 27))
#         emit('my_response', {'data': numb})
#         time.sleep(1)


@socketio.on('my_event')
def numbers(message):
    with open('t.txt', 'r') as f:
            DIAPAZON, STEP = list(map(int, f.read().split()))

    print(DIAPAZON)
    DIAPAZON += 10
    print(DIAPAZON)
    with open('t.txt', 'w') as f:
        f.write(f"{DIAPAZON}\n{STEP}")

    time.sleep(20)

    with open('t.txt', 'r') as f:
            DIAPAZON, STEP = list(map(int, f.read().split()))

    print(DIAPAZON)
    DIAPAZON -= 10
    DIAPAZON = max([DIAPAZON, 15])
    print(DIAPAZON)
    with open('t.txt', 'w') as f:
        f.write(f"{DIAPAZON}\n{STEP}")

@socketio.on('event')
def generation(message):
    while True:
        
        with open('nums.txt', 'r') as f:
            numb = f.read().split()[-1]
        emit('my_response', {'data': numb})
        time.sleep(1)


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


def new_price():
    while True:
        with open('t.txt', 'r') as f:
            DIAPAZON, STEP = list(map(int, f.read().split()))

            
        num = random.randint(DIAPAZON - STEP, DIAPAZON + STEP)
        
        with open('nums.txt', 'a') as f:
            f.write(" " + str(num))

        time.sleep(1)

with open('nums.txt', 'w') as f:
    f.write("1")
with open('t.txt', 'w') as f:
    f.write(f"{DIAPAZON}\n{STEP}")
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=new_price)
    p1.start()
    socketio.run(app)


#username: demo
# password: 0000
