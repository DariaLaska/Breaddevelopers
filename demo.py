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
import multiprocessing

app = Flask(__name__)
socketio = SocketIO(app)
login = LoginManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/user/Desktop/www/books_table.db'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
login_manager = LoginManager(app)

DIAPAZON = 15
STEP = 10
MIN_AMOUNT = 10
PRODUCT_AMOUNT = 100
PROCENT = 50
MAXIM = 100
MINIM = 10
QUEUE = 0


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
    return render_template('password.html')

# @socketio.on('my_event')
# def test_message(message):
#     while True:
#         numb = str(random.randint(1, 27))
#         emit('my_response', {'data': numb})
#         time.sleep(1)

#diapozon = 10

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
    
@socketio.on('event')
def generation(message):
    while True:
        
        with open('nums.txt', 'r') as f:
            numb = f.read().split()[-1]
        emit('my_response', {'data': numb})
        time.sleep(1)


@socketio.on('futures_count')
def futures_increase(count):
    print(count)
    count = float(count["data"])
    with open('t.txt', 'r') as file:
        DIAPAZON, STEP, PRODUCT_AMOUNT, MIN_AMOUNT, PROCENT, MAXIM, MINIM, QUEUE = list(map(float, file.read().split()))

    QUEUE += count

    PRODUCT_AMOUNT -= count
    if PRODUCT_AMOUNT < MIN_AMOUNT:
        t = (MAXIM - MINIM) / 100 * MIN_AMOUNT * count
    else:
        t = (MAXIM - MINIM) / 100 * PROCENT * count
    DIAPAZON += t
    DIAPAZON = min([MAXIM, DIAPAZON])

    
    with open('t.txt', 'w') as f:
        f.write(f"{DIAPAZON}\n{STEP}\n{PRODUCT_AMOUNT}\n{MIN_AMOUNT}\n{PROCENT}\n{MAXIM}\n{MINIM}\n{QUEUE}")

           

def futures_dicrease(t):
    with open('t.txt', 'r') as file:
        DIAPAZON, STEP, PRODUCT_AMOUNT, MIN_AMOUNT, PROCENT, MAXIM, MINIM, QUEUE = list(map(float, file.read().split()))

    QUEUE =- 1.0
    DIAPAZON -= t
    if PRODUCT_AMOUNT < MIN_AMOUNT:
        DIAPAZON = max([DIAPAZON, (MAXIM - MINIM) / 100 * (MIN_AMOUNT / 100) * PRODUCT_AMOUNT])
        
    
    with open('t.txt', 'w') as f:
        f.write(f"{DIAPAZON}\n{STEP}\n{PRODUCT_AMOUNT}\n{MIN_AMOUNT}\n{PROCENT}\n{MAXIM}\n{MINIM}\n{QUEUE}")


def price_dicrease():
    with open('t.txt', 'r') as file:
        DIAPAZON, STEP, PRODUCT_AMOUNT, MIN_AMOUNT, PROCENT, MAXIM, MINIM, QUEUE = list(map(float, file.read().split()))

    time.sleep(20)

    with open('t.txt', 'r') as file:
        DIAPAZON, STEP, PRODUCT_AMOUNT_, MIN_AMOUNT, PROCENT, MAXIM, MINIM, QUEUE = list(map(float, file.read().split()))
    while True:
        if PRODUCT_AMOUNT == PRODUCT_AMOUNT_ and QUEUE > 0:
            print("dis")
            futures_dicrease((MAXIM - MINIM) / 100 * PROCENT)
        with open('t.txt', 'r') as file:
            DIAPAZON, STEP, PRODUCT_AMOUNT, MIN_AMOUNT, PROCENT, MAXIM, MINIM, QUEUE = list(map(float, file.read().split()))

        time.sleep(20)

        with open('t.txt', 'r') as file:
            DIAPAZON, STEP, PRODUCT_AMOUNT_, MIN_AMOUNT, PROCENT, MAXIM, MINIM, QUEUE = list(map(float, file.read().split()))
 

@socketio.on('product_amount')
def product(prod):
    with open('t.txt', 'r') as file:
        DIAPAZON, STEP, PRODUCT_AMOUNT, MIN_AMOUNT, PROCENT, MAXIM, MINIM, QUEUE = list(map(float, file.read().split()))
    with open('t.txt', 'w') as f:
        f.write(f"{DIAPAZON}\n{STEP}\n{prod}\n{MIN_AMOUNT}\n{PROCENT}\n{MAXIM}\n{MINIM}\n{QUEUE}")

@socketio.on('price_procent')
def procent(proc):
    with open('t.txt', 'r') as file:
        DIAPAZON, STEP, PRODUCT_AMOUNT, MIN_AMOUNT, PROCENT, MAXIM, MINIM, QUEUE = list(map(float, file.read().split()))
    with open('t.txt', 'w') as f:
        f.write(f"{DIAPAZON}\n{STEP}\n{PRODUCT_AMOUNT}\n{MIN_AMOUNT}\n{proc}\n{MAXIM}\n{MINIM}\n{QUEUE}")


@socketio.on('minimum')
def min_price(min_price):
    with open('t.txt', 'r') as file:
        DIAPAZON, STEP, PRODUCT_AMOUNT, MIN_AMOUNT, PROCENT, MAXIM, MINIM, QUEUE = list(map(float, file.read().split()))
    with open('t.txt', 'w') as f:
        f.write(f"{DIAPAZON}\n{STEP}\n{PRODUCT_AMOUNT}\n{MIN_AMOUNT}\n{PROCENT}\n{MAXIM}\n{min_price}\n{QUEUE}")


@socketio.on('maximum')
def max_price(max_price):
    with open('t.txt', 'r') as file:
        DIAPAZON, STEP, PRODUCT_AMOUNT, MIN_AMOUNT, PROCENT, MAXIM, MINIM, QUEUE = list(map(float, file.read().split()))
    with open('t.txt', 'w') as f:
        f.write(f"{DIAPAZON}\n{STEP}\n{PRODUCT_AMOUNT}\n{MIN_AMOUNT}\n{PROCENT}\n{max_price}\n{MINIM}\n{QUEUE}")


def price():
    while True:    
        with open('t.txt', 'r') as file:
            DIAPAZON, STEP, PRODUCT_AMOUNT, MIN_AMOUNT, PROCENT, MAXIM, MINIM, QUEUE = list(map(float, file.read().split()))

        num = min([MAXIM, max([MINIM, random.randint(round(DIAPAZON - STEP), round(DIAPAZON + STEP))])])
    
        with open('nums.txt', 'a') as f:
            f.write(" " + str(num))

        time.sleep(1)
    
    
    


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')



with open('nums.txt', 'w') as f:
    f.write("1")
with open('t.txt', 'w') as f:
    f.write(f"{DIAPAZON}\n{STEP}\n{PRODUCT_AMOUNT}\n{MIN_AMOUNT}\n{PROCENT}\n{MAXIM}\n{MINIM}\n{QUEUE}")
if __name__ == '__main__':
    # price_dicrease()
    # price()
    p1 = multiprocessing.Process(target=price)
    p2 = multiprocessing.Process(target=price_dicrease)
    p1.start()
    p2.start()
    socketio.run(app)
#username: demo
# password: 0000
