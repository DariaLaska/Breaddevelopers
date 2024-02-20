from flask import Flask, request, render_template, jsonify, redirect
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import jinja2
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField, validators
from flask_wtf import FlaskForm
import os
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)
login = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Дарья/Desktop/it_2023/flask_example/books_table.db'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
login_manager = LoginManager(app)

DIAPAZON = 15
STEP = 10
MIN_AMOUNT = 7

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


@app.route("/main")
def hello():
     #return redirect()
    return render_template('books.html')


@app.route('/login', methods=['post', 'get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(Users).filter(Users.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/main')

        #flash("Invalid password", 'error')
        return "Sorry, you don't log on"

    return render_template('login.html', form=form)

@app.route('/')
def index():
    return render_template('password_21_02.html')

# @socketio.on('my_event')
# def test_message(message):
#     while True:
#         numb = str(random.randint(1, 27))
#         emit('my_response', {'data': numb})
#         time.sleep(1)

diapozon = 10

# @socketio.on('my_event')
# def numbers():
#     global diapozon
#     diapozon += 5
#     for _ in range(10):
#         numb = str(random.randint(diapozon - 10, diapozon))
#         emit('my_response', {'data': numb})
#         time.sleep(0.1)

# @socketio.on('event')
# def generation(message):
#     print(message)
#     # while True:
#     #     numb = str(random.randint(1, 10))
#     #     emit('my_response', {'data': numb})
#     #     time.sleep(1)


@socketio.on('futures_count')
def futures(count):
    print(count)
    with open('gen_new_num.txt', 'w') as file:
        file.write(f"{count}")

@socketio.on('product_amount')
def product(prod):
    with open('gen_new_num.txt', 'w') as file:
        file.write(f"{prod}")

@socketio.on('price_procent')
def procent(proc):
    with open('gen_new_num.txt', 'w') as file:
        file.write(f"{proc}")

@socketio.on('minimum')
def min_price(min_price):
    with open('gen_new_num.txt', 'w') as file:
        file.write(f"{min_price}")

@socketio.on('maximum')
def max_price(max_price):
    with open('gen_new_num.txt', 'w') as file:
        file.write(f"{max_price}")

def price():
    with open('gen_new_num.txt', 'r') as file:
        futures, product_amount, procent, maxim, minim = list(map(int, file.read().split()))
        global DIAPAZON
        inter = futures*procent
        if inter!=0:
            DIAPAZON *= inter
        if product_amount >= MIN_AMOUNT:
            time.sleep(20)
        if DIAPAZON<minim:
            DIAPAZON = minim
        if DIAPAZON > maxim:
            DIAPAZON = maxim
        emit('my_response', {'data': DIAPAZON})


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)

#username: demo
# password: 0000